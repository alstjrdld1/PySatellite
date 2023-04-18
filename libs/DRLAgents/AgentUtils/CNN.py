import torch
import torch.nn as nn
import torch.nn.functional as F

from libs.Constants import *

class BasicCNN(torch.nn.Module):
    
    def __init__(self,
                 num_states  = NUM_STATES,
                 state_size1 = 64,
                 state_size2 = 84,
                 num_action = NUM_ACTIONS,
                 batch_size = BATCH_SIZE,
                 **kwargs):
        
        super(BasicCNN, self).__init__()
        self.conv1 = nn.Conv2d(128, 64, kernel_size=(1, 3), stride=(1, 2))
        self.conv2 = nn.Conv2d(64, 32, kernel_size=(1, 3), stride=(1, 2))
        self.conv3 = nn.Conv2d(32, batch_size, kernel_size=(1, 3), stride=(1, 2))

        # 각 컨볼루션 계층 이후의 텐서 크기에 따라 이 수치를 조정해야 할 수 있습니다.
        self.fc1 = nn.Linear(499, 4000)
        self.fc2 = nn.Linear(4000, num_action)

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = x.view(x.size(0), -1) # Flatten the tensor
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x