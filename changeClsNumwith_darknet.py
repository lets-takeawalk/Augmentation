import os
from glob import glob
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
################################
aug_folder_name='aug_res' #어그멘테이션 폴더들이 들어있는 상위폴더
"""
aug_res
    -aug_1
        -train
        -valid
    -aug_2
        -train
        -valid
    ...
"""
################################
directories = list(filter(os.path.isdir, glob(THIS_FOLDER+'/'+aug_folder_name+'/*')))
for aug_dir in directories:
    print(aug_dir)
    train_dir=aug_dir+'/train'
    valid_dir=aug_dir+'/valid'
    train_valid_list=[train_dir,valid_dir]

    for one_dir in train_valid_list:
        label_file_path=glob(one_dir+'/*.labels')
        try:
            with open(label_file_path[0],'r') as f:
                label_num=f.read()
                print('label_num:',label_num)
        except:
            print('_darknet.labels file not found')
            print('not change label number: ', aug_dir)

        txt_file_list=glob(one_dir+'/*.txt')

        for txt_file in txt_file_list:
            print(txt_file)
            info=''
            with open(txt_file, 'r') as f:
                info=f.readline().split()
                if info!='':
                    info[0]=label_num
                else:
                    print("Empty txt file: ",text_file)
                    continue

            with open(txt_file, 'w') as f:
                change_str=' '.join(info)
                f.write(change_str)
                print(change_str)
