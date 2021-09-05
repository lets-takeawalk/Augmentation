import learnModel_module as lm
import os
import sys
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
DARKNET_FOLDER = THIS_FOLDER+'/darknet'
# IMAGE_FOLDER = THIS_FOLDER+'/image'
DATASET_FOLDER = THIS_FOLDER+'/dataset'
TRAIN_FOLDER = DATASET_FOLDER+'/train'
VALID_FOLDER = DATASET_FOLDER+'/val'

building_cnt=lm.file_len(DATASET_FOLDER+'/_darknet.labels')
lm.write_obj_file(building_cnt)
lm.split_train_valid()
lm.write_train_path()
lm.write_valid_path()
lm.write_config_file()#config 모듈 같은 섹션은 덮어씌워짐 해결책 찾기

#498디텍딩시작
"""
다크넷 data/obj.names->tflite/data/classes/에 복사
tflite에 core/config.py를 coco.names->obj.name로 변경
save_model.py실행

"""
