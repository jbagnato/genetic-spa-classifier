import numpy as np
import argparse
import imutils
import glob
import cv2

# construct the argument parser and parse the arguments
from genspa.constants import PATTERN_DIR, DEBUG_SHOW_PATTERN_IMAGES

"""
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--patterns", required=True, help="Path to patterns to search")
ap.add_argument("-i", "--imagesdir", required=True, help="Path to images where template will be matched")
ap.add_argument("-t", "--threshold", type=int, default=4000000,
                help="Minimum threshold to match de image with pattern.")
ap.add_argument("-v", "--visualize", help="Flag to visualize during seconds the image detected")
args = vars(ap.parse_args())
skip_founded = set()

if args["patterns"].endswith(".jpg"):
    searchIcons = [args["patterns"]]
else:
    searchIcons = glob.glob(args["patterns"] + "/*.jpg")

searchImages = glob.glob(args["imagesdir"] + "/*.png")

results = []
"""

# load the image image, convert it to grayscale, and detect edges
def findIconInImage(pattern_list, image, anchorThreshold=5000000, visualize=False):
    for templatePath in pattern_list:
        template = cv2.imread(PATTERN_DIR + templatePath)
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        template = cv2.Canny(template, 50, 200)
        (tH, tW) = template.shape[:2]

        #anchorThreshold = args.get("threshold")  # recommended 4700000
        scaleRange = np.linspace(0.6, 1.3, 10)

        # loop over the images to find the template in
    #    for imagePath in sorted(searchImages):

        #image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        found = None
        foundInScale = 1.0

        # loop over the scales of the image
        for scale in scaleRange[::-1]:  # 0.5, 1.7, 29 <-- this one works on assignment
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            resized = imutils.resize(gray, width=int(gray.shape[1] * scale))
            r = gray.shape[1] / float(resized.shape[1])

            # if the resized image is smaller than the template, then break
            # from the loop
            if resized.shape[0] < tH or resized.shape[1] < tW:
                break

            # detect edges in the resized, grayscale image and apply template
            # matching to find the template in the image
            edged = cv2.Canny(resized, 50, 200)
            result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
            (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)

            # if we have found a new maximum correlation value, then ipdate
            # the bookkeeping variable
            if maxVal and (maxVal > anchorThreshold):
                found = (maxVal, maxLoc, r)
                #foundInScale = scale

        if found:
            # unpack the bookkeeping varaible and compute the (x, y) coordinates
            # of the bounding box based on the resized ratio
            (maxVal, maxLoc, r) = found
            print(maxVal)
            (startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
            (endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

            # check to see if the iteration should be visualized
            #print(imagePath, startX, startY, endX - startX, endY - startY, "val", maxVal, "scale",
            #      f"{foundInScale:.2f}", templatePath)
            #results.append({'img': imagePath, 'x': startX, 'y': startY, 'w': endX - startX, 'h': endY - startY,
            #                'proba': round(maxVal / 1000000, 2), 'scale': round(foundInScale, 2)})
            if visualize or DEBUG_SHOW_PATTERN_IMAGES:
                # draw a bounding box around the detected result and display the image
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
                cv2.namedWindow('Image', cv2.WINDOW_NORMAL)  # WINDOW_AUTOSIZE
                cv2.imshow("Image", image)
                cv2.waitKey(int(2))
            return maxVal * 1000 / 10000000
        #else:
    return 0.0

