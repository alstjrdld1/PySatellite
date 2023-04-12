from Net import *

class DQN:
    def __init__(self, 
                 num_states,
                 hidden_size,
                 num_action):
        
        super(DQN, self).__init__()
        self.eval_net, self.target_net = Net(num_states, hidden_size, num_action), Net(num_states, hidden_size, num_action)