import numpy as np
from sklearn.neighbors import NearestNeighbors
from kinect2robot import robotKineticSolve
from config import distorb_function_list, Jointlists3, board_bounding_box, min_point_before_moving
from matplotlib.colors import rgb_to_hsv
from ptool import showpoints,showcolorpoints

class PointCloud(object):
	"""docstring for PointCloud"""
	def __init__(self,pts,color = None,uv = None):
		super(PointCloud, self).__init__()
		assert pts.shape[1] == 3
		self.pts    = pts
		if uv is not None:
			self.color =  self.color_mapping(uv,color)
		else:
			self.color = color

	def filter(self,keep_list):
		self.pts = self.pts[keep_list]
		if self.color is not None:
			self.color = self.color[keep_list]

	def trans(self,T_mat):
		assert T_mat.shape[0] == 4
		R_m = T_mat[:3,:3]
		t_m = T_mat[:3,3:]
		self.pts = (R_m.dot(self.pts.T) + t_m).T

	def copy(self):
		return PointCloud(np.copy(self.pts),np.copy(self.color))

	def color_mapping(self,uv,color):

	    uvs    = np.round(uv).astype(np.int32)
	    uvs[:,0] = uvs[:,0] + 48
	    uvs[uvs[:,0]>479,0] = 479

	    uvs[:,1] = uvs[:,1] - 13
	    uvs[uvs[:,1]>639,1] = 639

	    colormap = color[uvs[:,0],uvs[:,1]]
	    colormap[:,[0,2]] = colormap[:,[2,0]]
	    return colormap	

	def __add__(self,other):
		assert type(other) == PointCloud

		if self.color is None:
			return PointCloud(np.vstack([self.pts,other.pts]))

		else:
			return PointCloud(np.vstack([self.pts,other.pts]),\
						      np.vstack([self.color,other.color]))

	def show(self):
		if self.color is not None:
			showcolorpoints(self.pts,self.color)
		else:
			showpoints(self.pts)

	def save(self,name):
		np.save(name,[self.pts,self.color])


class Pose(object):

	def __init__(self,pose):
		self.name = pose
		self.value = [float(item) for item in pose.split(',')]
		self.transmat = robotKineticSolve(self.value)
		
		self.bbox = board_bounding_box[Jointlists3.index(self.name)]
		self.moving = min_point_before_moving[Jointlists3.index(self.name)]
		self.distorb = distorb_function_list[Jointlists3.index(self.name)]
		


class PointProc(object):
	"""docstring for Preprocessor"""
	def __init__(self):
		super(PointProc, self).__init__()

	def load_data(self,pc):
		assert type(pc) == PointCloud
		self.pointcloud = pc.copy()
		return self


	def box_filter(self,b_box):

		[[x_min,x_max],[y_min,y_max],[z_min,z_max]] = b_box
		p = self.pointcloud.pts.T

		if(x_max is not None):
			keep_x_min = p[0,:] > x_min
			keep_x_max = p[0,:] < x_max
			keep_x = np.logical_and(keep_x_min,keep_x_max)
		else:
			keep_x = p[0,:] < 1000000

		if(y_max is not None):
			keep_y_min = p[1,:] > y_min
			keep_y_max = p[1,:] < y_max
			keep_y = np.logical_and(keep_y_min,keep_y_max)
		else:
			keep_y = p[1,:] < 1000000

		if(z_min is not None):
			keep_z_min = p[2,:] > z_min
			keep_z_max = p[2,:] < z_max
			keep_z = np.logical_and(keep_z_min,keep_z_max)
		else:
			keep_z = p[2,:] < 1000000

		return  np.logical_and(keep_x,np.logical_and(keep_y,keep_z))

	def color_filter(self,thresh):

	    [a,b] = thresh
	    hsv_t = rgb_to_hsv(self.pointcloud.color)
	    keep_1 = hsv_t[:,2] > a 
	    keep_2 = hsv_t[:,2] < b
	    keep   = np.logical_and(keep_1,keep_2)
	    return keep

	def pc_cluster(self,k_neighbor = 50,dis_thresh = 10):

	    pc_tmp = self.pointcloud.pts
	    neigh = NearestNeighbors(n_neighbors=k_neighbor)
	    neigh.fit(pc_tmp)
	    distances, indices = neigh.kneighbors(pc_tmp, return_distance=True)

	    cluster_container = []
	    using_list        = np.ones(pc_tmp.shape[0])
	    while using_list.any():
	    	current_cluster   = []
	    	tmp_cluster       = []
	    	pick = using_list.nonzero()[0][0]
	    	tmp_cluster.append(pick)
	    	using_list[pick]  = 0

	    	while len(tmp_cluster) is not 0:
	        	c_p     = tmp_cluster.pop()
	        	current_cluster.append(c_p)
	        	neibors = indices[c_p]
	        	d_s     = distances[c_p]

	        	for i in range(k_neighbor):
	        		nei     = neibors[i]
	        		dis     = d_s[i]
	        		if using_list[nei] == 1 and d_s[i] < dis_thresh: 	
	        			tmp_cluster.append(nei)
	        			using_list[nei] = 0

	    	cluster_container.append(current_cluster)

	    return cluster_container

	def outlier_filter(self):
		cluster_container = self.pc_cluster()
		keep = cluster_container[0]
		for cluster in cluster_container:	
			if(len(cluster) > len(keep)):
				keep = cluster
		return keep

	def default_process_cascade(self):
		keep_1   = self.box_filter([[-1500,-350],[-500,500],[None,None]])
		self.pointcloud.filter(keep_1)
		"""the scene data filtered out"""
		scene = self.pointcloud.copy()

		keep_2   = self.color_filter([200,255])
		self.pointcloud.filter(keep_2)
		keep_3   = self.outlier_filter()
		self.pointcloud.filter(keep_3)

		bb_box_min   = [[self.pointcloud.pts[:,0].min() - 20, self.pointcloud.pts[:,0].max() + 20],\
						[self.pointcloud.pts[:,1].min() - 20, self.pointcloud.pts[:,1].max() + 20],\
						[self.pointcloud.pts[:,2].min() - 5, 1e6]]

		

		self.load_data(scene)
		keep  = self.box_filter(bb_box_min)
		self.pointcloud.filter(keep)
		#print(bb_box_min)
		#keep  = self.outlier_filter()
		#self.pointcloud.filter(keep)

		# return scene, board
		return scene,self.pointcloud


	def fixed_tuned_process_cascaded(self,bbox,min_p_before_move,distorb_function):
		'''
		bbox is generated by run default process cascade bb_box_min
		'''

		self.pointcloud.pts = self.pointcloud.pts - min_p_before_move
		self.pointcloud.pts   = distorb_function(self.pointcloud.pts)

		keep = self.box_filter(bbox)
		self.pointcloud.filter(keep)

		#bbox = self.box_filter([[50,250],[50,250],[None,None]])


		return self.pointcloud
