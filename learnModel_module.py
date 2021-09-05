import os
import sys
import splitfolders
import configparser
from glob import glob
from os.path import isdir
"""
0901 dev note
obj.data 경로
"""
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DARKNET_FOLDER=THIS_FOLDER+'/darknet'
IMAGE_FOLDER = THIS_FOLDER+'/image'
DATASET_FOLDER = THIS_FOLDER+'/dataset'
TRAIN_FOLDER = DATASET_FOLDER+'/train'
VALID_FOLDER = DATASET_FOLDER+'/val'

def file_len(fname):#다크넷라벨안에 있는 건물 개수
  with open(fname) as f:
    for i, l in enumerate(f):
      pass
  return i + 1

def write_obj_file(classes):
    with open(DARKNET_FOLDER+'/data/obj.data','w') as f:
        f.write('classes = {}\n'.format(classes))#추가된 이미지 개수
        f.write('train = data/train.txt\n')
        f.write('valid = data/valid.txt\n')
        f.write('names = data/obj.names\n')
        f.write('backup = backup/')

def split_train_valid():
    splitfolders.ratio(IMAGE_FOLDER,output=DATASET_FOLDER,ratio=(0.8,0.2),group_prefix=2)
    print('success split train and valid dataset: '+DATASET_FOLDER)

"""dataset/train,valid/0,aug_0"""
def write_train_path():
    train_list = os.listdir(TRAIN_FOLDER)
    full_path=[]
    for folder in train_list:
        onedir = TRAIN_FOLDER+'/'+folder
        onedir_jpg_elem = glob(onedir+'/*.jpg')
        full_path=[os.path.join(onedir,f) for f in onedir_jpg_elem]
        with open(DARKNET_FOLDER+'/data/train.txt','a') as f:
            for jpg_path in full_path:
                f.write(jpg_path+'\n')

def write_valid_path():
    valid_list = os.listdir(VALID_FOLDER)
    full_path=[]
    for folder in valid_list:
        onedir = VALID_FOLDER+'/'+folder
        onedir_jpg_elem = glob(onedir+'/*.jpg')
        full_path=[os.path.join(onedir,f) for f in onedir_jpg_elem]
        with open(DARKNET_FOLDER+'/data/valid.txt','a') as f:
            for jpg_path in full_path:
                f.write(jpg_path+'\n')


"""
다크넷라벨안에 건물 정보 기록 어떻게 할건지
메인서버에서 받아서 _darknet.labels에 저장 이 파일 위치는 dataset/_darknet.labels
"""

def write_config_file():
    num_classes=file_len(DATASET_FOLDER+'/_darknet.labels')
    max_batches = num_classes*2000
    steps1 = .8 * max_batches
    steps2 = .9 * max_batches
    steps_str = str(steps1)+','+str(steps2)
    num_filters = (num_classes + 5) * 3
    print("writing config for a custom YOLOv4 detector detecting number of classes: " + str(num_classes))

    if os.path.exists(DARKNET_FOLDER+'/cfg/custom-yolov4-tiny-detector.cfg'):
        os.remove(DARKNET_FOLDER+'/cfg/custom-yolov4-tiny-detector.cfg')

    config = configparser.ConfigParser()
    config['net']={
        'batch':'64',
        'subdivisions':'64',
        'width':'416',
        'height':'416',
        'channels':'3',
        'momentum':'0.9',
        'decay':'0.0005',
        'angle':'0',
        'saturation':'1.5',
        'exposure':'1.5',
        'hue':'.1',
        'learning_rate':'0.00261',
        'burn_in':'1000',
        'max_batche':max_batches,
        'policy':'steps',
        'steps':steps_str,
        'scales':'.1,.1'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'32',
        'size':'3',
        'stride':'2',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'64',
        'size':'3',
        'stride':'2',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'64',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-1',
        'groups':'2',
        'group_id':'1'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'32',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'32',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-1,-2'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'64',
        'size':'1',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-6,-1'
    }
    config['maxpool']={
        'size':'2',
        'stride':'2'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'128',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-1',
        'groups':'2',
        'group_id':'1'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'64',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'64',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-1,-2'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'128',
        'size':'1',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-6,-1'
    }
    config['maxpool']={
        'size':'2',
        'stride':'2'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'256',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-1',
        'groups':'2',
        'group_id':'1'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'128',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'128',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-1,-2'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'256',
        'size':'1',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['route']={
        'layers':'-6,-1'
    }
    config['maxpool']={
        'size':'2',
        'stride':'2'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'512',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'256',
        'size':'1',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'512',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'size':'1',
        'stride':'1',
        'pad':'1',
        'filters':num_filters,
        'activation':'linear'
    }
    config['yolo']={
        'mask':'3,4,5',
        'anchors':'10,14,  23,27,  37,58,  81,82,  135,169,  344,319',
        'classes':num_classes,
        'num':'6',
        'jitter':'.3',
        'scale_x_y':'1.05',
        'cls_normalizer':'1.0',
        'iou_normalizer':'0.07',
        'iou_loss':'ciou',
        'ignore_thresh':'.7',
        'truth_thresh':'1',
        'random':'0',
        'nms_kind':'greedynms',
        'beta_nms':'0.6'
    }
    config['route']={
        'layers':'-4'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'128',
        'size':'1',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['upsample']={
        'stride':'2'
    }
    config['route']={
        'layers':'-1,23'
    }
    config['convolutional']={
        'batch_normalize':'1',
        'filters':'256',
        'size':'3',
        'stride':'1',
        'pad':'1',
        'activation':'leaky'
    }
    config['convolutional']={
        'size':'1',
        'stride':'1',
        'pad':'1',
        'filters':num_filters,
        'activation':'linear'
    }
    config['yolo']={
        'mask':'1,2,3',
        'anchors':'10,14,  23,27,  37,58,  81,82,  135,169,  344,319',
        'classes':num_classes,
        'num':'6',
        'jitter':'.3',
        'scale_x_y':'1.05',
        'cls_normalizer':'1.0',
        'iou_normalizer':'0.07',
        'iou_loss':'ciou',
        'ignore_thresh':'.7',
        'truth_thresh':'1',
        'random':'0',
        'nms_kind':'greedynms',
        'beta_nms':'0.6'
    }

    with open(DARKNET_FOLDER+'/cfg/custom-yolov4-tiny-detector.cfg','w') as f:
        config.write(f)
