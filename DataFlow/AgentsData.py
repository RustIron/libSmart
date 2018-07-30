import copy

class DevData(object):

	def __init__(self):
		self.agent = None

	def linkAgent(self,agent):
		self.agent = agent
		return self

	def get(self):
		raise ValueError('Please implement your data getting function')

	def set(self,data):
		raise ValueError('Please implement your data setting function')


class cameraData(DevData):
	"""docstring for cameraData"""
	def __init__(self):
		super(cameraData, self).__init__()
	
	def get(self):

		return [copy.deepcopy(self.agent.dev.point_xyz),\
				copy.deepcopy(self.agent.dev.color_map),\
				copy.deepcopy(self.agent.dev.point_uv)]

	def set(self,data):
		print('not allowed to set cameraData')


class robotData(DevData):

	def __init__(self):
		super(robotData,self).__init__()

	def get(self):
		print('no need to get robot data for now')

	def set(self,data):
		self.agent.joint_lists = copy.deepcopy(data)