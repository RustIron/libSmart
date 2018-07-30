import numpy as np
from libSmart.DataFlow.dataProcessor.preprocessor import Pose,PointCloud, PointProc
from libSmart.DataFlow.dataProcessor.config import distorb_function_list, Jointlists3, board_bounding_box, min_point_before_moving
from IPython.core.debugger import Tracer
pcs_l  = [] # the list to put more point cloud together

for idx in [0,1,2,3]:

	p = np.load('pointcloud_%d.npy'%idx) # load from stored data, collected by "collect_raw_point_cloud.py"
	pc = PointCloud(p[0],p[1])     
	pose = Pose(Jointlists3[idx])        
	pc.trans(pose.transmat)              # transform the point cloud to robot base coordinating system
	#pc.show()

	''' fixed process cascade '''
	PProc = PointProc()
	PProc.load_data(pc)

	bbox = board_bounding_box[idx]
	distorb_function = distorb_function_list[idx]
	min_p_before_move = min_point_before_moving[idx]

	pc = PProc.fixed_tuned_process_cascaded(bbox,min_p_before_move,distorb_function)
	print(pc.pts.min(axis = 0))
	print(pc.pts.max(axis = 0))
		

#	pc.show()

	pcs_l.append(pc)
#pcs = pcs_l[2]
pcs = pcs_l[0] + pcs_l[1] + pcs_l[2] + pcs_l[3]
pcs.show()
#pcs.save("./box1")