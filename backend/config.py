import torch


IMAGE_SIZE = [600, 600]
DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
NUM_CLASSES = 2
BATCH_SIZE = 2
NUM_EPOCHS = 10001
SAVE_EPOCH = 500
TRAIN_NEW_MODEL = False

TEST_DIR = "uploads"
BEST_MODEL_DIR = "best_model_02.torch"
PREDICTION_DIR = "predictions"
best_model_file = 'CNN_aug_best_weights.h5'
