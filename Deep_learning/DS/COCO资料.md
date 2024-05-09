# 数据集COCO

MS COCO的全称是Microsoft Common Objects in Context，起源于微软于2014年出资标注的Microsoft COCO数据集，与ImageNet竞赛一样，被视为是计算机视觉领域最受关注和最权威的比赛之一

## 数据集特点
* Object segmentation
* Recognition in context
* Superpixel stuff segmentation
* 330K images (>200K labeled)
* 1.5 million object instances
* 80 object categories
* 91 stuff categories
* 5 captions per image
* 250,000 people with keypoints

在91个类别中的82个类别有超过5000个实例标记。其中包含了Pascal [[VOC资料]]的数据集类别。COCO数据集共有328000张图片，有2500000实例标记

![本地](<../../Document images/DS/COCO数据类别.jpg>)

该数据集主要解决3个问题：目标检测，目标之间的上下文关系，目标的2维上的精确定位

![本地](<../../Document images/DS/COCO数据集对比示意图.jpg>)

## 数据组成
COCO数据集分两部分发布，前部分于2014年发布，后部分于2015年

下载地址 https://cocodataset.org/#download

## COCO数据集格式
COCO有5种类型的标注，分别是：目标检测、关键点检测、实例分割、全景分割、图片标注，都是对应一个`json`文件。COCO数据集现在有3种标注类型：`object instances`（目标实例）, `object keypoints`（目标上的关键点）, 和`image captions`

![本地](<../../Document images/DS/annotation文件.jpg>)

```json
{
    "info": info,
    "licenses": [license],
    "images": [image],
    "annotations": [annotation],
    "categories": [category]
}
```
包含5个字段信息：`info`, `licenses`, `images`, `annotations`，`categories`

上面3种标注类型共享的字段信息有：`info`、`image`、`license`。不共享的是`annotation`和`category`这两种字段，他们在不同类型的JSON文件中是不一样的

* `images`字段列表元素的长度等同于划入训练集（或者测试集）的图片的数量
* `annotations`字段列表元素的数量等同于训练集（或者测试集）中`bounding box`的数量
* `categories`字段列表元素的数量等同于类别的数量，coco为80个类别

以 object instances为例

`info` 字段
```json
info: {
    "year": int,# 年份
    "version": str,# 版本
    "description": str, # 数据集描述
    "contributor": str,# 提供者
    "url": str,# 下载地址
    "date_created": datetime
}
```
`licenses`字段
```json
license{
    "id": int,
    "name": str,
    "url": str,
}
```
`images`字段
```json
image{
    "id": int,# 图片的ID编号（每张图片ID是唯一的）
    "width": int,#宽
    "height": int,#高
    "file_name": str,# 图片名
    "license": int,
    "flickr_url": str,# flickr网路地址
    "coco_url": str,# 网路地址路径
    "date_captured": datetime # 数据获取日期
}
```
Images是包含多个image实例的数组，对于一个image类型的实例:
```json
{
	"license":3,
	"file_name":"COCO_val2014_000000391895.jpg",
	"coco_url":"http:\/\/mscoco.org\/images\/391895",
	"height":360,
    "width":640,
    "date_captured":"2013-11-14 11:18:45",
	"flickr_url":"http:\/\/farm9.staticflickr.com\/8186\/8119368305_4e622c8349_z.jpg",
	"id":391895
}
```
`annotations`字段

`annotations`字段是包含多个`annotation`实例的一个列表，`annotation`类型本身又包含了一系列的字段，如这个目标的`category id`和`segmentation mask`。`segmentation`格式取决于这个实例是一个单个的对象（即`iscrowd=0`，将使用`polygons`格式）还是一组对象（即`iscrowd=1`，将使用`RLE`格式）。如下所示
```json
annotation{
    "id": int, # 对象ID，因为每一个图像有不止一个对象，所以要对每一个对象编号（每个对象的ID是唯一的）
    "image_id": int,# 对应的图片ID（与images中的ID对应）
    "category_id": int,# 类别ID（与categories中的ID对应）
    "segmentation": RLE or [polygon],# 对象的边界点（边界多边形，此时iscrowd=0）。
    #segmentation格式取决于这个实例是一个单个的对象（即iscrowd=0，将使用polygons格式）还是一组对象（即iscrowd=1，将使用RLE格式）
    "area": float,# 区域面积
    "bbox": [x,y,width,height], # 定位边框 [x,y,w,h]
    "iscrowd": 0 or 1 
}
```
`categories`字段

`ategories`是一个包含多个`category`实例的列表，而一个`category`结构体描述如下:
```json
{
	"supercategory": str,# 主类别
    "id": int,# 类对应的id （0 默认为背景）
    "name": str # 子类别
}
```
`categories`类型实例:
```json
{
	"supercategory": "person",
	"id": 1,
	"name": "person"
},
{
	"supercategory": "vehicle",
	"id": 2,
	"name": "bicycle"
}
```
可以读取json字典尝试一下看看,因为整体的json很大，这里只读取一张图片
```python
# -*- coding:utf-8 -*
from __future__ import print_function
import json

json_file='instances_val2017.json' # # Object Instance 类型的标注
# person_keypoints_val2017.json  # Object Keypoint 类型的标注格式
# captions_val2017.json  # Image Caption的标注格式

data=json.load(open(json_file,'r'))

data_2={}
data_2['info']=data['info']
data_2['licenses']=data['licenses']
data_2['images']=[data['images'][0]] # 只提取第一张图片
data_2['categories']=data['categories']
annotation=[]

# 通过imgID 找到其所有对象
imgID=data_2['images'][0]['id']
for ann in data['annotations']:
    if ann['image_id']==imgID:
        annotation.append(ann)

data_2['annotations']=annotation

# 保存到新的JSON文件，便于查看数据特点
json.dump(data_2,open('new_instances_val2017.json','w'),indent=4) # indent=4 更加美观显示
#打开 new_instances_val2017.json 观察数据格式
```