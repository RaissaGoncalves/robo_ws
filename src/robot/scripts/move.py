#!/usr/bin/env python3
import rospy
import math
import time
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

# Variáveis globais para armazenar a posição atual
a = 0.0
b = 0.0

# Callback para atualizar a posição da tartaruga
def poseCallback(pose_message):
    global a, b
    a = pose_message.x
    b = pose_message.y

# Função para mover a tartaruga
def move(speed, angle):
    velocity_message = Twist()
    global a, b
    x0 = a
    y0 = b
    velocity_message.linear.x = speed
    velocity_message.angular.z = angle
    distancia = 0.0
    loop_rate = rospy.Rate(10)

    while True:
        rospy.loginfo("Movendo...")
        velocity_publisher.publish(velocity_message)
        loop_rate.sleep()
        distancia += 0.1 * math.sqrt(((a - x0) ** 2) + ((b - y0) ** 2))
        print(distancia)

# Função principal
if __name__ == '__main__':
    try:
        rospy.init_node('turtlesim_moves', anonymous=True)

        # Tópico para enviar velocidades
        cmd_vel_topic = '/turtle1/cmd_vel'
        velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

        # Tópico para obter a posição da tartaruga
        position_topic = '/turtle1/pose'
        pose_subscriber = rospy.Subscriber(position_topic, Pose, poseCallback)

        time.sleep(2)  # Aguarda o sistema inicializar
        move(1.0, 3.0)

    except rospy.ROSInterruptException:
        pass

