# PC setup

## ubuntu 18.04 のインストール

windowsなどがプリインストールされている場合、先にwindowsでディスクを空けておく必要がある
ディスクの管理からボリュームの縮小でubuntuにほしい分だけ減らす。128GBあれば十分かと思う
詳しい操作方法はggr

ubuntu18.04をインストールするにはセットアップUSBを作成する

インストール時にカスタムを選択して、efiパーティション、bootパーティション、ルートパーティションを作成する。前２つは100MBあれば十分

デバイス名は扱いやすいものを。もちろん全角不可、というか以降どのような場合でも全角不可

研究室共用のPCの場合、パスワードは "gazebo" で統一している

## ROS melodic のインストール

ここを参考にしていく。コマンドだけ読まず、本文の **英語も読め**
http://wiki.ros.org/melodic/Installation/Ubuntu

1.3は `sudo apt-key` だけ行う curlはしない
1.4では `sudo apt install ros-melodic-desktop-full` を選択する
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

## Turtlebot3 のコードを落としてくる

```bash
$ cd ~/catkin_ws/src/
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
$ cd ~/catkin_ws && catkin_make
```

## network config

vscodeで ~/.bashrcを開く
最終行に以下を追加
```bash
source ~/catkin_ws/devel/setup.bash

export ROS_MASTER_URI=http://localhost:11311
export ROS_HOSTNAME=$HOSTNAME.local

export TURTLEBOT3_MODEL=burger
```
