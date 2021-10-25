from augmentation_module_0820 import loadXML, save_label_xml_format
from glob import glob
import os
"""
2021-10-25 기준 새로 찍은 건물
17,18,19,20,20-1,23
roboflow에서 pascal voc 형식으로 추출한 좌표 형식을
[cls_num xtop,ytop,xbottom,ybottom] 형식의 txt 파일로 변환
"""
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
XML_FOLDER = THIS_FOLDER + './xml_file'
folder_list=os.listdir(XML_FOLDER)

print(folder_list)

for folder in folder_list:
    xml_list=glob(XML_FOLDER+'/'+folder+'/*.xml')
    for xml in xml_list:
        coordinates=loadXML(xml)
        print(coordinates)
        break
    break