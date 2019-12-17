# Evalution iou per class and mean iou from folders
```
1. To change classes, palette for your dataset in get_iou_metric.py: L.89-93
Example:
  classes = {0: background,
             1: building,
             2: car}
  palette = {(0, 0, 0):0,
             (125, 0, 125):1,
             (255, 0, 0):2}

2. To enter path to masks in get_iou_metric.py: L.95-96
3. To run:
python get_iou_metric.py 
```
