# 简介
是一个命令行工具（command-line tool）。它是Linux系统中用于控制视频4 Linux 2（V4L2）设备的命令行实用程序。

V4L2是Linux内核提供的框架，用于支持视频设备的捕捉、输出和控制。v4l2-ctl工具允许用户在命令行界面上与V4L2设备进行交互，以配置和控制视频设备的参数、功能和特性。

v4l2-ctl --list-devices
-----------------------
查看usb camera链接了的usb口

v4l2-ctl -d /dev/video0 --all
-----------------------------
显示摄像头的详细信息

v4l2-ctl -d /dev/video0 --list-formats 
---------------------------------------
查看支持输出格式

v4l2-ctl -d /dev/video0 --get-fmt-video
---------------------------------------
获取摄像头的当前设置

v4l2-ctl --d /dev/video_device --set-fmt-video=width=[width],height=[height],pixelformat=[MJPG] --stream-[mmap] --stream-to=path/to/output.jpg --stream-count=1
-------------------------------------------------------------------------
从特定设备以特定分辨率抓图
***例子***

v4l2-ctl -d /dev/video0 --set-fmt-video=width=640,height=480,pixelformat=MJPEG

设置了640x480的分辨率和MJPEG像素格式

* stream配置
~~~
    --stream-mmap：使用内存映射（mmap）模式进行视频流捕获

    --stream-userptr：使用用户指针（userptr）模式进行视频流捕获。在该模式下，视频帧将通过用户提供的缓冲区进行传输

    --stream-planes：使用多平面（planes）模式进行视频流捕获。在多平面模式下，视频帧的不同平面（如Y、U、V）将分别传输到不同的缓冲区
~~~
* stream-to 指定捕获的视频帧将保存为JPEG图像的路径
* stream-count 指定要捕获的视频帧数量，为1就是抓图，数量大就是抓流

v4l2-ctl -d /dev/video0 --list-ctrls
------------------------------------
列出设备控制值

v4l2-ctl -d /dev/video0 --list-formats-ext
-------------------------------------
检查设置是否已成功应用