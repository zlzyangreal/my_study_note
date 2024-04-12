# 数据集 VOC

数据集整体概况
-------------
### 层级结构
PASCAL VOC 数据集的20个类别及其层级结构：

![本地](<../../Document images/DS/VOC数据集层级结构.png>)
* 从2007年开始，PASCAL VOC每年的数据集都是这个层级结构
* 总共四个大类：vehicle,household,animal,person
* 总共20个小类，预测的时候是只输出图中黑色粗体的类别
* 数据集主要关注分类和检测，也就是分类和检测用到的数据集相对规模较大。关于其他任务比如分割，动作识别等，其数据集一般是分类和检测数据集的子集

### 发展历程
* 2005年：还只有4个类别： bicycles, cars, motorbikes, people. Train/validation/test共有图片1578 张，包含2209 个已标注的目标objects
* 2007年 ：在这一年PASCAL VOC初步建立成一个完善的数据集。类别扩充到20类，Train/validation/test共有9963张图片，包含24640 个已标注的目标objects
* 07年之前的数据集中test部分都是公布的，但是之后的都没有公布
* 2009年：从这一年开始，通过在前一年的数据集基础上增加新数据的方式来扩充数据集。比如09年的数据集是包含了08年的数据集的，也就是说08年的数据集是09年的一个子集，以后每年都是这样的扩充方式，直到2012年；09年之前虽然每年的数据集都在变大（08年比07年略少），但是每年的数据集都是不一样的，也就是说每年的数据集都是互斥的，没有重叠的图片
* 2012年：从09年到11年，数据量仍然通过上述方式不断增长，11年到12年，用于分类、检测和person layout 任务的数据量没有改变。主要是针对分割和动作识别，完善相应的数据子集以及标注信息 
![本地](<../../Document images/DS/VOC数据集发展历程.png>)
分割任务的数据集变化略有不同:
* VOC 2012用于分类和检测的数据包含 2008-2011年间的所有数据，并与VOC2007互斥
* VOC 2012用于分割的数据中train+val包含 2007-2011年间的所有数据，test包含2008-2011年间的数据，没有包含07年的是因为07年的test数据已经公开了

**目前广大研究者们普遍使用的是 VOC2007和VOC2012数据集，因为二者是互斥的，不相容的**

数据量统计
---------
### VOC 2007
示例照片 http://host.robots.ox.ac.uk/pascal/VOC/voc2007/examples/index.html#aeroplane

数据集总体统计:

![本地](<../../Document images/DS/VOC 2007数据集总体统计.png>)

训练集，验证集，测试集划分情况:

![本地](<../../Document images/DS/VOC 2007数据集总体统计.png>)

### VOC 2012
示例图片 http://host.robots.ox.ac.uk/pascal/VOC/voc2012/examples/index.html

数据集总体统计:

![本地](<../../Document images/DS/VOC 2012数据集总体统计.png>)

### VOC 2007 与 VOC 2012 对比
![本地](<../../Document images/DS/VOC 2007 与 VOC 2012  对比.png>)

标注信息
--------
标注信息是用 xml 文件组织的如下:
```xml
<annotation>
	<folder>VOC2007</folder>
	<filename>000001.jpg</filename>
	<source>
		<database>The VOC2007 Database</database>
		<annotation>PASCAL VOC2007</annotation>
		<image>flickr</image>
		<flickrid>341012865</flickrid>
	</source>
	<owner>
		<flickrid>Fried Camels</flickrid>
		<name>Jinky the Fruit Bat</name>
	</owner>
	<size>
		<width>353</width>
		<height>500</height>
		<depth>3</depth>
	</size>
	<segmented>0</segmented>
	<object>
		<name>dog</name>
		<pose>Left</pose>
		<truncated>1</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>48</xmin>
			<ymin>240</ymin>
			<xmax>195</xmax>
			<ymax>371</ymax>
		</bndbox>
	</object>
	<object>
		<name>person</name>
		<pose>Left</pose>
		<truncated>1</truncated>
		<difficult>0</difficult>
		<bndbox>
			<xmin>8</xmin>
			<ymin>12</ymin>
			<xmax>352</xmax>
			<ymax>498</ymax>
		</bndbox>
	</object>
</annotation>
```
1. `filename` 文件名
2. `source` `owner`图片来源 拥有者
3. `size` 图片大小
4. `segmented` 是否分割
5. `object` 表明这是一个目标，里面的内容是目标的相关信息
    * `name` object名称，20个类别
    * `pose` 拍摄角度：front, rear, left, right, unspecified
    * `truncated` 目标是否被截断（比如在图片之外），或者被遮挡（超过15%）
    * `difficult` 检测难易程度，这个主要是根据目标的大小，光照变化，图片质量来判断
    * `difficult` 示例: 图中白色虚线，被标记为 difficult
    
    ![本地](<../../Document images/DS/difficult示例.png>)
6. `bndbox` bounding box 的左上角点和右下角点的4个坐标值