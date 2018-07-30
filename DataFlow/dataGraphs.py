from datacenter import Datagraph
from dataProcessor.preprocessor import PointCloud, PointProc,Pose

class PreprocessorGraph(Datagraph):

	def __init__(self,nodes):
		super(PreprocessorGraph,self).__init__(nodes)


	def Graphinit(self):
		self.processor = PointProc()

	def Graphrun(self):

		pose_num = len(self.nodes['joint'].data)
		for i in range(pose_num):
			self.nodes.create('pose_%d'%i,self.nodes['joint'].data[i])
			self.nodes.create('camera_frame_%d'%i,[self.nodes['camera'].data[0][i],\
										           self.nodes['camera'].data[1][i],\
										           self.nodes['camera'].data[2][i]])

			self.nodes.create('pointcloud_%d'%i,\
				              self.__process_single_frame_pc__(self.nodes['pose_%d'%i],self.nodes['camera_frame_%d'%i]))

		
	def __process_single_frame_pc__(self,pose_node,camera_frame_node):
		
		pose       = Pose(pose_node.data)
		pointcloud = PointCloud(*camera_frame_node.data)
		
		pointcloud.trans(pose.transmat)
		self.processor.load_data(pointcloud)
		pc_processed =self.processor.fixed_tuned_process_cascaded(pose.bbox,pose.moving,pose.distorb)
		
		return pc_processed
		#return pointcloud

if __name__ == '__main__':

	from datacenter import Nodes
	import numpy as np
	from dataProcessor.config import Jointlists2
	import cPickle
	from IPython.core.debugger import Tracer
	#Tracer()()

	nodes = Nodes()

	nodes.create('camera')
	nodes.create('joint')

	with open('camera.nds','r') as f:
		data = cPickle.load(f)

	nodes['camera'].data = data
	nodes['joint'].data  = Jointlists2

	preprocG  = PreprocessorGraph(nodes)

	preprocG.Graphinit()
	preprocG.Graphrun()

	pc = nodes['pointcloud_0'].data +  \
	     nodes['pointcloud_1'].data +  \
	     nodes['pointcloud_2'].data +  \
	     nodes['pointcloud_3'].data +  \
	     nodes['pointcloud_4'].data +  \
	     nodes['pointcloud_5'].data +  \
		 nodes['pointcloud_6'].data 

	pc.show()

	print('process finished')
	