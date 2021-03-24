#!/usr/bin/env python

import rospy
from udm_service.srv import *
from std_msgs.msg import String
import json

def handle_request(request):
	global json_dict
	access_id=request.access_id.data
	state=request.state.data

	if ((access_id == 1 or access_id == 2) and (state == 1 or state == 0)):
		json_dict["access_%d"%(access_id)]=state
		response=change_stateResponse()
		response.res.data=True
	else:
		response=change_stateResponse()
		response.res.data=False
	return response

def simple_server():
	global json_dict
	rospy.init_node("udm_service")
	rospy.Service("udm_service_server" , change_state, handle_request)
	pub=rospy.Publisher("access_state", String,queue_size=10)
	rate=rospy.Rate(15)


	json_dict={
	"access_1":0,
	"access_2":0
	}

	while not rospy.is_shutdown():
		json_msg=json.dumps(json_dict)
		pub.publish(json_msg)
		rate.sleep()

if __name__ == '__main__':
	global json_dict
	simple_server()
