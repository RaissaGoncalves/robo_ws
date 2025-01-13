#!/usr/bin/env python3
import rospy
import math
import time
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

x1, y1, theta1 = 0.0, 0.0, 0.0
x2, y2, theta2 = 0.0, 0.0, 0.0
x = 0
y = 0
theta = 0

def poseCallback1(pose_message):
    global x1, y1, theta1
    x1 = pose_message.x
    y1 = pose_message.y
    theta1 = pose_message.theta

def poseCallback2(pose_message):
    global x2, y2, theta2
    x2 = pose_message.x
    y2 = pose_message.y
    theta2 = pose_message.theta

def move():
    velocity_message = Twist()
    global x1, y1, x2, y2, theta1, theta2
    loop_rate = rospy.Rate(10)

    cmd_vel_topic2 = '/turtle2/cmd_vel'
    velocity2_publisher = rospy.Publisher(cmd_vel_topic2, Twist, queue_size=10)

    while True:
        rospy.loginfo("Movendo")
        velocity2_publisher.publish(velocity_message)
        loop_rate.sleep()
        ErroDist = abs(math.sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2)))
        angle = math.atan2((y1 - y2), (x1 - x2))
        if y1 > y2 and angle < 0:
            angle = math.pi + angle
        elif y1 < y2 and angle > 0:
            angle = angle - math.pi

        ErroTheta = (theta2 - angle)
        if ErroDist > 0.1:
            velocity_message.linear.x = 0.8 * ErroDist
        else:
            velocity_message.linear.x = 0
        if (theta2 - angle) > ((math.pi - theta2) + (math.pi - -angle)):
            velocity_message.angular.z = 1 * ErroTheta
        elif (theta2 - angle) < ((math.pi - theta2) + (math.pi - angle)):
            velocity_message.angular.z = -1 * ErroTheta
        print(theta2)
        print(angle)
        print(ErroDist)
        print(ErroTheta)

if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_moves', anonymous=True)
        cmd_vel_topic2 = '/turtle2/cmd_vel'
        velocity2_publisher = rospy.Publisher(cmd_vel_topic2, Twist, queue_size=10)
        position1_topic = '/turtle1/pose'
        position2_topic = '/turtle2/pose'
        position1_subscriber = rospy.Subscriber(position1_topic, Pose, poseCallback1)
        position2_subscriber = rospy.Subscriber(position2_topic, Pose, poseCallback2) 
        time.sleep(2)
        move()

    except rospy.ROSInterruptException:
        pass

