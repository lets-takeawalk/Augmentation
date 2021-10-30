import xml.etree.ElementTree as Et
from xml.etree.ElementTree import Element, SubElement, ElementTree
from glob import glob
import os
"""
2021-10-25 기준 새로 찍은 건물
17,18,19,20,20-1,23
roboflow에서 pascal voc 형식으로 추출한 좌표 형식을
[cls_num xtop,ytop,xbottom,ybottom] 형식의 txt 파일로 변환
"""
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
XML_FOLDER = THIS_FOLDER+'/1030_building'
folder_list=os.listdir(XML_FOLDER)

def loadXML(path):#xml파일에서 좌표값 추출 (xmin,ymin,xmax,ymax), filename
    xml=open(path,'r')
    tree = Et.parse(xml)
    root = tree.getroot()
    file_name = root.find("filename").text
    object = root.findall("object")

    for _object in object:
        name = _object.find("name").text
        bndbox = _object.find("bndbox")
        xmin = bndbox.find("xmin").text
        ymin = bndbox.find("ymin").text
        xmax = bndbox.find("xmax").text
        ymax = bndbox.find("ymax").text

        # print("class : {}\nxmin : {}\nymin : {}\nxmax : {}\nymax : {}\n".format(name, xmin, ymin, xmax, ymax))
        return (xmin,ymin,xmax,ymax),file_name


for folder in folder_list:
    xml_list=glob(XML_FOLDER+'/'+folder+'/*.xml')
    for xml in xml_list:
        print('xml',xml)
        coordinates,file_name=loadXML(xml)#return xmin,ymin,xmax,ymax
        file_name=file_name.rstrip('.jpg')
        print('file_name',file_name)
        with open(XML_FOLDER+'/'+folder+'/'+file_name+'.txt','w') as f:
            f.write(' '.join(coordinates))

        os.remove(xml)
