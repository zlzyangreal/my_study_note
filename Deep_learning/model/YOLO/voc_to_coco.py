import os, shutil
from tqdm import tqdm
from collections import Counter
import xml.etree.ElementTree as ET
from PIL import Image
import yaml
import random
 
 
class Dataset_Transforme_Yolov8:
    def __init__(self, jpg_path: str, xml_path: str, save_path: str, divide=False):
        self.jpg_path = jpg_path
        self.xml_path = xml_path
        self.save_path = save_path
        self.divide = divide
 
    def get_classes(self):
        '''
        缂佺喕顓哥捄顖氱窞娑撳ml闁插瞼娈戦崥鍕閸掝偅鐖ｇ粵鐐殶闁??        '''
        names = []
        files_1 = []
        for root, dirs, files in os.walk(self.xml_path):
            for file in files:
                if ".xml" in file:
                    file = os.path.join(root, file)
                    subs = ET.parse(file).getroot().findall("object")
                    if len(subs) != 0:
                        files_1.append(file)
                    for sub in subs:
                        name = sub.find("name").text
                        names.append(name)
        result = Counter(names)
        return result, files_1
 
    def xml2txt(self, classes, file_path, txt_save_path, image_width, image_height):
        '''
        根据xml文件生成txt文件
        :param classes 类别列表        
        :param file_path xml文件路径
        :param image_width 图片宽度        
        :param image_height 图片高度      
        '''
        tree = ET.parse(file_path)
        root = tree.getroot()
        objects = root.findall('object')
        bboxes = []
        class_names = []
        for obj in objects:
            bbox = obj.find('bndbox')
            xmin = int(bbox.find('xmin').text)
            ymin = int(bbox.find('ymin').text)
            xmax = int(bbox.find('xmax').text)
            ymax = int(bbox.find('ymax').text)
            class_name = obj.find('name').text
 
            c1 = round((xmin + xmax) / (image_width * 2), 6)
            c2 = round((ymin + ymax) / (image_height * 2), 6)
            c3 = round((xmax - xmin) / image_width, 6)
            c4 = round((ymax - ymin) / image_height, 6)
 
            if class_name in classes:
                # print(class_name)
                bboxes.append([c1, c2, c3, c4])
                class_names.append(class_name)
            # 鐏忓棙鏆熼幑顔煎晸閸忋儱鍩孻OLO閻ㄥ嚲XT閺傚洣娆㈡稉?        with open(txt_save_path, 'w') as file:
            for bbox, class_name in zip(bboxes, class_names):
                file.write(
                    f"{classes.index(class_name)} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")
 
    def data_split(self, full_list, train, val, shuffle, seed):
        """
        数据划分: 将列表full_list按比例分割成train,val,test
        :param full_list: 数据列表
        :param ratio: 比例
        :param shuffle: 是否打乱设计
        :param seed: 随机种子
        :return:
        """
        n_total = len(full_list)
        offset_train = int(n_total * train)
        offset_val = int(n_total * val)
        offset_trainval = offset_train + offset_val
 
        if n_total == 0 or offset_train < 1 or train + val > 1.0:
            raise ValueError("划分出差,请检查列表与划分比例!参考格式:train,val->0.7,0.1")
 
        if shuffle:
            random.seed(seed)
            random.shuffle(full_list)
        train_list = full_list[:offset_train]
        val_list = full_list[offset_train:offset_trainval]
        test_list = full_list[offset_trainval:]
        return train_list, val_list, test_list
 
    def voc2yolov8(self, train, val, shuffle=True, seed=10):
        """
        :param train: 训练集比例        
        :param val: 验证集比例        
        """
        obj_classes, files = self.get_classes()
 
        os.makedirs(os.path.join(self.save_path, "images/train"), exist_ok=True)
        os.makedirs(os.path.join(self.save_path, "images/val"), exist_ok=True)
        os.makedirs(os.path.join(self.save_path, "images/test"), exist_ok=True)
 
        os.makedirs(os.path.join(self.save_path, "labels/train"), exist_ok=True)
        os.makedirs(os.path.join(self.save_path, "labels/val"), exist_ok=True)
        os.makedirs(os.path.join(self.save_path, "labels/test"), exist_ok=True)
 
        classes = list(obj_classes.keys())
        train_list, val_list, test_list = self.data_split(files, train, val, shuffle, seed)
        for file in tqdm(files):
            if ".xml" in file:
                name = file.replace("\\", "/").split("/")[-1].split(".")[0]
                xml_file = file.replace("\\", "/")
                jpg_file = os.path.join(self.jpg_path, name + ".jpg").replace("\\", "/")
                img_w, img_h = Image.open(jpg_file).size
 
                if file in val_list:
                    txt_save_path=os.path.join(self.save_path, "labels/val",name+".txt")
                    self.xml2txt(classes, xml_file, txt_save_path, img_w, img_h)
                elif file in test_list:
                    txt_save_path = os.path.join(self.save_path, "labels/test", name + ".txt")
                    self.xml2txt(classes, xml_file, txt_save_path, img_w, img_h)
                else:
                    txt_save_path = os.path.join(self.save_path, "labels/train", name + ".txt")
                    self.xml2txt(classes, xml_file, txt_save_path, img_w, img_h)
 
                if self.divide:
                    if file in val_list:
                        shutil.copy(jpg_file, os.path.join(self.save_path, "images/val", name + ".jpg"))
                    elif file in test_list:
                        shutil.copy(jpg_file, os.path.join(self.save_path, "images/test", name + ".jpg"))
                    else:
                        shutil.copy(jpg_file, os.path.join(self.save_path, "images/train", name + ".jpg"))
 
        # 缂傛牕鍟搚aml閺傚洣娆?
        classes_txt = {i: classes[i] for i in range(len(classes))}  # 閺嶅洨顒风猾璇插焼
        data = {
            'path': os.path.join(os.getcwd(),self.save_path),
            'train': "images/train",
            'val': "images/val",
            'test': "images/test",
            'names': classes_txt,
            'download': ''
        }
        with open(self.save_path + '/dataset.yaml', 'w', encoding="utf-8") as file:
            yaml.dump(data, file, allow_unicode=True)
        print("标签", dict(obj_classes))
        print("有标签的文件数量", len(files))
 
 
if __name__ == '__main__':
    jpg_path = r"/home/aorus/Desktop/WJ/Code/ultralytics/ultralytics/models/yolo/Fair/mydata3/image1"       
    xml_path = r"/home/aorus/Desktop/WJ/Code/ultralytics/ultralytics/models/yolo/Fair/mydata3/annotations"  
    save_path = r"/home/aorus/Desktop/WJ/Code/ultralytics/ultralytics/models/yolo/Fair/mydata3/output"      
    deals = Dataset_Transforme_Yolov8(jpg_path, xml_path, save_path, divide=True)
    deals.voc2yolov8(0.9, 0.1)