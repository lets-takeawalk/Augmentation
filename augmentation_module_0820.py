import sys
import os
import cv2
import copy
import numpy as np
import imgaug as ia
import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, SubElement, ElementTree
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

IMAGE_SIZE=416

def create_folder(directory):#폴더생성
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('ERROR creating driectory: '+directory)

"""https://deepbaksuvision.github.io/Modu_ObjectDetection/posts/02_01_PASCAL_VOC.html"""
def loadXML(path):#xml파일에서 좌표값 추출 (xmin,ymin,xmax,ymax)
    xml=open(path,'r')
    tree = Et.parse(xml)
    root = tree.getroot()
    object = root.findall("object")
    for _object in object:
        name = _object.find("name").text
        bndbox = _object.find("bndbox")
        xmin = bndbox.find("xmin").text
        ymin = bndbox.find("ymin").text
        xmax = bndbox.find("xmax").text
        ymax = bndbox.find("ymax").text

        # print("class : {}\nxmin : {}\nymin : {}\nxmax : {}\nymax : {}\n".format(name, xmin, ymin, xmax, ymax))
        return xmin,ymin,xmax,ymax

def load_images_from_folder(path):
    images = []
    img = cv2.imread(path)
    input_img = img[np.newaxis, :, :, :]
    if img is not None:
        images.append(input_img)
    return images[0]

def save_aug_img(img,save_path):#이미지배열,파일이름
    save_path+='.jpg'
    for n in img:
        cv2.imwrite(save_path,n)
    print('save aug image: ',save_path)

def save_label_xml_format(bbox,save_name,xml_path,save_path):
    save_path+='.xml'

    xml=open(xml_path,'rt')
    tree = Et.parse(xml)
    root=tree.getroot()

    tg_name=root.find("filename")
    tg_path=root.find("path")
    tg_objs=root.find("object")

    tg_name.text=save_name
    tg_path.text=save_name

    bndbox = tg_objs.find("bndbox")
    bndbox.find("xmin").text=str(int(bbox[0]))
    bndbox.find("ymin").text=str(int(bbox[1]))
    bndbox.find("xmax").text=str(int(bbox[2]))
    bndbox.find("ymax").text=str(int(bbox[3]))

    tree.write(save_path)
    print('save aug xml: ',save_path)

def check_fix_Pixel(bbox):#415가 최대,마이너스일 때 0
    x1y1x2y2=[bbox[0].x1,bbox[0].y1,bbox[0].x2,bbox[0].y2]
    x1y1x2y2=list(map(int,x1y1x2y2))
    print('bfr',x1y1x2y2)
    for idx,pix in enumerate(x1y1x2y2):
        if pix<0:
            x1y1x2y2[idx]=0
        elif pix>415:
            x1y1x2y2[idx]=415

    if x1y1x2y2[0]>x1y1x2y2[2]:
        temp=x1y1x2y2[0]
        x1y1x2y2[0]=x1y1x2y2[2]
        x1y1x2y2[2]=temp
    if x1y1x2y2[1]>x1y1x2y2[3]:
        temp=x1y1x2y2[1]
        x1y1x2y2[1]=x1y1x2y2[3]
        x1y1x2y2[3]=temp

    print('atf',x1y1x2y2)
    return x1y1x2y2

def check_orginal_Pixel(xml_path):#원래 이미지의 바운딩박스 범위 재설정
    edit_cnt=0
    xml=open(xml_path,'rt')
    tree=Et.parse(xml)
    root=tree.getroot()
    object=root.find("object")

    bndbox=object.find("bndbox")
    xmin = bndbox.find("xmin").text
    ymin = bndbox.find("ymin").text
    xmax = bndbox.find("xmax").text
    ymax = bndbox.find("ymax").text

    bbox=[xmin,ymin,xmax,ymax]
    bbox=list(map(int,bbox))

    for idx,pix in enumerate(bbox):
        if pix>415:
            bbox[idx]=415
            edit_cnt+=1
        elif pix<0:
            bbox[idx]=0
            edit_cnt+=1

    bndbox.find("xmin").text=str(bbox[0])
    bndbox.find("ymin").text=str(bbox[1])
    bndbox.find("xmax").text=str(bbox[2])
    bndbox.find("ymax").text=str(bbox[3])

    tree.write(xml_path)
    if edit_cnt:
        print('edit original xml: ',xml_path)


#0829
def check_original_pixel_coordinate(pixel_txt_path):
    try:
        with open(pixel_txt_path,'r') as f:
            #cls_num,xtop,ytop,xbottom,ybottom
            origin_bbox=list(map(int,f.read().split()))

    except:
        print('[FAIL]pixel txt file is not open'+pixel_txt_path)

    #if pixel coordinate are out of range in [0,415], fix it
    fix_bbox=copy.deepcopy(origin_bbox)
    if 0>origin_bbox[1]: fix_bbox[1]=0
    if 0>origin_bbox[2]: fix_bbox[2]=0
    if 415<origin_bbox[3]: fix_bbox[3]=415
    if 415<origin_bbox[4]: fix_bbox[4]=415

    if fix_bbox!=origin_bbox:
        try:
            with open(pixel_txt_path,'w') as f:
                fix_bbox=' '.join(map(str,fix_bbox))
                f.write(fix_bbox)
        except:
            print('[FAIL]change original pixel txt file: '+pixel_txt_path)
            with open(pixel_txt_path,'w') as f:
                f.write(origin_bbox)

def load_pixel_coordinate(pixel_txt_path):
    try:
        with open(pixel_txt_path,'r') as f:
            #cls_num,xtop,ytop,xbottom,ybottom
            bbox=list(map(int,f.read().split()))
            cls_num=bbox[0]
            xtop=bbox[1]
            ytop=bbox[2]
            xbottom=bbox[3]
            ybottom=bbox[4]
    except:
        print('[FAIL]pixel txt file is not open'+pixel_txt_path)

    return cls_num,xtop,ytop,xbottom,ybottom

def check_aug_pixel_coordinate(aug_bbox):
    xtop=aug_bbox[0].x1
    ytop=aug_bbox[0].y1
    xbottom=aug_bbox[0].x2
    ybottom=aug_bbox[0].y2

    if xtop<0: xtop=0.0
    if ytop<0: ytop=0.0
    if xbottom>415: xbottom=415.0
    if ybottom>415: ybottom=415.0
    if xtop>xbottom: xtop,xbottom=xbottom,xtop
    if ytop>ybottom: ytop,ybottom=ybottom,ytop

    bbox=[xtop,ytop,xbottom,ybottom]

    print(bbox)
    return bbox

def pixel_to_yolo(cls_num,bbox_aug):
    dw=1./IMAGE_SIZE
    dh=1./IMAGE_SIZE
    xcenter=(bbox_aug[0]+bbox_aug[2])/2.0-1
    ycenter=(bbox_aug[1]+bbox_aug[3])/2.0-1
    width=bbox_aug[2]-bbox_aug[1]#xbottom-xtop
    height=bbox_aug[3]-bbox_aug[0]#ybottom-ytop
    xcenter*=dw
    width*=dw
    ycenter*=dh
    height*=dh

    #(0.0 to 1.0]
    if xcenter+(width/2)>1.0:
        temp=2*(xcenter+(width/2)-1.0)+0.0001
        width-=temp
    if ycenter+(height/2)>1.0:
        temp=2*(ycenter+(height/2)-1.0)+0.0001
        height-=temp
    if xcenter-(width/2)<=0.0:
        temp=2*abs(xcenter-(width/2))+0.0001
        width-=temp
    if ycenter-(height/2)<=0.0:
        temp=2*abs(ycenter-(height/2))+0.0001
        height-=temp

    return [cls_num,xcenter,ycenter,width,height]

def save_label_pixel_to_yolo(yolo_format,save_path):
    yolo_str=' '.join(map(str,yolo_format))
    try:
        with open(save_path+'.txt','w') as f:
            f.write(yolo_str)
            print(save_path,yolo_str)
    except:
        print('[FAIL]writing yolo format coordinate at '+save_path+', yolo_str: '+yolo_str)
