#-*- encoding: utf-8 -*-
import cv2
import os
"""
dev note
[keyboard]
1. d: delete image (save to delimg.txt)
2. k: edit image (save to editimg.txt)
3. n: next image
4. z: stop!

[file]
1. del_f: delete file number list
2. edit_f: edit file number list
3. current_r_ptr: current file number pointer for read
4. current_w_ptr: current file number pointer for write
"""

THIS_FOLDER=os.path.dirname(os.path.abspath(__file__))
IMG_FOLDER=THIS_FOLDER+'/konkukimg0712bbox/13/'#need to hardcoding image_folder
file_list = os.listdir(IMG_FOLDER)

allFile=len(file_list)#10643
print(file_list)

current_r_ptr = open(THIS_FOLDER+"/konkukimg0712bbox/currentimgPtr.txt","r")
last_file_name = current_r_ptr.readline().rstrip('\n')
current_r_ptr.close()
print(current_r_ptr)
if last_file_name=='':
    last_file_name=file_list[0]

del_f = open(THIS_FOLDER+"/konkukimg0712bbox/delimg0712.txt","a")
edit_f = open(THIS_FOLDER+"/konkukimg0712bbox/editimg0712.txt","a")
current_w_ptr = open(THIS_FOLDER+"/konkukimg0712bbox/currentimgPtr.txt","w")


current_idx=file_list.index(last_file_name)#-1
file_list = file_list[current_idx:]

for filename in file_list:
    oneimg = cv2.imread(IMG_FOLDER+filename)
    dst=cv2.resize(oneimg,dsize=(700,700))
    cv2.imshow(filename,dst)
    cv2.resizeWindow(filename,700,700)

    key = cv2.waitKey()
    if key == ord('d'):
        cv2.imshow(filename, oneimg)
        del_f.write(filename.rstrip('.jpg')+'\n')
        cv2.destroyAllWindows()
    elif key == ord('k'):
        cv2.imshow(filename, oneimg)
        edit_f.write(filename.rstrip('.jpg')+'\n')
        cv2.destroyAllWindows()
    elif key == ord('n'):
        cv2.imshow(filename, oneimg)
        cv2.destroyAllWindows()
    elif key == ord('z'):
        current_w_ptr.write(filename)
        print(filename)
        break

del_f.close()
edit_f.close()
current_w_ptr.close()

print('allFile',allFile,'complete',allFile-len(file_list),'remaining',len(file_list))
