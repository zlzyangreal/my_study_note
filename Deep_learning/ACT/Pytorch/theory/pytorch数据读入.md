# 3.3 数据读入

PyTorch数据读入是通过Dataset+DataLoader的方式完成的，Dataset定义好数据的格式和数据变换形式，DataLoader用iterative的方式不断读入批次数据。

我们可以定义自己的Dataset类来实现灵活的数据读取，定义的类需要继承PyTorch自身的Dataset类。主要包含三个函数：

- `__init__`: 用于向类中传入外部参数，同时定义样本集
- `__getitem__`: 用于逐个读取样本集合中的元素，可以进行一定的变换，并将返回训练/验证所需的数据
- `__len__`: 用于返回数据集的样本数

下面以cifar10数据集为例给出构建Dataset类的方式：

```python
import torch
from torchvision import datasets
train_data = datasets.ImageFolder(train_path, transform=data_transform)
val_data = datasets.ImageFolder(val_path, transform=data_transform)
```

这里使用了PyTorch自带的ImageFolder类的用于读取按一定结构存储的图片数据（path对应图片存放的目录，目录下包含若干子目录，每个子目录对应属于同一个类的图片）。

其中`data_transform`可以对图像进行一定的变换，如翻转、裁剪等操作，可自己定义。

这里我们给出一个自己定制Dataset的例子

```python

import os
import pandas as pd
from torchvision.io import read_image

class MyDataset(Dataset):
    def __init__(self, annotations_file, img_dir, transform=None, target_transform=None):
        """
        Args:
            annotations_file (string): Path to the csv file with annotations.
            img_dir (string): Directory with all the images.
            transform (callable, optional): Optional transform to be applied
                on a sample.
            target_transform (callable, optional): Optional transform to be applied
                on the target.
        """
        self.img_labels = pd.read_csv(annotations_file)
        self.img_dir = img_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.img_labels)

    def __getitem__(self, idx):
        """
        Args:
            idx (int): Index
        """
        img_path = os.path.join(self.img_dir, self.img_labels.iloc[idx, 0])
        image = read_image(img_path)
        label = self.img_labels.iloc[idx, 1]
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            label = self.target_transform(label)
        return image, label
```
其中，我们的标签类似于以下的形式：
```csv
image1.jpg, 0
image2.jpg, 1
......
image9.jpg, 9
```
构建好Dataset后，就可以使用DataLoader来按批次读入数据了，实现代码如下：

```python
from torch.utils.data import DataLoader

train_loader = torch.utils.data.DataLoader(train_data, batch_size=batch_size, num_workers=4, shuffle=True, drop_last=True)
val_loader = torch.utils.data.DataLoader(val_data, batch_size=batch_size, num_workers=4, shuffle=False)
```

其中:

- batch_size：样本是按“批”读入的，batch_size就是每次读入的样本数
- num_workers：有多少个进程用于读取数据，Windows下该参数设置为0，Linux下常见的为4或者8，根据自己的电脑配置来设置
- shuffle：是否将读入的数据打乱，一般在训练集中设置为True，验证集中设置为False
- drop_last：对于样本最后一部分没有达到批次数的样本，使其不再参与训练

这里可以看一下我们的加载的数据。PyTorch中的DataLoader的读取可以使用next和iter来完成

```python
import matplotlib.pyplot as plt
images, labels = next(iter(val_loader))
print(images.shape)
plt.imshow(images[0].transpose(1,2,0))
plt.show()
```