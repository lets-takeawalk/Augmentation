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
def write_cfg():
    num_classes=file_len(DATASET_FOLDER+'/_darknet.labels')
    max_batches = num_classes*2000
    steps1 = .8 * max_batches
    steps2 = .9 * max_batches
    steps_str = str(steps1)+','+str(steps2)
    num_filters = (num_classes + 5) * 3
    if os.path.exists(DARKNET_FOLDER+'/cfg/custom-yolov4-tiny-detector.cfg'):
        os.remove(DARKNET_FOLDER+'/cfg/custom-yolov4-tiny-detector.cfg')
    cfg_f=''
    with open(DARKNET_FOLDER+'/cfg/initial_cfg.txt','r') as f:
        cfg_f=f.read()
        cfg_f=cfg_f.replace('{num_classes}',str(num_classes))
        cfg_f=cfg_f.replace('{max_batches}',str(max_batches))
        cfg_f=cfg_f.replace('{steps1}',str(steps1))
        cfg_f=cfg_f.replace('{steps2}',str(steps2))
        cfg_f=cfg_f.replace('{steps_str}',str(steps_str))
        cfg_f=cfg_f.replace('{num_filters}',str(num_filters))
        print(cfg_f)

    with open(DARKNET_FOLDER+'/cfg/custom-yolov4-tiny-detector.cfg','w') as f:
        f.write(cfg_f)
        print('SUCCESS write custom-yolov4-tiny-detector.cfg')
