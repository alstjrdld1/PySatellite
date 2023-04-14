from .AgentUtils.Net import *
from libs.Constants import *

import numpy as np

import torch
import torch.nn as nn

class DQN:
    def __init__(self, 
                 num_states = NUM_STATES,
                 hidden_size = HIDDEN_SIZE,
                 num_action = NUM_ACTIONS, 
                 memory_capacity = MEMORY_CAPACITY,
                 learning_rate = LR,
                 episilo = EPISILO):
        
        super(DQN, self).__init__()
        
        self.MEMORY_CAPACITY = memory_capacity
        self.LR = learning_rate
        self.EPISILO = episilo

        self.NUM_ACTIONS = num_action
        self.NUM_STATES  = num_states
        self.HIDDEN_SIZE = hidden_size
        
        self.eval_net    = Net(self.NUM_STATES, self.HIDDEN_SIZE, self.NUM_ACTIONS)
        self.target_net  = Net(self.NUM_STATES, self.HIDDEN_SIZE, self.NUM_ACTIONS)

        self.learn_step_counter = 0
        self.memory_counter = 0
        self.memory = np.zeros((self.MEMORY_CAPACITY, self.NUM_STATES * 2 + 2))

        self.optimizer = torch.optim.Adam(self.eval_net.parameters(), lr = self.LR)
        self.loss_func = nn.MSELoss()
    
    def choose_action(self, state):
        state = torch.unsqueeze(torch.FloatTensor(state), 0)

        if (np.random.randn() <= self.EPISILO):
            action_value = self.eval_net.forward(state)
            action = torch.max(action_value, 1)[1].data.numpy()
            action = action[0]
        else:
            action = np.random.randint(0, self.NUM_ACTIONS)
            action = action

        return action
    
    def store_transition(self, state, action, reward, next_state):
        state_flat = state.flatten()
        next_state_flat = next_state.flatten()

        transition = np.hstack((state_flat, [action, reward], next_state_flat))
        index = self.memory_counter % self.MEMORY_CAPACITY
        self.memory[index, :] = transition
        self.memory_counter += 1

    def learn(self, 
              network_iteration,
              batch_size,
              gamma):
        
        # update the parameters
        if self.learn_step_counter % network_iteration == 0:
            self.target_net.load_state_dict(self.eval_net.state_dict())
        self.learn_step_counter +=1

        # sample batch from memory
        sample_index = np.random.choice(self.MEMORY_CAPACITY, batch_size)
        batch_memory = self.memory[sample_index, :]
        batch_state = torch.FloatTensor(batch_memory[:, :self.NUM_STATES])
        batch_action = torch.LongTensor(batch_memory[:, self.NUM_STATES:self.NUM_STATES + 1].astype(int))
        batch_reward = torch.FloatTensor(batch_memory[:, self.NUM_STATES + 1:self.NUM_STATES + 2])
        batch_next_state = torch.FloatTensor(batch_memory[:, -self.NUM_STATES:])

        # q_eval
        q_eval = self.eval_net(batch_state).gather(1, batch_action)
        q_next = self.target_net(batch_next_state).detach()
        q_target = batch_reward + gamma*q_next.max(1)[0].view(batch_size, 1)
        loss = self.loss_func(q_eval, q_target)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()