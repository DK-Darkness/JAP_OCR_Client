#coding=utf-8
 
import os
import tensorflow as tf
from PIL import Image
import sys

def creat_tf(imgpath):
 
    cwd = os.getcwd()
    classes = os.listdir(cwd + imgpath)
    class_map = {}
    # 此处定义tfrecords文件存放
    writer = tf.io.TFRecordWriter("train.tfrecords")
    for index, name in enumerate(classes):
        class_path = cwd + imgpath + name + "/"
        class_map[index] = name
        print(class_path)
        if os.path.isdir(class_path):
            for img_name in os.listdir(class_path):
                img_path = class_path + img_name
                img = Image.open(img_path)
                img = img.resize((224, 224))
                img = img.convert('RGB')
                img_raw = img.tobytes()
             
                example = tf.train.Example(features=tf.train.Features(feature={
                'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
            }))
                writer.write(example.SerializeToString())  
                print(img_name)
    writer.close()
    txtfile = open('label.txt','w+')
    for key in class_map.keys():
        txtfile.writelines(str(key)+":"+class_map[key]+"\n")
    txtfile.close()

 
if __name__ == '__main__':
    imgpath = '/extract/'
    creat_tf(imgpath)

    
 
    
