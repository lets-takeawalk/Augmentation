# Augmentation
This is code for konkuk buildings augmentation with pascal voc format labels.

## Necessary data
- data: 416x416 images & pascal voc format xml label files

### augmentation_pascal_0820.py
- augmentaion main code
- applid key parameters: rain, Snowflakes, Clouds, FastSnowyLandscape, multiplyBritness...
- initial setting: you need to set 3 parameters. 
  - building_number is images and labels data folder number. 
  - img_folder_name is parent folder containing building_number folders. 
  - aug_count is output data count.  
```Python 
building_number=1 
img_folder_name='aug_0820'
aug_count=1000
```
- file_dic has jpg, xml file path information.
```Python
file_dic[file_name]={'jpg_path':file_path+'.jpg','xml_path':file_path+'.xml'}
file_dic[file1]={'jpg_path':'C:/Desktop/folder1/file1.jpg','xml_path':'C:/Desktop/folder1/file1.xml'}
```

### augmentation_module_0820.py
- loadXML(path):
  - parameter: xml file path
  - action: load xml file and get boundingbox coordinate(xmin,ymin,xmax,ymax)
  - return: xmin,ymin,xmax,ymax

- check_fix_Pixel(bbox):
  - parameter: aug_bbox coordinate
  - action: 
      - check coordinate range in 0~415. if it is out of range value, fix it.
      - if (xmin, xmax) or (ymin, ymax) are exchanged, fix it.
  - return: [x1,y1,x2,y2]

- check_original_Pixel(xml_path):
  - parameter: original xml file path
  - action: if original bounding box coordinates range is not in 0~415, fix it.
  
### changeClsNumwith_darknet.py
- Change yolo darknet format class number
- Use _darknet.labels file. _darknet.labels file have correct class number.
- If label text file have empty contents, print "Empty txt file: file" and continue process.

# Edit Label Text File
