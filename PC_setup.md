# PC setup

## ubuntu 18.04 のインストール

windowsなどがプリインストールされている場合、先にwindowsでディスクを空けておく必要がある
ディスクの管理からボリュームの縮小でubuntuにほしい分だけ減らす。128GBあれば十分かと思う
詳しい操作方法はggr

ubuntu18.04をインストールするにはセットアップUSBを作成する

インストール時にカスタムを選択して、efiパーティション、bootパーティション、ルートパーティションを作成する。前２つは100MBあれば十分

デバイス名は扱いやすいものを。もちろん全角不可、というか以降どのような場合でも全角不可

研究室共用のPCの場合、パスワードは "gazebo" で統一している

## (日本語Remixの場合)ローカルフォルダの英名化

「ドキュメント」→[Documents]など
必須ではないが、こうすることでコンソールから叩きやすい

```bash
$ LANG=C xdg-user-dirs-gtk-update
```
ダイアログが出てくるので、[Don't ask me this again]にチェックを付けた上で[Update Names]を選択

もしチェックをつけ忘れると、次のubuntu起動の際に同じダイアログ(今度は逆方向)が出てくるので、その時は[Don't ask me this again]にチェックを付けKeep old namesする

## (Windowsとデュアルブートする場合)時計の設定

これを行うことで、windows<->Ubuntuに切り替えた際の時刻がずれる問題を解決できる

```bash
$ sudo timedatectl set-local-rtc true
```

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

## Turtlebot3の依存パッケージのインストール

以下は一行

```bash
$ sudo apt install ros-melodic-joy ros-melodic-teleop-twist-joy ros-melodic-teleop-twist-keyboard ros-melodic-laser-proc ros-melodic-rgbd-launch ros-melodic-depthimage-to-laserscan ros-melodic-rosserial-arduino ros-melodic-rosserial-python ros-melodic-rosserial-server ros-melodic-rosserial-client ros-melodic-rosserial-msgs ros-melodic-amcl ros-melodic-map-server ros-melodic-move-base ros-melodic-urdf ros-melodic-xacro ros-melodic-compressed-image-transport ros-melodic-rqt-image-view ros-melodic-gmapping ros-melodic-navigation ros-melodic-interactive-markers
```

## Turtlebot3 のコードを落としてくる

- Turtlebot3公式のコード 3種
- OA自作のコード 1種

```bash
$ cd ~/catkin_ws/src/
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
$ git clone https://github.com/nabeya11/multi_turtle.git
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

export ROSLAUNCH_SSH_UNKNOWN=1
```

## 参考URL
https://emanual.robotis.com/docs/en/platform/turtlebot3/pc_setup/#pc-setup
https://qiita.com/take5249/items/13ada73bbd01ee12a2c3
https://linux.just4fun.biz/?Ubuntu/Unable+to+acquire+the+dpkg+frontend+lock%E3%80%8D%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6


## memo

catkin_create_pkg package_name rospy std_msgs geometry_msgs tf
