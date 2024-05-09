# 标注工具 Labelimg

## 安装
1. 打开 Anaconda 终端
    * 验证是否安装成功，以及版本指令`pip --version`
2. 安装依赖的第三方库
    * `pip install PyQt5`
    * `pip install PyQt5-tools`
    * `pip install lxml`
3. 安装插件 `pip install labelimg`

打开路径

![本地](Labelimg路径.png images/Anaconda/Labelimg路径.png>))
* 本机路径 C:\Users\86132\AppData\Roaming\Python\Python311\Scripts

## 使用
labelimg的标注模式分为VOC和YOLO两种，两种模式下生成的标注文件分别为.xml文件和.txt文件，因此在进行标注前需要优先选择好标注的模式

操作界面

![本地](Labelimg操作界面.png images/Anaconda/Labelimg操作界面.png>))
* labelimg左侧菜单栏中按钮功能

   ![本地](labelimg左侧菜单栏中按钮功能.png images/Anaconda/labelimg左侧菜单栏中按钮功能.png>))
* 在labelimg中，标注的快捷键为w，标注后用鼠标拖动锚框进行框选，框选完毕后会弹出类别选择框，如果是当前已有类则直接选择即可，若需要新加类别则在输入框中输入类别标签并确定

   ![本地](Labelimg标签操作.png images/Anaconda/Labelimg标签操作.png>))

## 两种文件和类别文件
xml文件
* 在 [[VOC资料]] 有

txt文件(YOLO备注模式)
* 数分别表示类别，中两个中心点坐标，后两个w，h

类别文件
* classes文件中是标注的类别
