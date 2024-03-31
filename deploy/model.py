import torch.nn as nn
import torch
from torchvision import transforms
import numpy as np

class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(1, 8, kernel_size=3, stride=1, padding=0), #[1, 28, 28] -> [8, 26, 26]
            nn.ReLU(),
            nn.BatchNorm2d(8),
            nn.MaxPool2d(kernel_size = 3, stride = 2), #[8, 26, 26] -> [8, 12, 12] 
            nn.Dropout(0.25))

        self.layer2 = nn.Sequential(
            nn.Conv2d(8, 16, kernel_size=3, stride=1, padding=0), #[8, 12, 12] -> [16, 10, 10]
            nn.ReLU(),
            nn.BatchNorm2d(16),
            nn.MaxPool2d(kernel_size=3, stride=2) #[16, 10, 10] -> [16, 4, 4]
        )

        self.classifier = nn.Sequential(
            nn.Linear(256, 50),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(50, 10)
        )

        self.gradient = None
        self.relu = nn.ReLU()
        self.resize = transforms.Resize(28)
        self.flatten = nn.Flatten()

    def forward(self, x):
       z = self.layer1(x)
       z = self.layer2(z)
       h = z.register_hook(self.hook_activation)
       z = self.flatten(z)
       z = self.classifier(z)
       return z
    
    def get_activations(self, x):
        with torch.no_grad():
            x = self.layer1(x)
            return self.layer2(x)
        
    def hook_activation(self, grad):
        self.gradient = grad
    
modifiedNet = Net()
modifiedNet.load_state_dict(torch.load('models/Model.pt'))
modifiedNet.eval()

def predict(img):
    img = np.array(img)
    inp = torch.from_numpy(img).unsqueeze(0).unsqueeze(0).float()
    output = modifiedNet(inp)
    (_, pred) = torch.max(output, 1)    
    return pred.item()