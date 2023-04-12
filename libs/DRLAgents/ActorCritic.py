import torch
import torch.nn as nn 
import torch.nn.functional as F

class ActorCritic(torch.nn.Module):
    def __init__(self, state_size=5, action_size=5, **kwargs):
        super(ActorCritic, self).__init__(**kwargs)
        self.d1 = nn.Linear(state_size, 256)
        self.d2 = nn.Linear(256, 256)
        self.pi = nn.Linear(256, action_size)
        self.v = nn.Linear(256 , 1)
    
    def forward(self, x):
        x = F.relu(self.d1(x))
        x = F.relu(self.d2(x))
        # return torch.tanh(self.pi(x)), self.v(x) # in continuous 
        return torch.softmax(self.pi(x)), self.v(x) 