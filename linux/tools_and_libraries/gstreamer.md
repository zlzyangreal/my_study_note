# 简介
GStreamer是一个功能强大的开源多媒体框架，用于创建、处理和播放多媒体应用程序。它提供了一组库、工具和插件，可用于构建各种多媒体处理和流媒体应用

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

