from glob import glob
import os
import sys
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = THIS_FOLDER + '/1030_aug'
file_list=os.listdir(IMAGE_DIR)
for file in file_list:
    if not file.isdigit():continue
    cls_num=file
    txt_list=glob(IMAGE_DIR+'/'+file+'/*.txt')
    print('cls_num:',cls_num)
    for path in txt_list:
        coordinates=''
        with open(path,'r') as f:
            coordinates=f.read()

        if len(coordinates.split(' '))==4:
            with open(path,'w') as f:
                f.write(cls_num+' '+coordinates)
                print(cls_num+' '+coordinates)
