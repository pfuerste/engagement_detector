import numpy as np
import cv2
from matplotlib import pyplot as plt


def cut_img(img, bbs):
    """Returns n cropped bbs from an image and a list of n bb-coordinates.

    Args:
        img (np.array): image.
        bbs (list): list of n tuples of ints of the form (top, right, bot, left)

    Returns:
        list: list of np.arrays
    """
    imgs = list()
    for bb in bbs:
        imgs.append(img[bb[0]:bb[2], bb[3]:bb[1]])

    return imgs


def get_angle(p1, p2):
    """get angle in degree on line between two points

    Args:
        p1 (float): tuple of (x,y)-coordinates of a point
        p2 (float): tuple of (x,y)-coordinates of a point

    Returns:
        float: degree of line
    """
    rad = np.arctan2(p1[1] - p2[1], p1[0] - p2[0])
    return np.rad2deg(rad)


def hough_lines_cutter(img):
    """ Uses a hough transform to get horizontal and vertical lines
        in an image.

    Args:
        img (np.array): image
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    minLineLength = 100
    maxLineGap = 10
    # TODO: find better params for lineextractor
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
                            lines=np.array([]), minLineLength=minLineLength, maxLineGap=80)

    a, b, c = lines.shape
    for i in range(a):
        deg = get_angle((lines[i][0][0], lines[i][0][1]),
                        (lines[i][0][2], lines[i][0][3]))
        if deg not in [0, 90, 180]:
            continue
        cv2.line(line_img, (lines[i][0][0], lines[i][0][1]),
                 (lines[i][0][2], lines[i][0][3]), (0, 0, 255), 3, cv2.LINE_AA)

    plt.subplot(131), plt.imshow(gray, cmap="gray")
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132), plt.imshow(edges, cmap='gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(133), plt.imshow(line_img, cmap='gray')
    plt.title('Line Image'), plt.xticks([]), plt.yticks([])
    plt.show()


if __name__ == "__main__":
    img = cv2.imread('input/data/zoom_ui2.png')
    line_img = np.zeros_like(img)
    hough_lines_cutter(img)
