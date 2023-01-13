# Parking-monitoring-system
# 0. 声明
- 项目来源 https://github.com/ethz-asl/rotors_simulator

# 1. 编译
```shell
mkdir -p ~/rotors_ws/src
cd ~/rotors_ws/src
git clone https://github.com/SEUyhang/Parking-monitoring-system.git
cd ..
catkin_make
```

## 2. 运行
- 单机仿真
```shell
cd ~/rotors_ws/
source devel/setup.bash
roslaunch rotors_gazebo single_uav.launch
```
- 多机仿真
```shell
cd ~/rotors_ws/
source devel/setup.bash
roslaunch rotors_gazebo multi_uav.launch
```

- 默认均采用 `ardrone` 四旋翼无人机

## 3. 常用参数说明
- `~/rotors_ws/rotors_simulator/rotors_gazebo/launch/spawn_mav.launch` 中
  ```shell
  <arg name="x" default="0.0"/>
  <arg name="y" default="0.0"/>
  <arg name="z" default="0.1"/>
  ```
  决定无人机初始位置，`single_uav.launch` 和 `multi_uav.launch` 均引入`spawn_mav.launch` 文件，只修改了 `y` 值，其它保持不变。
- `~/rotors_ws/rotors_simulator/rotors_gazebo/launch/multi_mav.launch` 中，每一个 `<group ns="">` 标签对用于添加新的无人机，`ns` 指示话题前缀名。

## 4. 常用话题说明
- `/ardrone_{x}/command/pose`：无人机位姿控制话题，控制无人机位姿
- `/ardrone_{x}/odometry_sensor{x}/odometry`：无人机里程计话题，世界坐标系下的坐标
- `/ardrone_{x}/vi_sensor/camera_depth/camera/camera_info`：深度相机内参
- `/ardrone_{x}/vi_sensor/camera_depth/camera/image_raw`：原图
- `/ardrone_{x}/vi_sensor/camera_depth/depth/disparity`：深度图
- `/ardrone_{x}/vi_sensor/left/image_raw`：左目相机图
- `/ardrone_{x}/vi_sensor/right/image_raw`：右目相机图


## 5. 修改相机位置
- 修改 `rotors_simulator/rotors_description/urdf/mav_with_vi_sensor.gazebo`中的`<origin xyz="0.1 0.0 -0.03" rpy="0.0 0.1 0.0" />`，相较于机体的位置，`x,y,z`为位置，`rpy`为旋转欧拉角

## 6. 加载世界模型
- 目前可在 gazebo 中直接插入组件
- 世界模型在Parking-monitoring/rotors_gazebo/worlds中，launch中可修改默认的world
- to be continue
