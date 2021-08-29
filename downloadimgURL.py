import augmentation_module_0820 as am
import requests
import json
import os
import urllib.request as urlr
import numpy as np
import cv2
import glob
from PIL import Image
"""
0828 dev note
json 파싱
imgURL 받음
이미지 다운로드 저장이름: url의 마지막 슬라이스 다음 http://.../name.jpg
이미지 사이즈 416x416으로 변경 필수(클때는 자르면 되는데 사이즈가 이것보다 작을때 고려해야->패딩?X ->알아서 늘려줌(해결))
리사이즈할때 바운딩박스 정보는 어떻게 수정?
txt 415 사이즈 넘는 데이 간혹 있음 이것도 수정(원래 어그멘테이션 과정에서 수정했었음)
다운받고 new폴더에 저장후 변경 후 사이즈 다 확인하고 옮김? 완전 탐색 너무 오래걸리는거 아님?
어그멘테이션 하기 직전에 xml 형식으로 저장해야됨
한 폴더에 이미지랑 xml 저장해야하는데, xml 파싱 형식 바꿔야겠네(굳이 xml 형식 필요없음)
그냥 픽셀 값이랑 클래스 번호만 전달하면 어그멘테이션 시킬 수 있음
마지막에 욜로 형식으로 변환하고
그리고 결과물 나온 pixel값을 라벨 포함 yolo darknet(0.0~1.0) 형식으로도 생성하고 저장해야됨
+나중에 확장자 이슈 발생 가능 jpg,jpeg,png 확장자 리스트 생성해두는게 좋음
os.path.splitext()[1]==확장자(.jpg)
"""
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
TEST_JSON=THIS_FOLDER+"/test.json"
IMAGE_FORMAT=['.jpg','.jpeg','.png']

def load_json(path):
    with open(path,encoding='utf-8') as json_file:
        return json.load(json_file)

def parse_imgURL(json_data):
    URL_lst=[]
    buildingInfoNum=len(json_data['buildingInfo'])
    for building in json_data['buildingInfo']:
        for img in building['imgInfos']:#지금은 전체 빌딩 이미지 주소 가져옴
            if img['imgURL']:
                URL_lst.append(img['imgURL'])

    return URL_lst

def download_img_with_URL(URL):
    save_name=URL.split('/')[-1]
    save_path=THIS_FOLDER+'/'+save_name
    with open(save_path,'wb') as f:
        f.write(urlr.urlopen(URL).read())
        print('download at: '+save_path)

    return save_path

# def resize_img_416(img_path):
#     try:
#         img=Image.open(img_path)
#         img_resize=img.resize((416,416))
#         title,ext=os.path.splitext(img_path)
#         img_resize.save(title+'_416'+ext)
#         print('success img resize: ',img_path)
#     except:
#         print('fail img resize: ',img_path)
# 애초에 보내주는 이미지 사이즈 416으로 변경


"""main"""
json_data=load_json(TEST_JSON)
URLs=parse_imgURL(json_data)
print(URLs)
resize_img_416(download_img_with_URL(URLs[0]))

# am.creat_folder()#이미지 id에 따라서 폴더 생성 후 저장
