
from typing import Sequence
import os
import numpy as np

from scipy.ndimage import label
from scipy import ndimage
import cv2
import torch
import torchvision
import torchvision.transforms as transforms
from motpy import Detection, ModelPreset, MultiObjectTracker, NpImage
from motpy.core import setup_logger
from motpy.detector import BaseObjectDetector
from motpy.testing_viz import draw_detection, draw_track
from motpy.utils import ensure_packages_installed


path = os.path.abspath("video/san_pham1.mp4")
i =0




def read_video_file(video_path: str):
    video_path = os.path.expanduser(video_path)
    cap = cv2.VideoCapture(video_path)
    video_fps = float(cap.get(cv2.CAP_PROP_FPS))
    return cap, video_fps


def erosion(src):
    kernel = np.ones((5, 5), np.uint8)
    erosion_dst = cv2.erode(src, kernel)
    return erosion_dst


def dilatation(src):
    kernel = np.ones((5, 5), np.uint8)
    dilatation_dst = cv2.dilate(src, kernel)
    return dilatation_dst


def label_array(array_binary):
    a = np.array(array_binary)
    labeled_array, num_features = label(a)
    return labeled_array, num_features

def finding_object(array_object):
    return ndimage.find_objects(array_object)


def processImage(slices,i):

    out_detections = []
    if slices is not None:
        for label_slice in slices:
            bboxx = label_slice[1]
            bboxy = label_slice[0]
            ymin, ymax, xmin, xmax = bboxy.start, bboxy.stop, bboxx.start, bboxx.stop
            i=i+1
            out_detections.append(Detection(box=[xmin, ymin, xmax, ymax], score=1,class_id = i))
            print(i)
    return out_detections
def run(video_path, video_downscale: float = 0.4, viz_wait_ms: int = 1,i=0):
    model_spec = {'order_pos': 1, 'dim_pos': 2,
                  'order_size': 0, 'dim_size': 2,
                  'q_var_pos': 5000., 'r_var_pos': 0.1}


    cap, cap_fps = read_video_file(video_path)

    dt = 1 / cap_fps # assume 15 fps
    tracker = MultiObjectTracker(dt=dt, model_spec=model_spec)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, fx=video_downscale, fy=video_downscale, dsize=None, interpolation=cv2.INTER_AREA)
        # chuyen anh sang anh xam
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blob = cv2.dnn.blobFromImage(gray, 1.0, (300, 300), [104, 117, 123], False, False)
        # chuyen anh sang nhi phan
        ret, threshold1 = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)
        threshold_dilation = dilatation(threshold1)
        threshold_erosion = erosion(threshold_dilation)

        labeled_array, num_features = label_array(threshold_erosion)
        slices=finding_object(labeled_array)
        detections = processImage(slices,i)
        # print('detections process: ', detections)

        _ = tracker.step(detections)
        tracks = tracker.active_tracks(min_steps_alive=45)

        for det in detections:
            draw_detection(frame, det)


        for track in tracks:
            draw_track(frame, track)


        cv2.imshow('frame', frame)
        c = cv2.waitKey(viz_wait_ms)
        if c == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


run(video_path=path,i=0)
