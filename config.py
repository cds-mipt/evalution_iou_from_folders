#Apolloscape

TRUE_LABEL_DIR = '/home/adeshkin/projects/datasets/apolloscape/original/test_masks'
PRED_LABEL_DIR = '/home/adeshkin/projects/datasets/apolloscape/results_multiclass_unet_test_2'

TRUE_FLAG_CONVERT = False
PRED_FLAG_CONVERT = True
BATCH_SIZE = 32
NUM_CLASSES = 19

            
CLASSES ={0: 'void',
          1: 'stop_lane',
          2: 'arrow_right',
          3: 'dirt',
          4: "don't know",
          5: 'dirt_another',
          6: 'arrow_forward_right',
          7: 'yellow_service_another',
          8: 'parking',
          9: 'dashed',
          10: 'zebra',
          11: 'hatched',
          12: 'arrow_forward_left',
          13: 'arrow_left',
          14: 'solid',
          15: 'yellow_service',
          16: "don't know2",
          17: 'arrow_turn',
          18: 'ignored'}

PALETTE = {(0, 0, 0): 0,
           (0, 0, 192): 1,
           (35, 136, 226): 2,
           (60, 15, 3): 3,
           (60, 15, 67): 4,
           (64, 16, 4): 5,
           (100, 25, 70): 6,
           (100, 25, 198): 7,
           (128, 32, 8): 8,
           (142, 35, 8): 9,
           (153, 102, 153): 10,
           (156, 167, 105): 11,
           (160, 168, 234): 12,
           (180, 109, 91): 13,
           (180, 173, 43): 14,
           (190, 47, 75): 15,
           (204, 51, 12): 16,
           (230, 57, 14): 17,
           (255, 255, 255): 18} 