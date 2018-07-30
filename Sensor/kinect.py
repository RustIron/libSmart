#!/usr/bin/env python
import freenect
import cv2
import numpy as np
import time
from threading import Thread, Lock
from IPython.core.debugger import Tracer
'''
cv2.namedWindow('RGB')
'''
class Kinector():
    
    def __init__(self):
        
        self.depth_frame = None
        self.color_frame = None
        self.depth_image = None
        self.stat        = False #False means device closed
        self.signal      = False #dont capture for now
        self.depth_mutex = Lock()
        self.signal_mutex= Lock()
        #self.color_mutex = Lock()
        self.xyz_matrix  = self.__xyz_matrix()
        self.uv_matrix   = self.__uv_matrix()
        self.point_xyz   = []
        self.point_uv    = []
        self.color_map   = []

    def __xyz_matrix(self):

        fx = 594.21
        fy = 591.04
        a = -0.0030711
        b = 3.3309495
        cx = 339.5
        cy = 242.7
        mat = np.array([[1/fx, 0, 0, -cx/fx],
                        [0, -1/fy, 0, cy/fy],
                        [0,   0, 0,    -1],
                        [0, 0, a, b]])
        return mat

    def __uv_matrix(self):
     
        rot = np.array([[ 9.99846e-01,   -1.26353e-03,   1.74872e-02], 
                        [-1.4779096e-03, -9.999238e-01,  1.225138e-02],
                        [1.747042e-02,   -1.227534e-02,  -9.99772e-01]])


        trans = np.array([[1.9985e-02, -7.44237e-04,-1.0916736e-02]])
        m = np.hstack((rot, -trans.transpose()))
        m = np.vstack((m, np.array([[0,0,0,1]])))
        KK = np.array([[529.2, 0, 329, 0],
                        [0, 525.6, 267.5, 0],
                        [0, 0, 0, 1],
                        [0, 0, 1, 0]])
        m = np.dot(KK, (m))
        return m

    def shootframe(self):
        self.signal_mutex.acquire()
        self.signal = True
        self.signal_mutex.release()

    def process_frame(self,visualize):

        if(visualize):
            cv2.namedWindow('RGB')
            cv2.namedWindow('depth')
            

        while(self.stat):

            if(visualize):
                
                self.depth_mutex.acquire()
                tmp_frame = self.color_frame
                tmp_depth = self.depth_image
                self.depth_mutex.release()
            
                if(tmp_frame is not None):
                    if tmp_frame.shape[0] != 480:
                        print("wrong depth frame")
                        continue
                    if tmp_frame.shape[1] != 640:
                        print("wrong depth frame")
                        continue
	                
                    cv2.imshow('RGB',tmp_frame)
                    cv2.imshow('depth',tmp_depth)

                    
                    __input__ = cv2.waitKey(10)
                    #27
                    if(__input__ == 1048603):
                        self.shut_down()
                    #115    
                    elif(__input__ == 1048691):
                        self.shootframe()
                        print("frame shooted, we have %d frames now!"%(len(self.point_xyz)+1))
                

            if(self.signal):
	        	
	            self.depth_mutex.acquire()
	            tmp_depth = self.depth_frame
	            self.depth_mutex.release()
				
	            self.signal_mutex.acquire()
	            self.signal = False
	            self.signal_mutex.release()
		
	            u,v = np.mgrid[:480,:640]
		        # Build a 3xN matrix of the d,u,v data
	            C = np.vstack((u.flatten(), v.flatten(), tmp_depth.flatten(), 0*u.flatten()+1))
		        
		        # Project the duv matrix into xyz using xyz_matrix()
	            X,Y,Z,W = np.dot(self.xyz_matrix,C)
	            X,Y,Z = X/W, Y/W, Z/W
	            xyz = 1000 * np.vstack((X,Y,Z)).transpose()
	            self.point_xyz.append(xyz[Z<0,:])

		        # Project the duv matrix into U,V rgb coordinates using rgb_matrix() and xyz_matrix()
	            U,V,_,W = np.dot(np.dot(self.uv_matrix, self.xyz_matrix),C)
	            U,V = U/W, V/W
	            uv = np.vstack((U,V)).transpose()    
	            self.point_uv.append(uv[Z<0,:])

	            self.color_map.append(tmp_frame)
		            
        if(visualize):
        	print("quiting...")
        	cv2.destroyAllWindows()

        return 0

    def depth_hook(self, dev, data, timestamp):
        self.depth_mutex.acquire()
        
        self.depth_frame = data.astype(np.float32)
        np.clip(data, 0, 2**10 - 1, data)
        data >>= 2
        self.depth_image = data.astype(np.uint8)
        
        self.depth_mutex.release()

    def rgb_hook(self, dev, data, timestamp):
        #no lock for now
        #self.depth_mutex.acquire()
        data = data[:, :, ::-1]
        self.color_frame = data.astype(np.uint8)
        #self.depth_mutex.release()

    def body_hook(self,*args):
        if not self.stat:
            raise freenect.Kill 
        
    def start_captioning(self,visualize = False,occupy_main_thread = False):
        self.stat = True
        device_thread = Thread(target = freenect.runloop,\
                               args = (self.depth_hook,self.rgb_hook,self.body_hook),name='device_thread')

        data_thread   = Thread(target = self.process_frame,args = (visualize,),name ='data_thread')

        device_thread.start()
        data_thread.start()

        if(occupy_main_thread):
           device_thread.join()
           data_thread.join()
        

    def shut_down(self):
        self.stat = False

if __name__ == '__main__':
    
    
    dev = kinector()

    dev.start_captioning(visualize=True,occupy_main_thread = True)
    
    #time.sleep(30)
    #dev.shootframe()
    time.sleep(3)
    np.save('/home/matt/Project/Smart/Sensor/scaned_object_data/new_scan_data/xyz',dev.point_xyz)
    np.save('/home/matt/Project/Smart/Sensor/scaned_object_data/new_scan_data/uv',dev.point_uv)
    np.save('/home/matt/Project/Smart/Sensor/scaned_object_data/new_scan_data/color',dev.color_map)
    print('ending...')





