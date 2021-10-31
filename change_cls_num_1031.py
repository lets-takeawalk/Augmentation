from glob import glob
import os
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR=THIS_FOLDER+'/aug_1031_except6'
file_list=os.listdir(IMAGE_DIR)
for file in file_list:
    if int(file)<6:continue
    txt_list=glob(IMAGE_DIR+'/'+file+'/*.txt')
    for txt in txt_list:
        coordinates=''
        with open(txt,'r') as f:
            coordinates=f.read()
        coordinates=coordinates.split(' ')
        coordinates[0]=str(int(coordinates[0])-1)
        with open(txt,'w') as f:
            f.write(' '.join(coordinates))
