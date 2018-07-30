import time
from IPython.core.debugger import Tracer

class devAgent(object):
	"""docstring for dev"""
	def __init__(self,dev):
		self.dev = dev
		self.command_dict = {}
		self.state_dict   = {}
	
	def check(self,state_dict):
		raise keyError('check function not implemented')

	def notify(self,command_dict):
		raise keyError("notify function not implemented")


class robotAgent(devAgent):

	def __init__(self,dev):
		super(robotAgent, self).__init__(dev)
		#self.dev = Robot()
		self.command_dict = {'robot_start':False,'robot_move':False,'robot_stop':False}
		self.state_dict   = {'robot_ready':False,'robot_moving':False,'robot_end':False}

		self.joint_lists = None
		self.motion_end  = False

	def notify(self,command_dict):
		if(command_dict['robot_start']):
			self.dev.establish_connection()

		if(command_dict['robot_move']):
			if len(self.joint_lists) is not 0:
				joint = self.joint_lists.pop(0)
				self.dev.movejoint(joint)
			else:
				self.motion_end = True

		if(command_dict['robot_stop']):
			self.dev.kill_connection()


	def check(self,state_dict):
		state_dict['robot_ready']    = self.dev.r_status.connected
		state_dict['robot_moving']   = self.dev.r_status.moving
		state_dict['robot_end']      = self.motion_end



class cameraAgent(devAgent):
	"""docstring for cameraAgent"""
	def __init__(self,dev):
		super(cameraAgent, self).__init__(dev)
		#self.dev = kinector()
		self.command_dict = {'camera_start':False,'camera_shoot':False,'camera_waitpic':False,'camera_stop':False}
		self.state_dict   = {'camera_ready':False,'picture_took':False}

		self.picture_took = True

	def notify(self,command_dict):
		
		if(command_dict['camera_start']):	
			self.dev.start_captioning(visualize=True)

		if(command_dict['camera_waitpic']):
			self.picture_took = False

		if(command_dict['camera_shoot']):
			self.dev.shootframe()
			print('picture_took')
			self.picture_took = True
			
		if(command_dict['camera_stop']):
			self.dev.shut_down()

	def check(self,state_dict):
		state_dict['camera_ready']   = self.dev.stat
		state_dict['picture_took']  = self.picture_took




class graphAgent(devAgent):

	def __init__(self,dev):
		super(graphAgent,self).__init__(dev)
		self.command_dict = {'graph_start':False,'graph_run':False}
		self.state_dict   = {'graph_end':False}
		self.inference_finished = False

	def notify(self,command_dict):

		if(command_dict['graph_start']):
			self.dev.synchronize_output_nodes()
			self.dev.Graphinit()

		if(command_dict['graph_run']):
			self.dev.synchronize_input_nodes()
			self.dev.Graphrun()
			self.inference_finished = True

	def check(self,state_dict):
		state_dict['graph_end'] = self.inference_finished