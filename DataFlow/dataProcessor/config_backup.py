board_bounding_box = [[[-1500, -500], [-500, 500], [-576, 500.0]],\
					  [[-1174, -847], [-207, 147], [-608, 500.0]],\
					  [[-1027, -678], [-163, 149], [-741, 500.0]],\
					  [[-978, -636], [-207, 143], [-791, 500.0]],\
					  [[-1211, -857], [-284, 65], [-599, 500.0]]]

min_point_before_moving = [[-1234.62914799,  -118.72451451,  -565.66171255],\
								[-1166.71299277,  -179.98497283,  -593.2747267 ],\
								[-1007.21775927,  -162.86766742,  -695.9285123 ],\
								[-963.49076081,   -187.70523461,  -775.57315116],\
								[-1187.76622161,  -264.64364306,  -583.70879895]]

def distorb0(points):

	points[:,0] = (points[:,0] - 0.1  * points[:,1] - 0.18 * points[:,2])*1.015
	points[:,1] = points[:,1]  - 0.1  * points[:,2]
	points[:,2] = 0.867*(points[:,2] - 0.05 * points[:,0])
	#points = points - points.min(axis = 0)

	return points

def distorb1(points):

	points[:,0] = (points[:,0] - 0.11 * points[:,2]- 0.03 * points[:,1]) * 1.026
	points[:,1] = (points[:,1] + 0.05 * points[:,0]- 0.2 * points[:,2]) * 1.0168
	points[:,2] = points[:,2] * 0.875
	#points = points - points.min(axis = 0)
	return points

def distorb2(points):
	
	points[:,0] = (points[:,0]  - 0.05 * points[:,1] + 0.01 *points[:,2]) *  0.976
	points[:,1] = (points[:,1]  - 0.06 * points[:,1] - 0.05  * points[:,2]) *1.1023
	points[:,2] = (points[:,2]  + 0.14 * points[:,1]) * 0.82 

	#points = points - points.min(axis = 0)
	return points

def distorb3(points):
	points[:,0] = (points[:,0] - 0.1 *  points[:,1]  +  0.05 * points[:,2]) * 0.9831
	points[:,1] = (points[:,1] - 0.1 * points[:,2]) * 1.049263 
	points[:,2] = (points[:,2] + 0.03 * points[:,1]- 0.15 * points [:,0]) * 0.7619
	#points = points - points.min(axis = 0)
	return points


def distorb4(points):
	points[:,0] = (points[:,0] - 0.20 *points[:,2] ) * 0.989
	points[:,1] = (points[:,1] - 0.15 * points [:,2]) * 1.018 
	points[:,2] = (points[:,2] - 0.05 * points[:,0]) * 0.853
	#points = points - points.min(axis = 0)
	return points

distorb_function_list = [distorb0,distorb1,distorb2,distorb3,distorb4]

Jointlists = ["-54.259,48.396,-73.360,116.643,0,0",\
				"-79.785,60.523,-45.213,89.762,0,0",\
   				"-132.513,67.412,-61.807,44.201,0,0",\
   				"-159.362,-28.596,-132.738,40.801,0,0",\
   				"-87.73,22.19,-68.21,86.53,0,0"]

Jointlists2 = ["-65,42,-82,78,10,123",\
			   "-83,41,-72,1,-12,177",\
			   "-103,45,-70,1,-12,177",\
			   "-120,49,-61,3,-18,158",
			   "0,0,0,0,0,0",\
			   "0,-30,-60,0,30,0",\
			   "-20,-40,-90,0,50,-20"]
#for scanning inside the blue tape area
Jointlists3 = ["-47.858,43.936,-78.542,-130.216,-11.372,-18.89",\
			   "-87.449,70.578,-19.635,-173.968,21.964,-14.013",\
			   "-123.609,44.375,-67.215,-181.781,1.13,-35.786",\
			   "-87.859,-16.706,-142.57,-173.117,-61.720,-3.253"]