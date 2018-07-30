import socket
import subprocess
import time
from threading import Thread
from IPython.core.debugger import Tracer


class robotstatus(object):
	def __init__(self):
		super(robotstatus,self).__init__()
		self.power         = False #false for off
		self.running       = False #servo motor running
		self.moving        = False
		#self.pause         = False
		self.connected     = False #false for not connected
		self.log           = ''
		self.REPEAT_mode   = False
		self.monitor_speed = ''    #in percentage
		self.program_speed = ''	   #in percentage
		self.accu          = '1'   #in mm
		self.error         = False #False means no error
		self.TEACH_MOD     = False

	def dump(self):
		#TODO: make it work
		with open('log.txt','w') as f:
			f.write(self.log)

	def addlog(self,current_log):
		self.log += current_log


	def checkBefore_movejoints(self):
		if (self.power and not self.running and self.connected and self.REPEAT_mode and not self.error):

			return True

		return False
		

	def checkBefore_establish_connection(self):
		if (self.power and not self.connected):

			return True

		return False

	def checkBefore_kill_connection(self):
		if (not self.running):

			return True

		return False

class Robot(object):
	"""docstring for Robot"""
	def __init__(self):
		super(Robot, self).__init__()
		self.r_status = robotstatus()
		
	def establish_connection(self):

		self.process  = subprocess.Popen('plink -telnet 192.168.0.110',bufsize = -1, shell=True,stdout = subprocess.PIPE,stdin = subprocess.PIPE,stderr=subprocess.PIPE)
		time.sleep(5)
		
		
		try: 
			connectionlog = self.__get_interaction__(': ')
			self.r_status.addlog(connectionlog)
			if ("login" in connectionlog):
				self.process.stdin.write('as\n\n'.encode()) #should i include login: ?
				self.r_status.connected = True
				print('robot is connected')
				self.r_status.addlog(self.__check_status__())
			elif ("ERROR" in connectionlog):
				print('Robot is not ready, check AC primary power is not on')

		except:
			self.kill_connection()



	def kill_connection(self):

		self.r_status.addlog(self.__check_status__())
		self.process.kill()
		self.r_status.dump()
		print('robot is disconnected by kill_connection')
	
	"""
	def move_joints(self,joint_list,sleep_time):
		#Tracer()()
		self.r_status.addlog(self.__check_status__())
		if(not self.r_status.checkBefore_movejoints()):
			print('robot is not ready to move, robot needs power on, no error, connection and in repeat mode in order to be ready')
		else:
			try:	
				# fill in with more cases
				
				##TODO: check is joint list is in standard form
				
				for joint in joint_list:
					self.r_status.running = True
					self.__movejoint__(joint)
					self.r_status.running = False
					time.sleep(sleep_time)

				self.r_status.motion_end  = True
			except:
				self.kill_connection()
	"""

	def __get_interaction__(self,ending_code):

		log = ''
		out = self.process.stdout.read(1).decode('utf-8')
		while out != '' and self.process.poll() == None:
			log += out
			if(ending_code in log):
				break
			self.process.stdout.flush()
			out =  self.process.stdout.read(1).decode('utf-8')
		self.process.stdout.flush()
		
		return log

	def __movejoint__(self,joint):

		self.r_status.moving = True	
		self.r_status.addlog(self.__check_status__())
		if(not self.r_status.checkBefore_movejoints()):
			print('robot is not ready to move, robot needs power on, no error, connection and in repeat mode in order to be ready')
		else:
			try:
				command = "execute movejt\n"

				self.process.stdin.write(command.encode())
				self.process.stdin.flush()
				self.process.stdin.write(" ".encode())
				self.process.stdin.flush()

				current_log = self.__get_interaction__('enter joint angle:')
				self.r_status.addlog(current_log)
				

				if("enter joint angle:" in current_log):
					self.process.stdin.write(joint.encode())
					self.process.stdin.flush()
					self.process.stdin.write("\n".encode())
					self.process.stdin.flush()
					self.process.stdin.write(" ".encode())
					self.process.stdin.flush()

				current_log = self.__get_interaction__('Program completed.')
				self.r_status.addlog(current_log)

				self.r_status.moving = False
			except:
				self.kill_connection()

	def movejoint(self,joint):

		t = Thread(target = self.__movejoint__,args = (joint,))
		t.start()


	def __check_status__(self):

		if(not self.r_status.connected):
			print('not connected, wrong call to check_status')

		command = "status"
		self.process.stdin.write("status\n\n".encode())
		self.process.stdin.flush()

		status =  self.__get_interaction__('Execution') 
		status += self.__get_interaction__('>')


		if ("Motor power OFF") in status:
			self.r_status.power  = False

		elif ("Motor power OFF") not in status:
			self.r_status.power  = True

		if ("During error condition") in status: 
			self.r_status.error = True

		elif ("During error condition")  not in status: 
			self.r_status.error = False

		if ("TEACH MODE") in status:
			self.r_status.TEACH_MODE = True

		elif("REPEAT mode") in status:
			self.r_status.REPEAT_mode = True

		if ("Now moving program") in status:
			self.r_status.running = True


		return status


if __name__ == '__main__':
	rb = Robot()
	rb.establish_connection()

	rb.move_joints(["0,0,0,0,0,0","10,5,0,30,0,0","-10,-5,0,-30,0,0"],1) #stop time 5 sec
	#rb.check_status()
	rb.kill_connection()
