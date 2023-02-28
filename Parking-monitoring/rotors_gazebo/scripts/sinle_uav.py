#!/usr/bin/python3.8

import rospy
from geometry_msgs.msg import PoseStamped


def single_uav_publisher():
    rospy.init_node('single_uav_publisher', anonymous=True)

    path_publisher = rospy.Publisher('/ardrone_1/command/pose', PoseStamped, queue_size=10)

    rate = rospy.Rate(0.5)

    pos = [[1.0, 1.0], [-1.0, 1.0], [-1.0, -1.0], [1.0, -1.0]]

    while not rospy.is_shutdown():
        fly = PoseStamped()
        fly.header.seq = 0
        fly.header.stamp.secs = 0
        fly.header.stamp.nsecs = 0
        fly.header.frame_id = ''
        fly.pose.orientation.x = 0.0
        fly.pose.orientation.y = 0.0
        fly.pose.orientation.z = 0.0
        fly.pose.orientation.w = 0.0
        fly.pose.position.z = 1.0
        for element in pos:
            fly.pose.position.x = element[0]
            fly.pose.position.y = element[1]
            path_publisher.publish(fly)
            rospy.loginfo('ardrone_1 flying to {0} {1} {2}'.format(fly.pose.position.x,
                                                                   fly.pose.position.y,
                                                                   1))
            rate.sleep()


if __name__ == '__main__':
    try:
        single_uav_publisher()
    except rospy.ROSInterruptException:
        pass
