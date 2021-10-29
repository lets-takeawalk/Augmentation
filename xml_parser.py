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
XML_FOLDER = THIS_FOLDER+'/xml_file'
folder_list=os.listdir(XML_FOLDER)

# print(folder_list)

for folder in folder_list:
    xml_list=glob(XML_FOLDER+'/'+folder+'/*.xml')
    for xml in xml_list:
        file_name=xml.split(folder)[1].lstrip('\\').rstrip('.xml')
        print(file_name)
        coordinates=loadXML(xml)#return xmin,ymin,xmax,ymax
        with open(XML_FOLDER+'/'+folder+'/'+file_name+'.txt','w') as f:
            f.write(' '.join(coordinates))

        os.remove(xml)
        # with open()
        # print(coordinates)
        #xtop,ytop,xbottom,ybottom
        #txt파일 만들고 xml 파일 지우기
        # print(xml)
