## 1.[官方网址(64位亲测可用)](https://www.sfml-dev.org/download/sfml/2.6.1/)
* 括号里面对应的是VS版本
## 2.导入头文件
* `F:\XHY\Work_for_DSP_CPP\ACT\SFML-2.6.1\include`
![[SFML1.png]]
## 3.导入lib文件
![[SFML2.png]]
## 4.配置Debug和Release
### 配置Debug
```bash
sfml-audio-d.lib  
sfml-graphics-d.lib  
sfml-system-d.lib  
sfml-window-d.lib  
sfml-network-d.lib
```
### 配置Release
```bash
sfml-audio.lib  
sfml-graphics.lib  
sfml-system.lib  
sfml-window.lib  
sfml-network.lib
```
![[SFML3.png]]
## 5.将dll文件复制到工程下
![[SFML4.png]]
## 6.配置环境变量
电脑查看高级系统设置高级设置 -> 环境变量 -> 添加Path变量
![[SFML5.png]]
![[SFML6.png]]