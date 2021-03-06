import os
import torch
import time
import numpy as np
from print_utils import print_log_message, print_info_message
from eval_utils import AverageMeter, MIOU
from data_loader import LabelDataset
from config import *

def get_iou_metric():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    
    print_info_message("Evalution of IoU")
    
    true_ds = LabelDataset(TRUE_LABEL_DIR, TRUE_FLAG_CONVERT)
    pred_ds =  LabelDataset(PRED_LABEL_DIR, PRED_FLAG_CONVERT)

    true_dl = torch.utils.data.DataLoader(true_ds, batch_size=BATCH_SIZE, shuffle=False) 
    pred_dl = torch.utils.data.DataLoader(pred_ds, batch_size=BATCH_SIZE, shuffle=False)
    
    inter_meter = AverageMeter()
    union_meter = AverageMeter()
    batch_time = AverageMeter()
    
    end = time.time()
    miou_class = MIOU(NUM_CLASSES)

    for i, (true_target, pred_target) in enumerate(zip(true_dl, pred_dl)):

        true_target = true_target.to(device=device)
        pred_target = pred_target.to(device=device)

        inter, union = miou_class.get_iou(pred_target, true_target)
        inter_meter.update(inter)
        union_meter.update(union)

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if (i + 1) % 10 == 0:  
            iou = inter_meter.sum / (union_meter.sum + 1e-10)
            miou = iou.mean() * 100
            print_log_message("[%d/%d]\t\tBatch Time:%.4f\t\tmiou:%.4f" %
                (i, len(true_dl), batch_time.avg, miou))
    

    iou = inter_meter.sum / (union_meter.sum + 1e-10)
    for i, iou_per_class in enumerate(iou):
        print_info_message("%s IoU: %.4f" % (CLASSES[i], iou_per_class))
    
    miou = iou.mean() * 100
    print_info_message('Mean IoU: {0:.4f}'.format(miou))

    return iou, miou

if __name__ == "__main__":    
    get_iou_metric()