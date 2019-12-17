import torch
from PIL import Image
import numpy as np
import os

class LabelDataset(torch.utils.data.Dataset):

    def __init__(self, label_root_dir):
        super(LabelDataset, self).__init__()
        
        self.label_root_dir = label_root_dir
        self.mask_paths = os.listdir(label_root_dir)
        self.mask_paths.sort()

    def __len__(self):
        return len(self.mask_paths)

    def __getitem__(self, index):
        mask_path = os.path.join(self.label_root_dir, self.mask_paths[index])
        label_img = Image.open(mask_path)
        label_img = torch.LongTensor(np.array(label_img).astype(np.int64))

        return label_img

class AverageMeter(object):
    """Computes and stores the average and current value"""
    
    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count
        
        
class MIOU(object):
    def __init__(self, num_classes):
        self.num_classes = num_classes
        self.epsilon = 1e-6

    def get_iou(self, pred, target):

        if pred.device == torch.device('cuda'):
            pred = pred.cpu()
        if target.device == torch.device('cuda'):
            target = target.cpu()
        
        pred = pred.type(torch.ByteTensor)
        target = target.type(torch.ByteTensor)

        # shift by 1 so that 255 is 0
        pred += 1
        target += 1

        pred = pred * (target > 0)
        inter = pred * (pred == target)
        area_inter = torch.histc(inter.float(), bins=self.num_classes, min=1, max=self.num_classes)
        area_pred = torch.histc(pred.float(), bins=self.num_classes, min=1, max=self.num_classes)
        area_mask = torch.histc(target.float(), bins=self.num_classes, min=1, max=self.num_classes)
        area_union = area_pred + area_mask - area_inter + self.epsilon

        return area_inter.numpy(), area_union.numpy()