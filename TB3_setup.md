# TB3 setup

## ubuntu MATE 18.04 のインストール

MATEのイメージはここから落としてくる

https://releases.ubuntu-mate.org/archived/bionic/arm64/

.xzファイルをDLし、展開(ubuntuならばxzコマンドを利用)してimgにしておく

研究室の三台のPCにはWindowsのダウンロードフォルダに入れてある

SDカードに書き込むためのソフトはここの `Raspberry Pi Imager` をダウンロード＆インストールし、利用する

https://www.raspberrypi.org/downloads/

研究室の三台のPCにはwindowsにすでにインストールしてある


以下の命名規則を定めているつもり

- あなたの名前:turtle-X (xは小文字アルファベットで他機体に割り当てられてないもの、今後に影響はない)
- デバイス名:raspi-X  (Xは大文字アルファベットで他機体に割り当てられてないもの)
- ユーザー名:turtle-x (xは小文字アルファベットで他機体に割り当てられてないもの)

Xとxは同じアルファベット

パスワードは "gazebo" で統一している

起動したらコンソールを開いて(ctrl+alt+T)

```bash
$ sudo apt update && sudo apt upgrade -y
```
注：この処理が重たすぎて完全に止まることがある。その時は電源をつけ直して再度コマンドを打つ。また、errorが出るが気にしない。

処理が終わったら絶対reboot

## ssh

ディスプレイをつながず、PCから今後のセットアップを行いたい場合に使うssh
ssh自体についてはggr
デフォルトでインストールされているはずだが壊れていることがあるので次の操作で再インストールを行う

```bash
$ sudo apt purge openssh-server
$ sudo apt install openssh-server
```

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

- Turtlebot3公式のコード 3種
- OA自作のコード 1種

```bash
$ cd ~/catkin_ws/src
$ git clone https://github.com/ROBOTIS-GIT/hls_lfcd_lds_driver.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
$ git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
$ git clone https://github.com/nabeya11/multi_tb3.git
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

-j1は使用するコア数。メモリ使用量を抑えるためにひとつだけを指定(コンパイルが途中で止まることあるため)

## network config

nano ~/.bashrc

最終行に以下を追加

```bash
source ~/catkin_ws/devel/setup.bash

export ROS_MASTER_URI=http://ROS-PC.local:11311
export ROS_HOSTNAME=$HOSTNAME.local
export TURTLEBOT3_MODEL=burger
```
ROS_MASTER_URIの`ROS-PC`部はroscoreを立ち上げるPCのデバイス名にする。
出来たらctrl+sで保存、ctrl+xで終了

`source ~/.bashrc`を実行するか、ターミナルを開き直すことでbashrcの変更を適用する。

## USBのセットアップ

```bash
$ rosrun turtlebot3_bringup create_udev_rules
```
OpenCRの右から２つめのオレンジのLEDの点滅が発生しなくなるまで待つ

## 画面解像度の修正(必要があれば)

場合によっては画面が粗くて、ウィンドウのOKボタンが押せないことがある
その時は解像度設定を変える

```bash
$ sudo nano /boot/config.txt
```
で編集する
```
hdmi_group=2    # DMT
hdmi_mode=82	# 1920x1080 60Hz
```
で保存(ctrl+s)してnanoを終了(ctrl+x)、再起動(reboot)
起動時の文字が小さくなって全体的にこまやかになればOK

参考
https://note.com/mokuichi/n/n709037d0a32a
https://www.raspberrypi.org/forums/viewtopic.php?f=5&t=5851

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
WASDXキーで動けばOK
turtlebotの「前」はタイヤ(駆動輪)がある方

## chronyの導入

時計同期を外部ネットワークがない状態でもホストPCから取得できるようにする。

```bash
$ sudo apt install chrony
```

`/etc/chrony.conf`をmulti_tb3内にあるファイルに置き換える
(multi_tb3内にあるファイルを`/etc/chrony.conf`へ上書きコピーする)
