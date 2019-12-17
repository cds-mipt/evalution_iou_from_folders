import numpy as np
import os
from PIL import Image
from tqdm import tqdm
from print_utils import print_info_message, print_error_message
    

def convert_from_color_segmentation(arr_3d, palette):
    height = arr_3d.shape[0]
    width = arr_3d.shape[1]
    arr_2d = np.zeros((height, width), dtype=np.uint8)

    for c, i in palette.items():
        m = np.all(arr_3d == np.array(c).reshape(1, 1, 3), axis=2)
        arr_2d[m] = i

    return arr_2d


def convert_mask(label_dir, save_dir, palette):
    '''
    To remove the color-map in the masks.
    If your dataset have n classes including background, you should label all pixels from 0 to n-1.
    
    args:
        label_dir: directory of the 3 ch masks.
        save_dir: directory for converted masks.
        palette: mapping "color to number of class". Example:
            palette[(0, 0, 0)] = 0 #backgound
            palette[((0, 0, 255)] = 2 #car and etc.
    
    '''
    
    if os.path.isdir(save_dir):
        print_error_message(f'Folder "{save_dir}" alread exists. Delete the folder and re-run the code!!!"')
    else:
        os.mkdir(save_dir)

    label_files = os.listdir(label_dir)
    label_files.sort()

    for l_f in tqdm(label_files):
        path = os.path.join(label_dir, l_f)
        arr = np.array(Image.open(path))
        
        arr = arr[:,:,0:3]
        arr_2d = convert_from_color_segmentation(arr, palette)
        
        new_path = os.path.join(save_dir, l_f)
        Image.fromarray(arr_2d).save(new_path)
        
    print_info_message('Converted masks were saved in the dir: {}'.format(save_dir))