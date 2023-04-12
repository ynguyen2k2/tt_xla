# Khai báo sử dụng hàm sobel
from matplotlib import pyplot as plt
from skimage.filters import sobel
import os

path = os.path.abspath("image/vo.jpg")
image = plt.imread(path)
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
