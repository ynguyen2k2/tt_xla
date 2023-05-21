from typing import Sequence
import os
import numpy as np
import math
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
path = os.path.abspath("video/san_pham.mp4")
i = 0


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


def processImage(slices):
    out_detections = []
    if slices is not None:
        for label_slice in slices:
            bboxx = label_slice[1]
            bboxy = label_slice[0]
            ymin, ymax, xmin, xmax = bboxy.start, bboxy.stop, bboxx.start, bboxx.stop

            out_detections.append(Detection(box=[xmin, ymin, xmax, ymax], score=1, class_id=None))

    return out_detections

def draw_dot_center(frame,bbox):
    xmin, ymin, xmax, ymax = bbox
    center_x = math.floor((xmin + xmax) / 2)
    center_y = math.floor((ymin + ymax) /2)
    cv2.line(frame, (center_x, center_y), (center_x+1, center_y), (0, 0, 255), 2)
    return center_x,center_y

def draw_center_line(frame):
    width, height = frame.shape[:2]
    widthline = math.floor(width / 5)
    cv2.line(frame, (widthline, height+height), (widthline, 0), (0, 255, 0), 2)
def countObject(frame,count,center_y,counted):
    line_x = math.floor(frame.shape[1] / 2)
    tolerance = 1  # Khoảng dung sai cho phép
    if abs(center_y - line_x) <= tolerance:
        if counted == 1 :
            count += 1
    print(count)
    print_text(frame,count,frame.shape[2])
    return count

def print_text(frame,count,height):
    font = cv2.FONT_HERSHEY_DUPLEX
    color = (255, 0, 0)  # red
    fontsize = 1
    text = str(count)
    position = (100, 100)
    cv2.putText(frame, text, position, font, fontsize, color=color)

def run(video_path, video_downscale: float = 0.4, viz_wait_ms: int = 1, i=0):
    model_spec = {'order_pos': 1, 'dim_pos': 2,
                  'order_size': 0, 'dim_size': 2,
                  'q_var_pos': 5000., 'r_var_pos': 0.1}

    cap, cap_fps = read_video_file(video_path)

    dt = 1 / cap_fps  # assume 15 fps
    tracker = MultiObjectTracker(dt=dt, model_spec=model_spec)
    while True:
        ret, frame = cap.read()
        couted = 1
        #print(frame.shape)
        if not ret:
            break

        frame = cv2.resize(frame, fx=video_downscale, fy=video_downscale, dsize=None, interpolation=cv2.INTER_AREA)
        # chuyen anh sang anh xam
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # chuyen anh sang nhi phan
        ret, threshold1 = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)
        threshold_dilation = dilatation(threshold1)
        threshold_erosion = erosion(threshold_dilation)

        labeled_array, num_features = label_array(threshold_erosion)
        slices = finding_object(labeled_array)
        detections = processImage(slices)
        # print('detections process: ', detections)

        _ = tracker.step(detections)
        tracks = tracker.active_tracks(min_steps_alive=45)

        for det in detections:
            draw_detection(frame, det)


        for track in tracks:
            draw_track(frame, track)
            center_xframe,center_yframe=draw_dot_center(frame,track[1])
            #print(center_xframe,center_xframe)
            i = countObject(frame, i, center_xframe,couted)


        draw_center_line(frame)
        cv2.imshow('frame', frame)
        c = cv2.waitKey(viz_wait_ms)
        if c == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


run(video_path=path, i=0 )
