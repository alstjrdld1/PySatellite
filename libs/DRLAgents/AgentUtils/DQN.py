import torch
import torch.nn.functional as F

from libs.Constants import *

# Define Deep Q Network 
class DQN(torch.nn.Module):
    def __init__(self, 
                 num_states  = NUM_STATES,
                 state_size1 = 64,
                 state_size2 = 84,
                 num_action = NUM_ACTIONS,
                 **kwargs):
        super(DQN, self).__init__(**kwargs)

        self.conv1 = torch.nn.Conv2d(in_channels=num_states, out_channels=32,
                                     kernel_size=8, stride=4)
        
        dim1 = ((state_size1 - 8)//4 + 1, (state_size2 - 8)//4 + 1)

        self.conv2 = torch.nn.Conv2d(in_channels=32, out_channels=64,
                                     kernel_size=4, stride=2)
        dim2 = ((dim1[0] - 4)//2 + 1, (dim1[1] - 4)//2 + 1)

        self.conv3 = torch.nn.Conv2d(in_channels=64, out_channels=64,
                                     kernel_size=3, stride=1)
        dim3 = ((dim2[0] - 3)//1 + 1, (dim2[1] - 3)//1 + 1)

        self.flat = torch.nn.Flatten()
        self.fc1 = torch.nn.Linear(64*dim3[0]*dim3[1], 512)
        self.q = torch.nn.Linear(512, num_action)

    def forward(self, x):
        x = x.permute(0, 3, 1, 2)
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x = self.flat(x)
        x = F.relu(self.fc1(x))
        return self.q(x)