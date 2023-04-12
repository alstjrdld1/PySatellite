import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self, 
                 num_state, 
                 hidden_size, 
                 num_action):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(num_state, hidden_size)
        self.fc2 = nn.Linear(hidden_size, num_action)
    
    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        action_value = self.fc2(x)
        return action_value