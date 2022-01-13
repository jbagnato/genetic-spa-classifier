import numpy as np
import argparse
import imutils
import glob
import cv2
import pytesseract

from genspa.constants import DEBUG_SHOW_PATTERN_IMAGES, TESSERACT_TIMEOUT, SCREEN_RES


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

            if w >int(380*SCREEN_RES*scale) and h>(350*SCREEN_RES*scale):
                if DEBUG_SHOW_PATTERN_IMAGES:
                    cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
                    cv2.imshow('shapes', cv_image)
                    cv2.waitKey(1)
                return 10.0

    return 0.0


def detect_image_gallery(cv_image, scale=1.0):
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    imgGry = cv2.GaussianBlur(imgGry, (17, 17), 0)
    # Blur the image for better edge detection
    #imgGry = cv2.GaussianBlur(imgGry, (3, 3), sigmaX=0, sigmaY=0)

    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    #cv2.imshow('test', thrash)
    #cv2.waitKey(3)
    #return

    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    qty = 0

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.09 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5

        cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)

        if len(approx) == 4:
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            #print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv2.putText(cv_image, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
            else:
                cv2.putText(cv_image, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            if (w >(75*SCREEN_RES*scale) and h>(100*SCREEN_RES*scale)) and (w < (175*SCREEN_RES*scale) and h<(300*SCREEN_RES*scale)):
                qty += 1

                if qty >= 3:
                    if DEBUG_SHOW_PATTERN_IMAGES:
                        cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
                        cv2.imshow('shapes', cv_image)
                        cv2.waitKey(1)
                    return 10.0

    return 0.0


def detect_big_button(cv_image, scale=1.0):
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    imgGry = cv2.GaussianBlur(imgGry, (17, 17), 0)
    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    qty = 0
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.13 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        #cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
        if len(approx) == 4:
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            #print(aspectRatio)
            if aspectRatio >= 0.95 and aspectRatio < 1.05:
                cv2.putText(cv_image, "square", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))
                continue
            else:
                cv2.putText(cv_image, "rectangle", (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))

            if (w >(50*SCREEN_RES*scale) and h>(25*SCREEN_RES*scale)) and (w < (250*SCREEN_RES*scale) and h<(105*SCREEN_RES*scale)):
                qty += 1

    if qty == 1:
        if DEBUG_SHOW_PATTERN_IMAGES:
            #cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
            cv2.imshow('shapes', cv_image)
            cv2.waitKey(1)
        return 10.0

    return 0.0


def detect_product_features(cv_image, scale=1.0):
    original = cv_image.copy()
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    imgGry = cv2.GaussianBlur(imgGry, (17, 17), 0)
    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    qty = 0
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.09 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5
        cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
        if len(approx) == 4:
            x, y , w, h = cv2.boundingRect(approx)
            aspectRatio = float(w)/h
            if (w >(50*SCREEN_RES*scale) and h>(50*SCREEN_RES*scale)) and (w < (350*SCREEN_RES*scale) and h<(350*SCREEN_RES*scale)):
                qty += 1
                if qty >= 2:
                    if DEBUG_SHOW_PATTERN_IMAGES:
                        cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)
                        cv2.imshow('shapes', cv_image)
                        cv2.waitKey(1)
                # AND has to have some text
                hasText = detectAbout(original, scale=scale, min_len=20, min_boxes=2, min_intros=1, min_box_height=20*SCREEN_RES)
                if hasText>0.0:
                    return 10.0

    return 0.0


def detect_banner(cv_image, scale=1.0):
    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    imgGry = cv2.GaussianBlur(imgGry, (7, 7), 0)

    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours , hierarchy = cv2.findContours(thrash, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.09 * cv2.arcLength(contour, True), True)
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

            if w >(400*SCREEN_RES*scale) and h<(200*SCREEN_RES*scale):
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
        elif len(approx) == 4:
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
    ih = gray.shape[0]
    iw = gray.shape[1]

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
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    #im2 = cv_image.copy()

    # Looping through the identified contours
    # Then rectangular part is cropped and passed on
    # to pytesseract for extracting text from it
    # Extracted text is then written into the text file
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        if h<(56*SCREEN_RES*scale):
            continue
        if y <(65*SCREEN_RES*scale) or y > (ih - (75*SCREEN_RES*scale)):
            continue

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Cropping the text block for giving input to OCR
        cropped = cv_image[y:y + h, x:x + w]

        try:
            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(cropped, timeout=TESSERACT_TIMEOUT)
        except Exception as e:
            print("ERROR, TESSERACT TIMEOUT!" + str(e))
            return 0.0

        number_of_intros = len(text.strip().splitlines())
        # Get bounding box estimates
        bounding = pytesseract.image_to_boxes(cropped,output_type='dict')

        if text and type(text) == str and len(text) > 4 and w > (125*SCREEN_RES*scale) and h > ((56*SCREEN_RES*scale)*number_of_intros)\
                and bounding['right'][0] < w and bounding['top'][0]< h :
            #print(w,h,text)
            #print(boundes['left'][0],boundes['bottom'][0],boundes['right'][0],boundes['top'][0])

            # Get verbose data including boxes, confidences, line and page numbers
            #print(pytesseract.image_to_data(cropped))

            if DEBUG_SHOW_PATTERN_IMAGES:
                cv2.drawContours(cv_image, cnt, 0, (0, 0, 0), 5)
                cv2.imshow('text', cv_image)
                cv2.waitKey(1)
            return 10.0

    return 0.0


def detectAbout(cv_image, scale=1.0, min_len=30, min_boxes=4, min_intros=1, min_box_height=50*SCREEN_RES):
    # Convert the image to gray scale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    # A smaller value like (10, 10) will detect
    # each word instead of a sentence.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (38,38))  #(18, 18))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

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

        if h<(min_box_height*scale):
            continue

        # Drawing a rectangle on copied image
        rect = cv2.rectangle(cv_image, (x, y), (x + w, y + h), (0, 255, 0), 2)


        # Cropping the text block for giving input to OCR
        cropped = cv_image[y:y + h, x:x + w]

        # Apply OCR on the cropped image
        try:
            text = pytesseract.image_to_string(cropped, timeout=TESSERACT_TIMEOUT)
        except Exception as e:
            print("ERROR, TESSERACT TIMEOUT!(2)" + str(e))
            return 0.0
        number_of_intros = len(text.strip().splitlines())
        #print(len(text),h,w,number_of_intros,text)

        if text and type(text) == str and len(text)>4 and h>(50*SCREEN_RES*scale) and number_of_intros > min_intros:
            cv2.drawContours(cv_image, cnt, 0, (0, 0, 0), 5)
            accum_text += " " + text.strip()
            qty += 1

            if qty >= min_boxes and len(accum_text) > min_len:
                if DEBUG_SHOW_PATTERN_IMAGES:
                    cv2.imshow('text', cv_image)
                    cv2.waitKey(1)
                return 10.0

    return 0.0

def detectBlank(cv_image, scale=1.0):
    try:
        text = pytesseract.image_to_string(cv_image, timeout=TESSERACT_TIMEOUT)
    except Exception as e:
        #print("ERROR, TESSERACT TIMEOUT!(3)" + str(e))
        return 0.0

    if text and type(text) == str and len(text)>4:
        # if there is text, is not blank
        return 0.0

    imgGry = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
    imgGry = cv2.GaussianBlur(imgGry, (17, 17), 0)

    ret , thrash = cv2.threshold(imgGry, 240 , 255, cv2.CHAIN_APPROX_NONE)
    contours, hierarchy = cv2.findContours(thrash, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    qty = 0
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.2 * cv2.arcLength(contour, True), True)
        x = approx.ravel()[0]
        y = approx.ravel()[1] - 5

        cv2.drawContours(cv_image, [approx], 0, (0, 0, 0), 5)

        qty += 1

        if len(approx) > 4:
            return 0.0

        if qty > 5:
            return 0.0

    return 1.0


def detect_form(cv_image, scale=1.0):
    try:
        text = pytesseract.image_to_string(cv_image, timeout=TESSERACT_TIMEOUT)
    except Exception as e:
        #print("ERROR, TESSERACT TIMEOUT!(3)" + str(e))
        return 0.0

    if text and type(text) == str and len(text)>3:
        possible= ["sign up","sign me up","subscribe","submit", "send", "email", "notify me","subscription"]
        for s in possible:
            if text.lower().find(s) >=0:
                return 7.0

    return 0.0
