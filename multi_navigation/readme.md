# multi navigation

## 概要 / Overview
このプログラム群では、turtlebot3に目的地を指定し、他のロボットを避けながら移動させることができる。また、そのシミュレーションが可能である。

These programs can move turtlebot3 while avoiding others when destination is set. Also its simulation is possible.

## 手順
基本的には以下の手順で行う
1. ノートパソコン(以下remotePC)からroscoreを起動する
1. 実機をセットアップまたはシミュレーションを起動
1. 必要なプログラムを起動
1. オプションのプログラムや自作プログラムを起動

ただし、事前にロボットを動かす環境の壁データ(以下mapfile)が必要.mapfile作成方法は別途記載(予定)

basically, Follow the steps below
1. start roscore by laptop(Hereinafter referred to as remotePC)
1. setup the real robots or launch simulation
1. launch required programs
1. launch option program or Homebrew program

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

## observerの起動 / launch observer
observer.launchを起動する

start observer.launch

ex.
```bash
$ roslaunch multi_navigation observer.launch map_name:=realmap
```
### 役割 / description
observer.launchには以下の２つの役割がある

observer.launch has following two roles

- map_server: mapfileの壁データを出力する
- rviz: デバッグ用ソフト。各ノードから出る情報を視覚化するもの。シミュレーションシステムではない
- set_initpos: 各ロボットの初期位置を設定する

- map_server: output a walldata in the mapfile
- rviz: for debug; vizualize data from each nodes. This is not a simulation system.
- set_initpos: set initial position of each robot

### 引数 / parameters

- map_name: 参照するmapファイル名。 `multi_navigation/maps` 内にあるもののみ。拡張子不要

- map_name: mapfile to reference in `multi_navigation/maps`. not need the extention.

## ロボットコアシステムの実行 / run robot coresysetm

各ロボットごとにtb3_coresystem.launch を起動する

start tb3_coresystem.launch for each robot

ex.
```bash
$ roslaunch multi_navigation tb3_coresystem.launch tb3_name:=tb3_0
```

### 役割 / description

LiDARのscanデータから、ロボットを抽出し、その座標からロボットを避ける動作を加える。
初期位置と見失った場合はグローバルデータを参照する。

detect robots from LiDAR scan data
in initial and in case of losting robot, it refer to the global data

### 引数 / parameters
- tb3_name: ロボット名

- tb3_name: robot name


## (オプション)位置制御プログラムの立ち上げ / (option)launch position control program
各ロボットごとにposition_ctrl.launch を起動する
start position_ctrl.launch for each robot

ex.
```bash
$ roslaunch multi_navigation position_ctrl.launch tb3_name:=tb3_0
```
### 役割 / description
コンソールから入力された場所(x,y)に移動する方向の速度ベクトルを出す
put a Twist vector of direction to move to point(x,y) enterd from the console

### 引数 / parameters
- tb3_name: ロボット名
- tb3_name: robot name
