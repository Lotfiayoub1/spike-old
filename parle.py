#!/usr/bin/env python
import rospy
from std_msgs.msg import String

rospy.init_node('parle', anonymous=True)
rospy.loginfo("parle en remote")


# On publie a behavior_parle
topic_parle = rospy.Publisher('topic_parle', String, queue_size=10)


while True:
	entree = raw_input("Spike dit> ")
	if len(entree) >= 0:
		rospy.loginfo("Je repete: " + entree)
        	topic_parle.publish(entree)

rospy.spin()
