# multi turtle

これは、Turtlebot3を複数台動かすためのソースです。
必ず、各ドキュメントを読んでください

## readable documents

ドキュメントは以下の通りです。

### create_package.md

制御器のプログラムの作成方法です。

### multi_navigation/readme.md

このツールの起動方法、使い方を記しています。

### PC_setup.md

PC環境のセットアップ方法を記載しています

### TB3_setup.md

turtlebot3のラズパイのセットアップ方法が記されています

## packages description

全部で以下の４パッケージあります

### multi_navigation

turtlebot3に他のロボットを避けながら移動させるパッケージです。また、目的地を指定しての移動も可能である。

### multi_sim

上のコードをgazebo(シミュレータ)上で動かすためのパッケージです
このパッケージを編集しないでください

### pubsub_cplus

- 速度指令の送信
- 固体から見た他ロボットの相対位置の読み取り
を行うexample(C++)コードです。

### example_python

- 速度指令の送信
- 固体から見た他ロボットの相対位置の読み取り
を行うexample(Python)コードです。
