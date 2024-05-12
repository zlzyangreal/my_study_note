导出的模型应该是导出 `torchscript` 模型
* [[pytorch模型保存三种格式]]
## 修改位置
**注意：修改的是野火提供的代码，不是官方代码，官方上会有很多的头部需要修改，因为推理的数据类型**
```python
    def forward(self, x):
        """Concatenates and returns predicted bounding boxes and class probabilities."""
        shape = x[0].shape  # BCHW
        if self.export and self.format == 'rknn':
            y = []
            for i in range(self.nl):
                y.append(self.cv2[i](x[i]))
                cls = torch.sigmoid(self.cv3[i](x[i]))
                # 修改为
                # cls_sum = torch.clamp(y[-1].sum(1, keepdim=True), 0, 1)
				# y.append(cls_sum)
				# 原内容
                cls_sum = torch.clamp(cls.sum(1, keepdim=True), 0, 1)
                y.append(cls)
                y.append(cls_sum)
                ###
            return y
        for i in range(self.nl):
            x[i] = torch.cat((self.cv2[i](x[i]), self.cv3[i](x[i])), 1)
        if self.training:
            return x
        elif self.dynamic or self.shape != shape:
            self.anchors, self.strides = (x.transpose(0, 1) for x in make_anchors(x, self.stride, 0.5))
            self.shape = shape
        x_cat = torch.cat([xi.view(shape[0], self.no, -1) for xi in x], 2)
        if self.export and self.format in ('saved_model', 'pb', 'tflite', 'edgetpu', 'tfjs'):  # avoid TF FlexSplitV ops
            box = x_cat[:, :self.reg_max * 4]
            cls = x_cat[:, self.reg_max * 4:]
        else:
            box, cls = x_cat.split((self.reg_max * 4, self.nc), 1)
        dbox = dist2bbox(self.dfl(box), self.anchors.unsqueeze(0), xywh=True, dim=1) * self.strides
        if self.export and self.format in ('tflite', 'edgetpu'):
            # Normalize xywh with image size to mitigate quantization error of TFLite integer models as done in YOLOv5:
            # https://github.com/ultralytics/yolov5/blob/0c8de3fca4a702f8ff5c435e67f378d1fce70243/models/tf.py#L307-L309
            # See this PR for details: https://github.com/ultralytics/ultralytics/pull/1695
            img_h = shape[2] * self.stride[0]
            img_w = shape[3] * self.stride[0]
            img_size = torch.tensor([img_w, img_h, img_w, img_h], device=dbox.device).reshape(1, 4, 1)
            dbox /= img_size
        y = torch.cat((dbox, cls.sigmoid()), 1)
        return y if self.export else (y, x)
```