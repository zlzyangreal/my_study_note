[论文](https://arxiv.org/abs/2106.08265)
[‍‌​⁣​⁣​⁤⁢‬⁤​​​​‌​‬⁣⁤​‬‍‍‌⁤‍‬⁢⁣​‬‌‬⁢​‌‍⁤‍⁤‬​⁡⁤⁡​‬⁡‬HikRobot-Competition - 飞书云文档 (feishu.cn)](https://hownzcc0792.feishu.cn/docx/TCgldls43oOl6sx3ycHcvBlPndh)
PatchCore是2021年提出的基于预训练神经网络的工业异常检测模型，截至2021年末在MVTex-AD数据集上精度排名第一。PatchCore训练时仅使用正常样本，训练过程中不对网络参数进行更新(无反向传播)，将每张图片的网络输出(图片对应区域的特征表示)保存作为“Memory Bank”的一部分，最后进行采样操作得到最终“Memory Bank”。推理时加载“Memory Bank”，得到某张图片的网络输出后，通过论文定义的计算得到该图片score，以输出异常图。


