from libSmart.Coordinator.AgentsDev import devAgent
import time
class coordinator_base(object):
	"""docstring for coordinator"""
	def __init__(self):
		super(coordinator_base, self).__init__()
		self.dev_list = []
		self.state_dict = {}
		self.command_dict = {}

	def register_dev(self,dev_c):
		assert issubclass(type(dev_c),devAgent)
		self.dev_list.append(dev_c)
	
		if len(set(self.state_dict.keys()) & set(dev_c.state_dict.keys())) is not 0:
			raise KeyError('Wrong state keys for device')
		else:
			self.state_dict.update(dev_c.state_dict)

		if len(set(self.command_dict.keys()) & set(dev_c.command_dict.keys())) is not 0:
			raise KeyError('Wrong command keys for device')
		else:
			self.command_dict.update(dev_c.command_dict)

	def notify_all_devs(self):
		for dev in self.dev_list:
			dev.notify(self.command_dict)

	def check_all_dev(self):
		for dev in self.dev_list:
			dev.check(self.state_dict)

	def state_solving(self):
		raise ValueError('Please implement your state machine')

	def run(self):
		raise ValueError('Please implement your run loop')
	

class coordinator(coordinator_base):

	def __init__(self):
		super(coordinator,self).__init__()

	def state_solving(self):
		for item in self.command_dict.keys():
			self.command_dict[item] = False

		if not (self.state_dict['camera_ready'] and self.state_dict['robot_ready']):
			raise ValueError('device not ready')

		if self.state_dict['picture_took'] and (not self.state_dict['robot_moving']):
			self.command_dict['robot_move'] = True

		if self.state_dict['robot_moving']:
			self.command_dict['camera_waitpic'] = True

		if (not self.state_dict['robot_moving']) and (not self.state_dict['picture_took']):
			self.command_dict['camera_shoot'] = True

		if self.state_dict['robot_end'] and (not self.state_dict['graph_end']):
			self.command_dict['graph_run'] = True

		if self.state_dict['graph_end']:
			self.command_dict['camera_stop'] = True
			self.command_dict['robot_stop']  = True
			
 


	def run(self):

		self.command_dict['camera_start'] =  True
		self.command_dict['robot_start']  =  True
		self.command_dict['graph_start']  =  True
		self.notify_all_devs()
		#Tracer()()
		while(True):
			self.check_all_dev()
			
			self.state_solving()
			
			self.notify_all_devs()

			time.sleep(0.08)

			if self.command_dict['camera_stop']:
				break


			
if __name__ == '__main__':

	from libSmart.Coordinator.AgentsDev import cameraAgent, robotAgent, graphAgent
	from libSmart.Robot.robot import Robot
	from libSmart.Sensor.kinect import Kinector
	from libSmart.DataFlow.AgentsData import cameraData, robotData
	from libSmart.DataFlow.datacenter import Nodes
	from libSmart.DataFlow.dataGraphs import PreprocessorGraph
	from libSmart.DataFlow.dataProcessor.config import Jointlists3
	from IPython.core.debugger import Tracer
	
	#Tracer()()
	cA = cameraAgent(Kinector())
	rA = robotAgent(Robot())

	nodes = Nodes()

	cameraDataBlock = cameraData().linkAgent(cA)
	robotDataBlock  = robotData().linkAgent(rA)
	nodes.create('camera').register_dev_data(cameraDataBlock)
	nodes.create('joint',Jointlists3).register_dev_data(robotDataBlock)

	ProcG = PreprocessorGraph(nodes)
	ProcG.register_input_nodes('camera')
	ProcG.register_output_nodes('joint')

	gA = graphAgent(ProcG)


	manager = coordinator()
	manager.register_dev(cA)	
	manager.register_dev(rA)
	manager.register_dev(gA)
	manager.run()
	
	nodes['pointcloud_0'].save()
	nodes['pointcloud_1'].save()
	nodes['pointcloud_2'].save()
	nodes['pointcloud_3'].save() 
