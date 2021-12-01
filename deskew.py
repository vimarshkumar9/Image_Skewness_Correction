import cv2
import numpy as np
import os,glob

#LOading the image
img = cv2.imread("demo.jpg")

#FUNCTION TO RESIZE IMAGE
def cus_resize(img , percent):
    scale_percent = percent
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)  
    return resized


def angle(img):

    if img.shape[0] > 2000:
        resize_img = cus_resize(img , 40)
    else:
        resize_img = img
    #blurring the img
    blur_img = cv2.GaussianBlur(resize_img , (3,3),0)

    #Converting the imported image to grayscale
    gray_img = cv2.cvtColor(blur_img , cv2.COLOR_BGR2GRAY)

    #Applying Binary thresholding
    thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

    #cv2.imshow("output", thresh_img)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10,5))

    # Dialting the IMage 
    dilate = cv2.dilate(thresh_img, kernel, iterations=1)
    #cv2.imshow("dilated" , dilate)


    '''#canny Edge Detection
    edges_img = cv2.Canny(dilate ,100,200)
    cv2.imshow("edged",edges_img)'''

    #Finding contours
    contours, hierarchy = cv2.findContours(dilate, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_sorted = sorted(contours, key = cv2.contourArea, reverse = True)


    
    #Angle of largest contour
    contour_with_relative_area = resize_img.shape[0] * resize_img.shape[1]*0.9
    contour_with_relative_area_2 = resize_img.shape[0] * resize_img.shape[1]*1
    
    #print(contour_with_relative_area , contour_with_relative_area_2)

    new_contour = [i for i in contours_sorted if cv2.contourArea(i) in range(int(contour_with_relative_area),int(contour_with_relative_area_2))]
    new_contour_sorted = sorted(new_contour, key = cv2.contourArea, reverse = True)
    

   
    #creating rectangular boxes for each contour
    angles = []
    for c in contours_sorted:
        minAreaRect = cv2.minAreaRect(c)
        angles.append(minAreaRect[-1])
        box = cv2.boxPoints(minAreaRect)
        box = np.int0(box)
        im = cv2.drawContours(resize_img.copy(),[box],0,(0,0,255),2)
        #cv2.imshow("im",im)
    #print(angles)
    
    def unique(list):
        unique_list = []
        unique_set = set(list)
        for num in unique_set:
            unique_list.append(num)

        return unique_list

    sorted_list = sorted(unique(angles),reverse=True)
    print(sorted_list)

    if cv2.contourArea(contours_sorted[0]) in range(int(contour_with_relative_area),int(contour_with_relative_area_2)):
        if len(sorted_list)>1:
            if sorted_list[0]==90:
                angle = sorted_list[1]
            else:
                angle = sorted_list[0]
        else:
            angle = sorted_list[0]
    else:
        largestContour = contours_sorted[0]
        minAreaRect = cv2.minAreaRect(largestContour)
        angle = minAreaRect[-1]

    #Angle Required to rotate the image to make it unskewed
    print("Image is skewed at angle of : " ,angle)
    if angle >45:
        angle = angle-90
    if angle ==0:
        print("Image is not skewed")
    else:
        print("Angle we have to rotate to make it straight : ", angle)
    return angle



def rotateImage(new_Image, angle: float):
    newImage = new_Image.copy()
    (h, w) = newImage.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    newImage = cv2.warpAffine(newImage, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return newImage

angle = angle(img)
cv2.imshow("UnSkewed",cus_resize(rotateImage(img ,angle),40))
cv2.waitKey(0)
