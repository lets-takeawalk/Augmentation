import sys
import os
import cv2
import numpy as np
import imgaug as ia
import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, SubElement, ElementTree
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage

def createFolder(directory):#폴더생성
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

def save_aug_xml(bbox,save_name,xml_path,save_path):
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
