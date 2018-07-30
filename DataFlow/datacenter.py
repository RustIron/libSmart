import cPickle

class Datacenter(object):
	"""docstring for Datacenter"""
	def __init__(self):
		super(Datacenter, self).__init__()
		self.datagraphs = {}
	
	def register_datagraph(self,datagraph,name):
		assert type(datagraph) is Datagraph
		assert type(name) is str
		assert len(self.datagraphs.keys()&{name}) is 0
		self.datagraphs[name] = datagraph

	def inference_datagraph(self,name):
		self.datagraphs[name].inference()


	def inference_all_datagraph(self):
		for itm in self.datagraphs.keys():
			self.inference_datagraph(itm)


class Datagraph(object):
	"""docstring for Datagraph"""
	def __init__(self,nodes):
		super(Datagraph, self).__init__()
		self.nodes       = nodes
		self.input_nodes = []
		self.output_nodes= []
		

	def Graphinit(self):
		pass

	def Graphrun(self):
		pass

	def synchronize_input_nodes(self):
		for node in self.input_nodes:
			self.nodes[node].synchronize_dev_to_node()

	def synchronize_output_nodes(self):
		for node in self.output_nodes:
			self.nodes[node].synchronize_node_to_dev()

	def register_input_nodes(self,node):

		if node not in self.nodes.keys():
			raise KeyError("unable to register undefined node")

		self.input_nodes.append(node)
		return self

	def register_output_nodes(self,node):

		if node not in self.nodes.keys():
			raise KeyError("unable to register undefined node")

		self.output_nodes.append(node)
		return self


class __Node__(object):
	
	def __init__(self,name,data = None):
		self.data     = data
		self.name     = name
		self.dev_data = None

	def register_dev_data(self,dev_data):
		self.dev_data = dev_data
		return self

	def synchronize_dev_to_node(self):
		self.data = self.dev_data.get()
		return self

	def synchronize_node_to_dev(self):
		self.dev_data.set(self.data)
		return self

	def save(self):
		self.data.save(self.name)

class Nodes(dict):

	def __init__(self):
		self.nodes_dict = {}

	def create(self,name,data = None):
		if name in self.nodes_dict.keys():
			raise KeyError('name occupied')
		else:
			self.nodes_dict[name] = __Node__(name,data)
			return self.nodes_dict[name]

	def __getitem__(self,key):
		return self.nodes_dict[key]

	def __setitem__(self,key):
		return self.nodes_dict[key]

	def __iter__(self):
		return iter(self.nodes_dict)

	def __len__(self):
		return len(self.nodes_dict)

	def __str__(self):
		return str(self.nodes_dict)

	def keys(self):
		return self.nodes_dict.keys()





if __name__ == '__main__':

	from libSmart.Coordinator.Agents import robotAgent,cameraAgent
	from AgentsData import cameraData, robotData
	from IPython.core.debugger import Tracer
	rA = robotAgent()
	cameradata = cameraData().linkAgent(cameraAgent())
	robotdata  = robotData().linkAgent(rA)


	cameraNode = Node().register_dev_data(cameradata)
	robotNode  = Node(["10,5,0,30,0,0","0,0,0,0,0,0","-10,-5,0,-30,0,0"]).register_dev_data(robotdata)

	robotNode.synchronize_node_to_dev()
	