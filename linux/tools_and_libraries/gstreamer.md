# 简介
GStreamer是一个功能强大的开源多媒体框架，用于创建、处理和播放多媒体应用程序。它提供了一组库、工具和插件，可用于构建各种多媒体处理和流媒体应用

例子
----
gst-launch-1.0 videotestsrc ! videoconvert ! autovideosink

gst-launch-1.0 videotestsrc pattern=11 ! videoconvert ! autovideosink

gst-launch-1.0 souphttpsrc location=https://www.freedesktop.org/software/gstreamer-sdk/data/media/sintel_trailer-480p.webm ! matroskademux name=d d.video_00 ! matroskamux ! filesink location=sintel_video.mkv
-------------------------------------------------------------------------
这个指令使用GStreamer的gst-launch-1.0工具创建一个视频处理管道，从指定的URL下载WebM格式的视频文件，并将其转换为MKV格式的视频文件

* souphttpsrc：这是GStreamer中的元件，用于从HTTP/HTTPS URL下载数据
* matroskademux：这是GStreamer中的元件，用于解封装Matroska（MKV）容器格式。它将下载的WebM文件解封装为Matroska容器，并将其分离为音频、视频和其他流
* name=d：这是一个元件命名操作，将matroskademux元件命名为d，以便后续连接使用
* d.video_00：这是matroskademux元件的视频输出流。它将被连接到后续的元件进行处理
* matroskamux：这是GStreamer中的元件，用于封装音频和视频流为Matroska（MKV）容器格式
* filesink：这是GStreamer中的元件，用于将数据写入文件。在这个指令中，它被用来将转换后的视频流写入MKV文件
* location=sintel_video.mkv：这是输出文件的路径和名称。在这个指令中，视频流将被写入名为sintel_video.mkv的文件



gst-launch-1.0 uridecodebin uri=[网址] ! decodebin ! autovideosink
------------------------------------------------------------------
从网站拉下视频

网站：

http://mirror.aarnet.edu.au/pub/TED-talks/911Mothers_2010W-480p.mp4(最稳定)

http://clips.vorwaerts-gmbh.de/big_buck_bunny.mp4

http://vjs.zencdn.net/v/oceans.mp4

https://media.w3.org/2010/05/sintel/trailer.mp4

gst-launch-1.0 videotestsrc pattern=smpte ! autovideosink
-----------------------------------------
彩条测试

