import numpy as np
import argparse
import imutils
import glob
import cv2


def detect_big_image(cv_image):
    template = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    #template = cv2.Canny(template, 50, 200)
    return 0.0

