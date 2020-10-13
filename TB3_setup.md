# TB3 setup

## ubuntu MATE 18.04 のインストール

MATEのイメージはここから落としてくる

研究室の三台のPCにはWindowsのダウンロードフォルダに入れてある

SDカードに書き込むためのソフトはここの `Raspberry Pi Imager` をダウンロード＆インストールし、利用する

https://www.raspberrypi.org/downloads/

研究室の三台のPCにはwindowsにすでにインストールしてある


以下の命名規則を定めているつもり

- デバイス名:raspi-X  (Xは大文字アルファベットで他機体に割り当てられてないもの)
- ユーザー名:turtle-x (xは小文字アルファベットで他機体に割り当てられてないもの)

Xとxは同じアルファベット

パスワードは "gazebo" で統一している




## ROS melodic のインストール

ここを参考にしていく。コマンドだけ読まず、本文の **英語も読め**

http://wiki.ros.org/melodic/Installation/Ubuntu

1.3は `sudo apt-key` だけ行う curlはしない
1.4では `sudo apt install ros-melodic-ros-base` を選択する
1.5も一番上のコマンド(`echo & source`)だけ行う

## ROS ワークスペースの作成

```bash
$ mkdir -p ~/catkin_ws/src
$ cd ~/catkin_ws/src
$ catkin_init_workspace
```

ワークスペースは空（srcフォルダにパッケージが無く、ただCMakeLists.txtのリンクがあるだけ）ですが、以下の手順でワークスペースをビルドすることができます。

```bash
$ cd ~/catkin_ws/
$ catkin_make
```

## Turtlebot3 のためのセットアップ

Turtlebot3 のコードを落としてくる
```bash
$ cd ~/catkin_ws/src
$ git clone https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
```
必要ないものを削除
```bash
$ cd ~/catkin_ws/src/turtlebot3
$ rm -r turtlebot3_description/ turtlebot3_teleop/ turtlebot3_navigation/ turtlebot3_slam/ turtlebot3_example/
```
追加で必要なパッケージのインストール
```bash
$ sudo apt install ros-melodic-rosserial-python ros-melodic-tf
```
ビルドする
```bash
$ cd ~/catkin_ws && catkin_make -j1
```

-j1は使用するコア数。メモリ使用量を抑えるためにひとつだけを指定(コンパイルが途中で止まることあり)

## USBのセットアップ

```bash
$ roscore
```
新しく別の端末を開き
```bash
$ rosrun turtlebot3_bringup create_udev_rules
```
後者が終了すれば、roscore側もctrl+cでストップ
OpenCRの右から２つめのオレンジのLEDの点滅が発生しなくなるまで待つ

## network config

nano ~/.bashrc

最終行に以下を追加

```bash
export ROS_MASTER_URI=http://ROS-PC.local:11311
export ROS_HOSTNAME=$HOSTNAME.local
```

## ssh

```bash
$ sudo apt purge openssh-server
$ sudo apt install openssh-server
```
## 動作チェック

roscoreの起動

PC
```bash:PC
$ roscore
```


turtlebot
```bash:turtlebot
$ roslaunch turtlebot3_bringup turtlebot3_robot.launch
```

PC
```bash:PC
roslaunch turtlebot3_bringup turtlebot3_remote.launch
```

Rviz(グラフィカルデバッグソフト)の起動

PC
```bash:PC
rosrun rviz rviz -d `rospack find turtlebot3_description`/rviz/model.rviz
```

turtlebotを操作する

PC
```bash
$ roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
```
WASDXで動けばOK
turtlebotの「前」はタイヤ(駆動輪)がある方