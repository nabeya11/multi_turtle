# create_package

制御器のプログラムは出来るだけ、multi_turtleフォルダ外に作成し、multi_turtle内の編集を出来るだけ最小に抑えたい。
catkin_ws/srcにて以下のコマンドをうつことで、新しいpakageが作成される。`package_name`は任意。

```bash
catkin_create_pkg package_name rospy std_msgs geometry_msgs tf
```

{package_name}ディレクトリ内にsrcフォルダを作成し、その中にpythonファイル（制御器のプログラム）を作成する。

launchファイルを作成するときは、同様にpackage_nameディレクトリの下にlaunchフォルダを作成する。
