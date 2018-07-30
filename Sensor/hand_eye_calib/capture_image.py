#!/usr/bin/env python

import cv2
import glob 
import numpy as np

from IPython.core.debugger import Tracer

set_i = 8
# Tracer()()

# from openCV Python Tutorials

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((7*6,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
objp = objp * 55;

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = sorted(glob.glob ('./image/set%d/*.jpg'%set_i))

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    # chess board is 8*6

    ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
    
    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
        cv2.imshow('img',img)
        cv2.waitKey(5000)
        print(fname, 'has found corners')
    # If not found, print file name
    if ret == False:
        print(fname, 'didnot found corners')


cv2.destroyAllWindows()

# to get the matrix
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None, None)

#Save several arrays into a single file in uncompressed ``.npz`` format.

np.savez("cam_calibration_output_set%d"%set_i, ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)


