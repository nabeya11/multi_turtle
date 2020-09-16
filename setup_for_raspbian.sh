#!/bin/bash

#create user and set password
sudo /usr/sbin/useradd --groups sudo -m turtle-b
sudo passwd turtle-b

#change root password
#sudo passwd root

#delete pi user
userdel -r pi

#1.1 Installing bootstrap dependencies
sudo apt-get install python-rosdep python-rosinstall-generator python-vcstool python-rosinstall build-essential
#1.2 Initializing rosdep
sudo rosdep init
rosdep update
#2.1 Create a catkin Workspace
mkdir -p ~/ros_catkin_ws/src
cd ~/ros_catkin_ws
#ROS-Comm: (Bare Bones) ROS package, build, and communication libraries. No GUI tools. 
rosinstall_generator ros_comm --rosdistro melodic --deps --tar > melodic-ros_comm.rosinstall
vcs import src < melodic-ros_comm.rosinstall
#2.1.1 Resolving Dependencies
rosdep install --from-paths src --ignore-src --rosdistro melodic -y
#2.1.2 Building the catkin Workspace
./src/catkin/bin/catkin_make_isolated --install -DCMAKE_BUILD_TYPE=Release -j2

echo "source ~/ros_catkin_ws/install_isolated/setup.bash" >> ~/.bashrc
source ~/.bashrc

#create workspace
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src
catkin_init_workspace

cd ~/catkin_ws/
catkin_make
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc

cd ~/catkin_ws/src
git clone https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver.git
git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone https://github.com/ROBOTIS-GIT/turtlebot3.git

cd ~/catkin_ws/src/turtlebot3
rm -r turtlebot3_description/ turtlebot3_teleop/ turtlebot3_navigation/ turtlebot3_slam/ turtlebot3_example/

sudo apt-get install ros-melodic-rosserial-python ros-melodic-tf

$ cd ~/catkin_ws && catkin_make -j2

roscore & rosrun turtlebot3_bringup create_udev_rules

echo "export ROS_MASTER_URI=http://ROS.local:11311" >> ~/.bashrc
echo "export ROS_HOSTNAME=http://${HOSTNAME}.local" >> ~/.bashrc
source ~/.bashrc