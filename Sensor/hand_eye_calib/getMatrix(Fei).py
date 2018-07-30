import cv2
import glob
import numpy as np 
from numpy import array,mat,sin,cos,dot,eye
from numpy.linalg import norm
from numpy import * 
from IPython.core.debugger import Tracer

a = np.load('./cam_calibration_output_set2.npz', mmap_mode=None, allow_pickle=True, fix_imports=False, encoding='ASCII')


def rodrigues(r):
    def S(n):
        Sn = array([[0,-n[2],n[1]],[n[2],0,-n[0]],[-n[1],n[0],0]])
        return Sn
    theta = norm(r)
    if theta > 1e-30:
        n = r/theta
        Sn = S(n)
        R = eye(3) + sin(theta)*Sn + (1-cos(theta))*dot(Sn,Sn)
    else:
        Sr = S(r)
        theta2 = theta**2
        R = eye(3) + (1-theta2/6.)*Sr + (.5-theta2/24.)*dot(Sr,Sr)
    return mat(R)
	

rvecs = a['rvecs']
tvecs = a['tvecs']
#print ('rvecs shape is ', rvecs.shape)
rot_Mat = np.zeros([19,3,3])
for i in range (0,18):
	rot_Mat [i,:,:] = rodrigues (rvecs[i])

# print Rot_Mat
# np.save("rotation matrix",rot_Mat)

#CBAK is the matrix from calibration borad to kinect


CBAK = np.zeros([19,4,4])

#print ('Rot_Mat shape is',Rot_Mat.shape)
#print ('tvecs shape is ',tvecs.shape)

for i in range (0,18):

    CBAK[i,0:3, 0:3] = rot_Mat [i]
    CBAK[i,0:3, 3] = tvecs [i].reshape(-1)
    CBAK[i,3,     3] = 1
print("tvecs is ",tvecs)
#print(CBAK)
np.save("CalibrationtoKinect_set2",CBAK)

#coordinates of the point in kinect frame
CKF = np.zeros([19,4,1]) 

for i in range (0,19):
    CKF [i,0:4,0:] = CBAK [i].dot(np.array([55,0,0,1]).reshape(-1,1))

print ("coordinate is kinect frame is", CKF)    
print(CKF.shape)
#tmp = np.zeros([4,4])
#tmp[0:3, 0:3] = R 
#tmp[ 3 , 0:3] = t
#tmp[3,3]      = 1

