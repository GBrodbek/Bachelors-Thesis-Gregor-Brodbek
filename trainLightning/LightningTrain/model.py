import pytorch_lightning as L
import torch
from torch import nn
import torch.nn.functional as F

class SimpleNN(L.LightningModule):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.layer_1 = nn.Linear(100, 50)
        self.layer_2 = nn.Linear(50, 2)

    def forward(self, x):
        x = F.relu(self.layer_1(x))
        x = self.layer_2(x)
        return x

    def training_step(self, batch, batch_idx):
        x, y = batch
        y_hat = self(x)
        loss = F.cross_entropy(y_hat, y)
        self.log('train_loss', loss)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=0.001)
        return optimizer
    
def get_model():
    model = SimpleNN()
    return model