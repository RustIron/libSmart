from libSmart.Coordinator.AgentsDev import cameraAgent, robotAgent, graphAgent
from libSmart.Coordinator.Coordinator import coordinator
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
#Tracer()()
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

pc_scanned = nodes['pointcloud_0'].data +\
			 nodes['pointcloud_1'].data +\
			 nodes['pointcloud_2'].data +\
			 nodes['pointcloud_3'].data 

pc_scanned.show()
pc_scanned.save('./Data/scannedData/plier/plier21')
'''
nodes['pointcloud_0'].save()
nodes['pointcloud_1'].save()
nodes['pointcloud_2'].save()
nodes['pointcloud_3'].save() 
'''