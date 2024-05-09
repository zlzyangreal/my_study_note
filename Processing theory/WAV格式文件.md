WAV是微软公司开发的一种音频格式文件，用于保存Windows平台的音频信息资源，它符合资源互换文件格式(Resource Interchange File Format，RIFF)文件规范。标准格式化的WAV文件和CD格式一样，也是44.1K的取样频率，16位量化数字，因此在声音文件质量和CD相差无几！WAVE是录音时用的标准的WINDOWS文件格式，文件的扩展名为“WAV”，数据本身的格式为PCM或压缩型，属于无损音乐格式的一种。
### 1. RIFF文件规范
RIFF有不同数量的chunk(区块)组成，每个chunk由“标识符”、“数据大小”和“数据”三个部分组成， “标识符”和“数据大小”都是占用4个字节空间。简单RIFF格式文件结构参考 图10。 最开始是ID为“RIFF”的chunk，Size为“RIFF”chunk数据字节长度，所以总文件大小为Size+8。 一般来说，chunk不允许内部再包含chunk，但有两个例外，ID为“RIFF”和“LIST”的chunk却是允许。 对此“RIFF”在其“数据”首4个字节用来存放“格式标识码(Form Type)”，“LIST”则对应“LIST Type”。

![图36_0_10 RIFF文件格式结构](https://doc.embedfire.com/mcu/stm32/f4/hal_general/zh/latest/_images/image105.png)

图10 RIFF文件格式结构

### 2. WAVE文件
WAVE文件是非常简单的一种RIFF文件，其“格式标识码”定义为WAVE。RIFF chunk包括两个子chunk，ID分别为fmt和data，还有一个可选的fact chunk。Fmt chunk用于表示音频数据的属性，包括编码方式、声道数目、采样频率、每个采样需要的bit数等等信息。fact chunk是一个可选chunk，一般当WAVE文件由某些软件转化而成就包含fact chunk。data chunk包含WAVE文件的数字化波形声音数据。WAVE整体结构如表 2。

表 2 WAVE文件结构

| 标识码(“RIFF”)   |
| ------------- |
| 数据大小          |
| 格式标识码(“WAVE”) |
| “fmt”         |
| “fmt”块数据大小    |
| “fmt”数据       |
| “fact”(可选)    |
| “fact”块数据大小   |
| “fact”数据      |
| “data”        |
| 声音数据大小        |
| 声音数据          |

data chunk是WAVE文件主体部分，包含声音数据，一般有两个编码格式：PCM和ADPCM，ADPCM(自适应差分脉冲编码调制)属于有损压缩，现在几乎不用，绝大部分WAVE文件是PCM编码。PCM编码声音数据可以说是在“数字音频技术”介绍的源数据，主要参数是采样频率和量化位数。
表 3为量化位数为16bit时不同声道数据在data chunk数据排列格式。

表 3 16bit声音数据格式
![表 36‑0‑3 16bit声音数据格式](https://doc.embedfire.com/mcu/stm32/f4/hal_general/zh/latest/_images/table14.png)
### 3. WAVE文件实例分析

利用winhex工具软件可以非常方便以十六进制查看文件，图11 为名为“张国荣-一盏小明灯.wav” 文件使用winhex工具打开的部分界面截图。这部分截图是WAVE文件头部分，声音数据部分数据量非常大，有兴趣可以使用winhex查看。
![图36_0_11 WAV文件头实例](https://doc.embedfire.com/mcu/stm32/f4/hal_general/zh/latest/_images/image1110.png)
图11 WAV文件头实例

下面对文件头进行解读，参考表 4。
表 4 WAVE文件格式说明

|     | 偏移地址 | 字节数 | 数据类型     | 十六进制源码      | 内容                                    |
| --- | ---- | --- | -------- | ----------- | ------------------------------------- |
| 文件头 | 00H  | 4   | char     | 52 49 46 46 | “RIFF”标识 符                            |
|     | 04H  | 4   | long int | F4 FE 83 01 | 文件长度：0x0 183FEF4( 注意顺序)               |
|     | 08H  | 4   | char     | 57 41 56 45 | “WAVE”标识 符                            |
|     | 0CH  | 4   | char     | 66 6D 74 20 | “fmt ”，最后一位为空 格                       |
|     | 10H  | 4   | long int | 10 00 00 00 | fmt chunk大小： 0x10                     |
|     | 14H  | 2   | int      | 01 00       | 编码格式：0x0 1为PCM。                       |
|     | 16H  | 2   | int      | 02 00       | 声道数目：0x01为单声道，0x02为双声道                |
|     | 18H  | 4   | int      | 44 AC 00 00 | 采样频率(每秒样 本数)：0xAC 44(44100 )          |
|     | 1CH  | 4   | long int | 10 B1 02 00 | 每秒字节数：0x 02B110，等 于`声道数*采样频 率*量化位数/8` |
|     | 20H  | 2   | int      | 04 00       | 每个采样点字节数 ：0x04，等于 `声道数*量化位数 /8`       |
|     | 22H  | 2   | int      | 10 00       | 量化位数：0x1                              |
|     | 24H  | 4   | char     | 64 61 74 61 | “data”数据 标识符                          |
|     | 28H  | 4   | long int | 48 FE 83 01 | 声音数据量：0x 0183FE48                     |
