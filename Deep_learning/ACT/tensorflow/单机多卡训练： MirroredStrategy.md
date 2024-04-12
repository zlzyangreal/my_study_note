[csdn原文：含原理](https://blog.csdn.net/zimiao552147572/article/details/105034637)
[pytorch多卡方式](DDP(显卡交火).md)
tf.distribute.MirroredStrategy 是一种简单且高性能的，数据并行的同步式分布式策略，主要支持多个 GPU 在同一台主机上训练
# MirroredStrategy运行原理：
1、训练开始前，该策略在所有 N 个计算设备（GPU）上均各复制一份完整的模型
2、每次训练传入一个批次的数据时，将数据分成 N 份，分别传入 N 个计算设备（即数据并行）
3、使用分布式计算的 All-reduce 操作，在计算设备间高效交换梯度数据并进行求和，使得最终每个设备都有了所有设备的梯度之和，使用梯度求和的结果更新本地变量
* 当所有设备均更新本地变量后，进行下一轮训练（即该并行策略是同步的）。默认情况下，TensorFlow 中的 MirroredStrategy 策略使用 NVIDIA NCCL 进行 All-reduce 操作。
# 构建代码步骤：
**使用这种策略时，我们只需实例化一个 MirroredStrategy 策略:**
```python
strategy = tf.distribute.MirroredStrategy()
```
**并将模型构建的代码放入 strategy.scope() 的上下文环境中:**
```python
with strategy.scope(): 
# 模型构建代码
```

> [!NOTE] 在参数中指定设备，如:
> strategy = tf.distribute.MirroredStrategy(devices=["/gpu:0", "/gpu:1"]
> *即指定只使用第 0、1 号 GPU 参与分布式策略*

## eg
使用 MirroredStrategy 策略，在 TensorFlow Datasets 中的部分图像数据集上使用 Keras 训练 MobileNetV2 的过程
```python
import tensorflow as tf
import tensorflow_datasets as tfds
 
num_epochs = 5
batch_size_per_replica = 64
learning_rate = 0.001
 
strategy = tf.distribute.MirroredStrategy()
print('Number of devices: %d' % strategy.num_replicas_in_sync)  # 输出设备数量
batch_size = batch_size_per_replica * strategy.num_replicas_in_sync
 
# 载入数据集并预处理
def resize(image, label):
    image = tf.image.resize(image, [224, 224]) / 255.0
    return image, label
 
# 当as_supervised为True时，返回image和label两个键值
dataset = tfds.load("cats_vs_dogs", split=tfds.Split.TRAIN, as_supervised=True)
dataset = dataset.map(resize).shuffle(1024).batch(batch_size)
 
with strategy.scope():
    model = tf.keras.applications.MobileNetV2()
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.sparse_categorical_crossentropy,
        metrics=[tf.keras.metrics.sparse_categorical_accuracy]
    )
 
model.fit(dataset, epochs=num_epochs)
```

### MirroredStrategy过程简介：
1. 训练开始前，该策略在所有 N 个计算设备上均各复制一份完整的模型；
2. 每次训练传入一个批次的数据时，将数据分成 N 份，分别传入 N 个计算设备（即数据并行）；
3. N 个计算设备使用本地变量（镜像变量）分别计算自己所获得的部分数据的梯度；
4. 使用分布式计算的 All-reduce 操作，在计算设备间高效交换梯度数据并进行求和，使得最终每个设备都有了所有设备的梯度之和；
5. 使用梯度求和的结果更新本地变量（镜像变量）；
6. 当所有设备均更新本地变量后，进行下一轮训练（即该并行策略是同步的）
#### eg
```python
%tensorflow_version 2.x
import tensorflow as tf
print(tf.__version__)
from tensorflow.keras import * 

#此处在colab上使用1个GPU模拟出两个逻辑GPU进行多GPU训练
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    # 设置两个逻辑GPU模拟多GPU训练
    try:
        tf.config.experimental.set_virtual_device_configuration(gpus[0],
            [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024),
             tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPU,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        print(e)

### 准备数据
MAX_LEN = 300
BATCH_SIZE = 32
(x_train,y_train),(x_test,y_test) = datasets.reuters.load_data()
x_train = preprocessing.sequence.pad_sequences(x_train,maxlen=MAX_LEN)
x_test = preprocessing.sequence.pad_sequences(x_test,maxlen=MAX_LEN)
​
MAX_WORDS = x_train.max()+1
CAT_NUM = y_train.max()+1
​
ds_train = tf.data.Dataset.from_tensor_slices((x_train,y_train)) \
          .shuffle(buffer_size = 1000).batch(BATCH_SIZE) \
          .prefetch(tf.data.experimental.AUTOTUNE).cache()
   
ds_test = tf.data.Dataset.from_tensor_slices((x_test,y_test)) \
          .shuffle(buffer_size = 1000).batch(BATCH_SIZE) \
          .prefetch(tf.data.experimental.AUTOTUNE).cache()
​
### 定义模型
tf.keras.backend.clear_session()
def create_model():
    
    model = models.Sequential()
​
    model.add(layers.Embedding(MAX_WORDS,7,input_length=MAX_LEN))
    model.add(layers.Conv1D(filters = 64,kernel_size = 5,activation = "relu"))
    model.add(layers.MaxPool1D(2))
    model.add(layers.Conv1D(filters = 32,kernel_size = 3,activation = "relu"))
    model.add(layers.MaxPool1D(2))
    model.add(layers.Flatten())
    model.add(layers.Dense(CAT_NUM,activation = "softmax"))
    return(model)
​
def compile_model(model):
    model.compile(optimizer=optimizers.Nadam(),
                loss=losses.SparseCategoricalCrossentropy(from_logits=True),
                metrics=[metrics.SparseCategoricalAccuracy(),metrics.SparseTopKCategoricalAccuracy(5)]) 
    return(model)

### 训练模型
#增加以下两行代码
strategy = tf.distribute.MirroredStrategy()  
with strategy.scope(): 
    model = create_model()
    model.summary()
    model = compile_model(model)
    
history = model.fit(ds_train,validation_data = ds_test,epochs = 10)  
```