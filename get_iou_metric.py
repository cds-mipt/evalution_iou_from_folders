import os
import torch
import time
from convert_mask import convert_mask
from get_classes_palette import get_classes_palette
from print_utils import print_log_message, print_info_message
from eval_utils import LabelDataset, AverageMeter, MIOU


def get_iou_metric(classes,
                   palette,
                   true_label_dir = None,
                   predicted_label_dir = None,
                   true_convert = './t_folder', 
                   predicted_convert = './p_folder',
                   batch_size = 16):
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    num_classes = len(classes)
    
    if true_label_dir != None:
        print_info_message("Converting true masks")
        convert_mask(label_dir = true_label_dir, 
                     save_dir = true_convert, 
                     palette = palette)
        
    if predicted_label_dir != None:
        print_info_message("Converting predicted masks")
        convert_mask(label_dir = predicted_label_dir, 
                     save_dir = predicted_convert, 
                     palette = palette)
    
    print('\n')
    print_info_message("Evalution of IoU")
    
    t_dataset = LabelDataset(label_root_dir = true_convert)
    p_dataset =  LabelDataset(label_root_dir = predicted_convert)

    true_dataset_loader = torch.utils.data.DataLoader(t_dataset, 
                                                      batch_size=batch_size, 
                                                      shuffle=False)
    
    pred_dataset_loader = torch.utils.data.DataLoader(p_dataset, 
                                                      batch_size=batch_size, 
                                                      shuffle=False)
    
    inter_meter = AverageMeter()
    union_meter = AverageMeter()
    batch_time = AverageMeter()
    
    end = time.time()
    miou_class = MIOU(num_classes=num_classes)
    
    for i, (true_target, pred_target) in enumerate(zip(true_dataset_loader, 
                                                       pred_dataset_loader)):

        true_target = true_target.to(device=device)
        pred_target = pred_target.to(device=device)

        inter, union = miou_class.get_iou(pred_target, true_target)
        inter_meter.update(inter)
        union_meter.update(union)

        # measure elapsed time
        batch_time.update(time.time() - end)
        end = time.time()

        if (i+1) % 10 == 0:  
            iou = inter_meter.sum / (union_meter.sum + 1e-10)
            miou = iou.mean() * 100

            print_log_message("[%d/%d]\t\tBatch Time:%.4f\t\tmiou:%.4f" %
                (i, len(true_dataset_loader), batch_time.avg, miou))
    
    print('\n')
    
    iou = inter_meter.sum / (union_meter.sum + 1e-10)
    for i, iou_per_class in enumerate(iou):
        print_info_message("%s IoU: %.2f" % (classes[i], iou_per_class))
    
    print('\n')
    
    miou = iou.mean() * 100
    print_info_message('Mean IoU: {0:.2f}'.format(miou))

    return iou, miou

if __name__ == "__main__":

    classes, palette = get_classes_palette()
    
    true_label_dir = '/home/adeshkin/projects/datasets/Winter_City/augmented_multiclass_dataset/test/mask'
    predicted_label_dir = '/home/adeshkin/projects/datasets/results_unet_mct_softmax_test_sample'
    true_convert = './t_folder'
    predicted_convert = './p_folder'
    batch_size = 16
    
    get_iou_metric(classes, 
                   palette, 
                   true_label_dir,
                   predicted_label_dir,
                   true_convert, 
                   predicted_convert,
                   batch_size)