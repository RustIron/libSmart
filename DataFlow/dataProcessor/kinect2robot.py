import numpy as np
from numpy import sin,cos,pi

def __rotate_x(theta,d):

	theta = theta * pi / 180
	T = np.zeros([4,4])
	T[0,:] = [1,0,0,0]
	T[1,:] = [0, cos(theta), -sin(theta), d*sin(theta)]
	T[2,:] = [0, sin(theta), cos(theta),  d*cos(theta)]
	T[3,:] = [0,0,0,1]

	return T

def __rotate_Nx(theta,d):

	theta = theta * pi / 180
	T = np.zeros([4,4])
	T[0,:] = [1,0,0,0]
	T[1,:] = [0, cos(theta), sin(theta), d*sin(theta)]
	T[2,:] = [0, -sin(theta), cos(theta),  d*cos(theta)]
	T[3,:] = [0,0,0,1]

	return T

def __rotate_z(theta,d):
	theta = theta * pi / 180
	T  = np.array([[cos(theta), -sin(theta), 0,0],\
      	           [sin(theta), cos(theta) , 0,0],\
                   [0,0,1,d],\
                   [0,0,0,1]]);
	return T


def __offset_x(d):
	T = [[1,0,0,d],\
	      [0,1,0,0],\
	      [0,0,1,0],\
	      [0,0,0,1]]
	return T

def __offset_y(d):
	T = [[1,0,0, 0],\
	      [0,1,0,d],\
	      [0,0,1,0],\
	      [0,0,0,1]]
	return T

def __offset_z(d):
	T = [[1,0,0,0],\
	      [0,1,0,0],\
	      [0,0,1,d],\
	      [0,0,0,1]];



def mat_trans_cam_points_to_robot(j_list):
    [j1,j2,j3,j4] = j_list
    d1 = 100; 
    d2 = 650;  
    d3 = 0;   
    d4 = 0; 
    cam_to_4 = np.array([[0.0251428167266869,  0.0429580868654639,	0.998760452530997,	150.691837790958],
						[-0.00682819705841764,-0.999045605781514,	0.0431422448833940,	16.8780453648336],
						[0.999660549632720,	  -0.00790445074031437,-0.0248254942854018, 580.626270684206],
						[0,	0,	0,	1]])
    '''
    rot = np.array([[ 9.99846e-01,   -1.26353e-03,   1.74872e-02], 
                    [-1.4779096e-03, -9.999238e-01,  1.225138e-02],
                    [1.747042e-02,   -1.227534e-02,  -9.99772e-01]])
    '''

    rot = np.array([[1.26353e-03,  -9.99846e-01,    1.74872e-02], 
                    [9.999238e-01, 1.4779096e-03,  1.225138e-02],
                    [1.227534e-02, -1.747042e-02,  -9.99772e-01]]) 
    '''
    rot = np.array([[0,-1,0],
    				[1,0,0],
    				[0,0,-1]])
    '''
    trans = np.array([[1.9985e-02, -7.44237e-04,-1.0916736e-02]])
    m = np.hstack((rot, -trans.transpose()))
    depth_to_cam = np.vstack((m, np.array([[0,0,0,1]])))

    T5_4 = __rotate_z(j4,d4);#tested, no offset
    T4_3 = __rotate_Nx(-j3,0).dot(__offset_y(-40));#use Negative X rotation
    T3_2 = __rotate_Nx(j2,d2);#use negative X raotation
    T2_1 = __rotate_z(-j1,0).dot(__offset_y(d1));#j1 is negative 
    
    R5 = cam_to_4.dot(depth_to_cam);
    #R5  = np.eye(4)
    R4 = T5_4.dot(R5);
    R3 = T4_3.dot(R4);
    R2 = T3_2.dot(R3);
    R = T2_1.dot(R2);

    return R

from IPython.core.debugger import Tracer

def robotKineticSolve(j_list):
	[j1,j2,j3,j4,j5,j6] = j_list
	d1 = 100
	d2 = 650
	d3 = 0
	d4 = 700
	d5 = 100
	d6 = 0

	TE_6 = __rotate_z(j6,d6)
	T6_5 = __rotate_Nx(-j5,d5)
	T5_4 = __rotate_z(j4,d4);#tested, no offset
	T4_3 = __rotate_Nx(-j3,0).dot(__offset_y(-40));#use Negative X rotation
	T3_2 = __rotate_Nx(j2,d2);#use negative X raotation
	T2_1 = __rotate_z(-j1,0).dot(__offset_y(d1));#j1 is negative 
	'''
	rot = np.array([[1.26353e-03,  -9.99846e-01,    1.74872e-02], 
	                [9.999238e-01, 1.4779096e-03,  1.225138e-02],
	                [1.227534e-02, -1.747042e-02,  -9.99772e-01]]) 
	
	rot = np.array([[0,-1,0],
				   [1,0,0],
				   [0,0,-1]])

	rot = np.array([[-1,0,0],
				    [0,-1,0],
				    [0,0,-1]])

	trans = np.array([[0.019, -7.44237e-04,-0.010]])
	m = np.hstack((rot, -trans.transpose()))
	depth_to_cam = np.vstack((m, np.array([[0,0,0,1]])))

	cam_to_6 = np.array([[-0.267086720759581,0.960622259524707,-0.0766130413156048,0],
				         [0.347552764726496,0.0218704641694929,-0.937405333101960,0],
				         [-0.898816866399974,-0.276995590763974,-0.339708232712227,0.02],
				         [0,0,0,1]])
	'''
	RC = np.array([[0,-1,0,0],
				   [0,0,1,0],
				   [1,0,0,0],
				   [0,0,0,1]])
	
	#RC = cam_to_6.dot(depth_to_cam)
	R6 = TE_6.dot(RC)
	R5 = T6_5.dot(R6)
	R4 = T5_4.dot(R5);
	R3 = T4_3.dot(R4);
	R2 = T3_2.dot(R3);
	R = T2_1.dot(R2);
	#Tracer()()
	return R


if __name__ == '__main__':
	R = mat_trans_cam_points_to_robot([-29.709,69.334,-43.633,37.953])
	print(R)