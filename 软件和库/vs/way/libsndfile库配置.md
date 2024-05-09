## 1.vcpkg下载
```bash
.\vcpkg.exe install libogg:x86-windows-static
.\vcpkg.exe install libvorbis:x86-windows-static
.\vcpkg.exe install libflac:x86-windows-static
.\vcpkg.exe install libsndfile:x86-windows-static
```
# 参考[[SFML库配置]]
## 2.导入头文件
```bash
D:\visual_studio\vcpkg\vcpkg\installed\x86-windows-static\include
```
## 3.导入lib文件
```bash
D:\visual_studio\vcpkg\vcpkg\installed\x86-windows-static\lib
D:\visual_studio\vcpkg\vcpkg\installed\x86-windows-static\debug\lib
```
## 4.配置Debug和Release
### Debug
```bash
FLAC.lib
FLAC++.lib
libmp3lame-static.lib
libmpghip-static.lib
mpg123.lib
ogg.lib
opus.lib
out123.lib
sndfile.lib
syn123.lib
vorbis.lib
vorbisenc.lib
vorbisfile.lib
```
## 5.移动dll
* 这里的dll还是在x64