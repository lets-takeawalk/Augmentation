# Augmentation
This is code for konkuk buildings augmentation with pascal voc format labels.

## Necessary data
- data: 416x416 images & pascal voc format xml label files

### augmentation_pascal_0820.py
- augmentaion main code
- applid key parameters: rain, Snowflakes, Clouds, FastSnowyLandscape, multiplyBritness...
- initial setting: you need to set 3 parameters. building_number is images and labels data folder number. img_folder_name is parent folder containing building_number folders. aug_count is output data number.  
```Python 
building_number=1 
img_folder_name='aug_0820'
aug_count=1000
```
- file_dic has jpg, xml file path information.
```Python
file_dic[file_name]={'jpg_path':file_path+'.jpg','xml_path':file_path+'.xml'}
```

### augmentation_module_0820.py
- loadXML(path):
  - parameter: xml file path
  - action: 
### changeClsNumwith_darknet.py
