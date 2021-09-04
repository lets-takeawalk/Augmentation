#-*- encoding: utf-8 -*-
import augmentation_module_0820 as am
import cv2
import os
import sys
import json
import numpy as np
import imgaug as ia
from glob import glob
from PIL import Image
import imgaug.augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
######################################################
# folder_list=[0,1,2]#라벨번호폴더 리스트
# building_number=folder_list[0]
# #building_number=0#라벨번호#cls_num
# img_folder_name='image'#씨드이미지폴더이름(image/0/ -.jpg -.txt)
# aug_count=5#어그멘테이션 갯수 설정
######################################################

#nodejs 메인서버에서 파라메타 argv="건물이름1,건물이름2" "1000" 보내는 경우
# folder_list=list(map(int,sys.argv[1].split(',')))
folder_list=sys.argv[1].split(',')
aug_count=int(sys.argv[2])
for folder in folder_list:
    augmentation(folder,'image',aug_count)

sometimes = lambda aug: iaa.Sometimes(0.5, aug)
seq = iaa.Sequential(
    [
        iaa.Sometimes(0.2,[
        iaa.Rain(drop_size=(0.10,0.20),speed=(0.1,0.3)),
        iaa.MultiplyBrightness((0.3, 1.0))
        ]),
        iaa.Sometimes(0.3, [
            iaa.MultiplyBrightness((0.25, 1.0))
        ]),
        iaa.Sometimes(0.2,[
        iaa.Snowflakes(flake_size=(0.1, 0.4), speed=(0.01, 0.05)),
        iaa.Clouds((5,15))
        ]),
        iaa.Sometimes(0.3,[
            iaa.Fliplr(0.5), # horizontally flip 50% of all images
            iaa.Flipud(0.2) # vertically flip 20% of all images
        ]),
        iaa.Sometimes(0.8,[
            iaa.CropAndPad(
            percent=(-0.05, 0.1),
            pad_mode=ia.ALL,
            pad_cval=(0, 255)
        )]),
        iaa.Sometimes(0.5,[
        iaa.Affine(scale=(0.5,1.5)),
        ]),#zoom in,out
        iaa.Sometimes(0.2,[
        iaa.Affine(
            scale={"x": (0.7, 1.3), "y": (0.7, 1.3)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-45, 45),
            shear=(-16, 16),
            order=[0, 1],
            cval=(0, 255),
            mode=ia.ALL
        )]),
        iaa.Sometimes(0.1,[
        iaa.SomeOf((0, 3),
            [
                iaa.FastSnowyLandscape(lightness_threshold=[200, 255],lightness_multiplier=(1.2,1.5)),
                sometimes(iaa.Superpixels(p_replace=(0, 1.0), n_segments=(20, 200))),
                iaa.OneOf([
                    iaa.GaussianBlur((0, 2.0)),
                    iaa.AverageBlur(k=(2, 5)),
                    iaa.MedianBlur(k=(3, 11)),
                ]),
                iaa.Sharpen(alpha=(0, 1.0), lightness=(0.75, 1.5)),
                iaa.Emboss(alpha=(0, 1.0), strength=(0, 1.5)),
                iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
                iaa.OneOf([
                    iaa.Dropout((0.01, 0.1), per_channel=0.5),
                    iaa.CoarseDropout((0.03, 0.15), size_percent=(0.02, 0.05), per_channel=0.2),
                ]),
                iaa.Invert(0.05, per_channel=True),
                iaa.Add((-10, 10), per_channel=0.5),
                iaa.AddToHueAndSaturation((-20, 20)),
  iaa.OneOf([
                iaa.Multiply((0.5, 1.5), per_channel=0.5),
                iaa.FrequencyNoiseAlpha(
                        exponent=(-4, 0),
                        first=iaa.Multiply((0.5, 1.5), per_channel=True),
                        second=iaa.ContrastNormalization((0.5, 2.0))
                    )
                ]),
                  iaa.Grayscale(alpha=(0.0, 1.0)),
                sometimes(iaa.ElasticTransformation(alpha=(0.5, 3.5), sigma=0.25)),
                sometimes(iaa.PiecewiseAffine(scale=(0.01, 0.05))),
                sometimes(iaa.PerspectiveTransform(scale=(0.01, 0.1)))
            ],
            random_order=True
        )
        ])
    ],
    random_order=True
)
def augmentation(building_name='none',img_folder_name='image',aug_count=1):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    AUG_BFR_IMG_FOLDER=THIS_FOLDER+'/'+img_folder_name+'/'+building_name
    AUG_AFT_IMG_FOLDER=THIS_FOLDER+'/'+img_folder_name+'/aug_'+building_name
    am.create_folder(AUG_AFT_IMG_FOLDER)

    #make jpg,txt path info dictionary
    jpg_list=glob(AUG_BFR_IMG_FOLDER+'/*.jpg')
    # img_list=glob()#jpg,jpeg,png
    file_path_list=[f.rstrip('.jpg') for f in jpg_list]
    file_name_list=[]
    file_dic={} #{filename: {jpg_path: '', xml_path: ''}}
    for file_path in file_path_list:
        file_name=file_path.split(building_name+'\\')[1]
        file_name_list.append(file_name)
        file_dic[file_name]={'jpg_path':file_path+'.jpg','txt_path':file_path+'.txt'}

    # json_str=json.dumps(file_dic,indent=4)
    # print(json_str)

    cnt=1
    while cnt<aug_count:
        for file_name, path in file_dic.items():
            if cnt>aug_count:exit(0)
            #check original xml and edit it
            am.check_original_pixel_coordinate(path['txt_path'])

            images=am.load_images_from_folder(path['jpg_path'])
            cls_num,xtop,ytop,xbottom,ybottom=am.load_pixel_coordinate(path['txt_path'])
            bbox=[ia.BoundingBox(x1=xtop,y1=ytop,x2=xbottom,y2=ybottom)]
            try:
                img_aug,bbox_aug=seq(images=images,bounding_boxes=bbox)
                print(bbox_aug)
            except:
                continue

            checked_bbox_aug=am.check_aug_pixel_coordinate(bbox_aug)
            yolo_format=am.pixel_to_yolo(cls_num,list(map(float,checked_bbox_aug)))
            #욜로형식범위 벗어날경우
            save_name=file_name+'_'+str(cnt)
            save_path=AUG_AFT_IMG_FOLDER+'/'+save_name

            # am.save_label_xml_format(checked_bbox_aug,save_name,)
            am.save_aug_img(img_aug,save_path)
            am.save_label_pixel_to_yolo(yolo_format,save_path)

            cnt+=1
