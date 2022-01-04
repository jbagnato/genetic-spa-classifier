import numpy as np
import argparse
import imutils
import glob
import cv2
import pytesseract

from genspa.constants import DEBUG_SHOW_PATTERN_IMAGES


def detect_big_image(cv_image, scale=1.0):
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 4:
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            #print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv2.putText(cv_image, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            else:
                cv2.putText(cv_image, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            if w >int(1000*scale) and h>(700*scale):
                if DEBUG_SHOW_PATTERN_IMAGES:
                    cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
                    cv2.imshow('shapes', cv_image)
                    cv2.waitKey(1)
                return 10.0

    return 0.0


def detect_image_gallery(cv_image, scale=1.0):
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    qty = 0

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 4 :
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            #print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv2.putText(cv_image, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            else:
                cv2.putText(cv_image, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            if (w >(300*scale) and h>(300*scale)) and (w < (600*scale) and h<(500*scale)):
                qty+=1

                if qty>4:
                    if DEBUG_SHOW_PATTERN_IMAGES:
                        cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
                        cv2.imshow('shapes', cv_image)
                        cv2.waitKey(1)
                    return 10.0

    return 0.0


def detect_banner(cv_image, scale=1.0):
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 4 :
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            #print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv2.putText(cv_image, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            else:
                cv2.putText(cv_image, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            if w >(1700*scale) and h<(400*scale):
                if DEBUG_SHOW_PATTERN_IMAGES:
                    cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
                    cv2.imshow('shapes', cv_image)
                    cv2.waitKey(1)
                return 10.0

    return 0.0

def detect_shapes(cv_image, scale=1.0):
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        if len(approx) == 3:
            cv2.putText( cv_image, "Triangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0) )
        elif len(approx) == 4 :
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            #print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv2.putText(cv_image, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            else:
                cv2.putText(cv_image, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            if w >60 and h>60:
                if DEBUG_SHOW_PATTERN_IMAGES:
                    cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
                    cv2.imshow('shapes', cv_image)
                    cv2.waitKey(1)
                return 10.0

        elif len(approx) == 5 :
            cv2.putText(cv_image, "pentagon", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        elif len(approx) == 10 :
            cv2.putText(cv_image, "star", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
        #else:
        #    cv2.putText(cv_image, "circle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

    return 0.0

def detectBigTitle(cv_image, scale=1.0):
    # Convert the image to gray scale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = cv_image.copy()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = im2[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        if text and type(text) == str and len(text)>4 and w > (250*scale) and h>(113*scale):
            if DEBUG_SHOW_PATTERN_IMAGES:
                cv2.drawContours(im2, cnt, 0, (0, 0, 0), 5)
                cv2.imshow('text', im2)
                cv2.waitKey(1)
            return 10.0

    return 0.0

def detectAbout(cv_image, scale=1.0):
    # Convert the image to gray scale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    #im2 = cv_image.copy()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    qty=0
    accum_text = ""
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = cv_image[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        text = pytesseract.image_to_string(cropped)

        if text and type(text) == str and len(text)>4 and h<(100*scale):
            cv2.drawContours(cv_image, cnt, 0, (0, 0, 0), 5)
            accum_text += " " + text
            qty += 1

            if qty > 4 or len(accum_text) > 40:
                if DEBUG_SHOW_PATTERN_IMAGES:
                    cv2.imshow('text', cv_image)
                    cv2.waitKey(1)
                return 10.0

    return 0.0
