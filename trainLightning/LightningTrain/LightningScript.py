import pytorch_lightning as pl
import torch
from torch import nn
from torch.utils.data import DataLoader, random_split, TensorDataset
import torch.nn.functional as F
import argparse as arg
import importlib.util

from LoadData import create_dataloader, ROOTDataset                 # import own modules
from model import SimpleNN
from argparser import get_args


def import_module(path, name='module'):                             # function to import module from specified path given as argument
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

args = get_args()                                                   # get arguments from argparser.py

device = (                                                          # chose device, gpu preferred
    "cuda" if torch.cuda.is_available()
    else "cpu"
)
print(f"Using {device} device")

createModel = import_module(args.model_path, 'model_module')        # import model from specified path
Model = createModel.get_model().to(device)                          # instantiate model
print(Model)

dataloader_train = create_dataloader(args.data_train_path, "events;1", batch_size=args.batch_size, shuffle=True)    # create dataloader for training data
dataloader_test = create_dataloader(args.data_test_path, "events;1", batch_size=args.batch_size, shuffle=True)      # create dataloader for test data