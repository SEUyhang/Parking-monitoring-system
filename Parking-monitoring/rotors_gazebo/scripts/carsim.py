#!/usr/bin/python3.8
import sys
import rospy
import random
import os
import time
from geometry_msgs.msg import Pose
from gazebo_msgs.srv import SpawnModel
from gazebo_msgs.srv import DeleteModel

# parking_spot_number = 4 停车位数量
position_x = [-5.103021,-3.404368,2.479433,2.577461,9.443136,11.383706,10.106677,9.883789,2.557173,4.712056,-4.476666,-4.769073,9.495507,11.570071,2.865197,2.603516,-5.886975,-3.647739] #所有停车点的x坐标
position_y = [6.899674,3.223762,6.964153,3.944118,7.063987,3.430657,-1.222709,-4.037406,-1.193896,-4.320618,-0.979300,-3.494447,-9.141672,-12.707073,-9.772421,-12.356461,-10.107197,-13.073170] #所有停车点的y坐标
car_typelist = ["car_01","car_02","car_03","car_04","car_05","car_06","car_07","car_08","car_09","car_10","car_11","car_12","car_13"] #车辆的款式
model_path = "/home/yhang/rotors_ws/src/rotors_simulator/rotors_simulator/rotors_gazebo/models" #模型的路径
#exist_flag =[1,1,1,0,1,1,1,0,1,0,1,1,0,1,1,0,1,1,0,0] #标志位，第i个停车位有车则为1，没有车则为0
exist_flag =[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] #标志位，第i个停车位有车则为1，没有车则为0

threshold = 0.4 #每次更新当随机数大于0.4时保持当前车位有车，否则让当前停车位空下来
models_file = []
models_content = []

#调用模型生成请求，传入模型的名字(自定义)、款式、初始化的x,y坐标
def add_car(number,x=0.0,y=0.0):
	# ROS节点初始化
    # rospy.init_nfode('carsim')
    # 发现/spawn服务后，创建一个服务客户端，连接名为/gazebo/spawn_sdf_model的service
    # rospy.wait_for_service('/gazebo/spawn_sdf_model')
    try:
        add_car = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
        # 请求服务调用，输入请求数据
        #"model_name: ''
        # model_xml: ''
        # robot_namespace: ''
        # initial_pose:
        #   position: {x: 0.0, y: 0.0, z: 0.0}
        #   orientation: {x: 0.0, y: 0.0, z: 0.0, w: 0.0}
        # reference_frame: ''" 
        
        Model_name='car'+str(number)
        Model_xml = models_content[number%4]
        Robot_namespace = "car"+str(number)
        Initial_pose = Pose()
        Initial_pose.position.x=x
        Initial_pose.position.y=y
        Initial_pose.position.z=0.0
        # Initial_pose.orientation.z=-1.57079632679
        Initial_pose.orientation.z=0
        response = add_car(model_name=Model_name,model_xml=Model_xml,robot_namespace=Robot_namespace,initial_pose=Initial_pose)
        return response
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


#调用删除模型请求，传入要删除的模型的编号(名字)
def delete_car(number):
	# ROS节点初始化
    # rospy.init_node('carsim')

	# 发现/delete服务后，创建一个服务客户端，连接名为/gazebo/delete_model的service
    # rospy.wait_for_service('/gazebo/delete_model')
    try:
        delete_car = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
		# 请求服务调用，输入请求数据 要删除的模型的名字
        #"model_name: ''
        Model_name='car'+str(number)
        response = delete_car(model_name=Model_name)
        return response
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)


if __name__ == "__main__":

    random.seed(0)
    for car_type in car_typelist:
        path = os.path.join(model_path,car_type,"model.sdf")
        f = open(path,'r')
        content = f.read()
        models_file.append(f)
        models_content.append(content)

        
    # ROS节点初始化
    rospy.init_node('carsim')
    # 发现/spawn服务后，创建一个服务客户端，连接名为/gazebo/spawn_sdf_model的service
    rospy.wait_for_service('/gazebo/spawn_sdf_model')
    # 发现/delete服务后，创建一个服务客户端，连接名为/gazebo/delete_model的service
    rospy.wait_for_service('/gazebo/delete_model')
    #不停地模拟车辆变化
    while not rospy.is_shutdown():
        #对每一个停车位进行循环
        for i in range(len(position_x)):
            value = random.uniform(0,1)
            if value > threshold:
                if exist_flag[i]:
                    pass
                else:
                    print("Spwan car successfully [name:%s]" %(add_car(i,position_x[i],position_y[i])))
                    exist_flag[i] = 1
            else:
                if exist_flag[i]:
                    print("Delete car successfully [name:%s]" %(delete_car(i)))
                    exist_flag[i] = 0
            if i < 4:
                time.sleep(5)
            else:
                time.sleep(2)

        
	
    for f in models_file:
        f.close()

