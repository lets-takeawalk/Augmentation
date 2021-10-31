import os
import splitfolders
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
IMAGE_FOLDER = THIS_FOLDER+'/aug_1031_all'
OUTPUT_FOLDER = THIS_FOLDER+'/aug_1031_all_output'
splitfolders.ratio(IMAGE_FOLDER,output=OUTPUT_FOLDER,ration=(0.8,0.2),group_prefix=2)