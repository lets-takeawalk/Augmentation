import os
import sys
import splitfolders
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

#폴더갯수 확인 후 클래스 갯수 체크
def get_class_count():
    classes=0
    for f in glob(IMAGE_FOLDER+'/*'):
        if isdir(f):
            classes+=1
    classes=int(classes/2)
    print('class count: ',classes)
    return classes

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

    # with open(DARKNET_FOLDER+'/data/train.txt','w') as f:
