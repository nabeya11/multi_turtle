# multi navigation

## 概要 / Overview
このプログラム群では、turtlebot3に目的地を指定し、他のロボットを避けながら移動させることができる。また、そのシミュレーションが可能である。
These programs can move turtlebot3 while avoiding others when destination is set. Also its simulation is possible.

## 手順
基本的には以下の手順で行う
1. ノートパソコン(以下remotePC)からroscoreを起動する
1. 実機をセットアップまたはシミュレーションを起動
1. 必要なプログラムを起動

ただし、事前にロボットを動かす環境の壁データ(以下mapfile)が必要.mapfile作成方法は別途記載

basically, Follow the steps below
1. start roscore by laptop(Hereinafter referred to as remotePC)
1. setup the real robots or launch simulation
1. launch required programs

However, Wall data(Hereinafter referred to as mapfile) of the surroundings in which the robot moves is required in advance

## roscoreの起動 / start roscore

```bash
$ roscore
```

## ロボットの準備 / Robot preparation

### 実機の場合 / for real robot



### シミュレーションの場合 / in simulation
multi_sim_world.launch を立ち上げる。ロボットの台数・初期位置はこのファイルをいじる。
launch multi_sim_world.launch. Please edit this file to change number of robots or initial position of each robot.

```bash
$ roslaunch multi_sim multi_sim_world.launch
```

## map&rvizの起動 / launch map&rviz
map_rviz.launchを起動する
start map_rviz.launch

ex.
```bash
$ roslaunch multi_navigation map_rviz.launch map_name:=realmap
```
### 役割 / description
map_rviz.launchには以下の２つの役割がある
map_rviz.launch has following two roles

- map_server: mapfileの壁データを出力する
- rviz: デバッグ用ソフト。各ノードから出る情報を視覚化するもの。シミュレーションシステムではない

- map_server: output a walldata in the mapfile
- rviz: for debug; vizualize data from each nodes. This is not a simulation system.

### 引数 / parameters

- map_name: 参照するmapファイル名。 `multi_navigation/maps` 内にあるもののみ。拡張子不要

- map_name: mapfile to reference in `multi_navigation/maps`. not need the extention.

## 目的地移動プログラムの立ち上げ / launch Move to destination program
各ロボットごとにmove_to_goal.launch を起動する
start map_rviz.launch for each robot

ex.
```bash
$ roslaunch multi_navigation move_to_goal.launch tb3_name:=tb3_0
```
### 役割 / description
コンソールから入力された場所(x,y)に移動する方向のベクトルを出す
また、後述するscan.launchから与えられるロボット位置からロボットを避ける動作を試みる
put a vector of direction to move to point(x,y) enterd from the console

### 引数 / parameters
- tb3_name: ロボット名
- tb3_name: robot name

- init_pose_x init_pose_y: ロボットの初期位置。 xが前進方向で右手系
- init_pose_x init_pose_y:The robot's initial position. x is in the forward direction and right-handed


## ロボット・障害物検知の実行 / run detection of robot and obstacle
各ロボットごとにscan.launch を起動する
start scan.launch for each robot

ex.
```bash
$ roslaunch multi_navigation scan.launch tb3_name:=tb3_0
```

### 役割 / description
LiDARのscanデータから、ロボットを抽出し、追従する
detect and follow robots from LiDAR scan data

初期位置と見失った場合はグローバルデータを参照する。
in initial and in case of losting robot, it refer to the global data

出力するデータは、自身からの相対位置及び姿勢(角度)
output data is relative position from itself and posture(angle)

### 引数 / parameters
- tb3_name: ロボット名
- tb3_name: robot name

### 注意 / attention
このプログラムはよく停止する。未解決
This program often stop unexpectedly unsolved

