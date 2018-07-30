from Processor.kinect2robot import mat_trans_cam_points_to_robot
from Processor.ptool import showcolorpoints,showpoints
import numpy as np
from Processor.preprocessor import PointCloud, Preprocessor
import sys
from IPython.core.debugger import Tracer

#data_path = './data/standard_drill'
#data_path = '/home/matt/Project/Smart/Sensor/scaned_object_data/drill_with_compensate'
#data_path = '/home/matt/Project/Smart/Sensor/scaned_object_data/wood_box_compensate'
#data_path = '/home/matt/Project/Smart/Sensor/scaned_object_data/wood_piece'
data_path = sys.argv[1]

joint_list = [[-54.259, 48.396, -73.36, 116.643],\
		  [-79.785, 60.523, -45.213, 89.762],\
          [-132.513, 67.412, -61.807, 44.201],\
		  [-159.362, -28.596, -132.738, 40.801],\
          [-87.73, 22.19, -68.21, 86.53]]

p_data     = np.load('%sxyz.npy'%data_path)
c_data     = np.load('%scolor.npy'%data_path)
uv_data    = np.load('%suv.npy'%data_path)

align_list =[]
color_list = []

obj_list = []
objc_list = []

processor = Preprocessor()

for idx in [0,1,2,3,4]:
	color  = c_data[idx]
	uv = uv_data[idx]
	pc = p_data[idx] * 1000
	pointcloud = PointCloud(pc,color,uv)
	pointcloud.trans(mat_trans_cam_points_to_robot(joint_list[idx]))
	processor.load_data(pointcloud)
	obj = processor.process_pose_i(idx)
	obj_list.append(obj.pts)
	objc_list.append(obj.color)

showcolorpoints(np.vstack(obj_list),np.vstack(objc_list))

if(len(sys.argv) == 3):
	np.save(sys.argv[2],[np.vstack(obj_list),np.vstack(objc_list)])
