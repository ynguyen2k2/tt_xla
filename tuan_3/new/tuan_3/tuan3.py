# Khai báo sử dụng hàm sobel
from matplotlib import pyplot as plt
from skimage.filters import sobel
import os


path1 = os.path.abspath("image/thanhpho.jpg")
image = plt.imread(path1)
path2 = os.path.abspath("image/luocdo.jpg")
image2 = plt.imread(path2)
path3 = os.path.abspath("image/xq.jpg")
image3 = plt.imread(path3)
path4 = os.path.abspath("image/coffee.jpg")
image4 = plt.imread(path4)

# áp dụng hàm sobel để lọc cạnh
edge_sobel = sobel(image)


# hiển thị kết quả ảnh gốc và ảnh đã được lọc cạnh
def plot_comparison(original, filtered, title_filtered):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(8, 6), sharex=True, sharey=True)
    ax1.imshow(original, cmap=plt.cm.gray)
    ax1.set_title("original")
    ax1.axis("off")
    ax2.imshow(filtered, cmap=plt.cm.gray)
    ax2.set_title(title_filtered)
    ax2.axis("off")


plot_comparison(image, edge_sobel, "Edge with Sobel")
