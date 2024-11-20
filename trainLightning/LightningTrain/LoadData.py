import uproot
import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import pandas as pd

class ROOTDataset(Dataset):
    def __init__(self, file_path, tree_name):
        self.file = uproot.open(file_path)
        self.tree = self.file[tree_name]
        self.data = self.tree.arrays(library="pd")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        features = self.data.drop(columns='label_true').iloc[idx].values
        label = self.data['label_true'].iloc[idx] 
        return features, label

    #def create_histograms(self, bins=50):
    #    import matplotlib.pyplot as plt
    #    for column in self.data.columns:
    #        plt.figure()
    #        self.data[column].hist(bins=bins, histtype='step')
    #        plt.title(f'Histogram of {column}')
    #        plt.xlabel(column)
    #        plt.ylabel('Frequency')
    #        plt.show()
    

def create_dataloader(file_path, tree_name, batch_size=32, shuffle=True):
    dataset = ROOTDataset(file_path, tree_name)
    dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)
    return dataset


#test = create_dataloader("roottest.root", "events;1")
test = ROOTDataset("roottest.root", "events;2")
print(test.__getitem__(5))