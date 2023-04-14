import random

from ....libs.Constants import *

def Transition(state, action, state_next, reward):
    pass

class ReplayMemory:
    def __init__(self, 
                 CAPACITY=MEMORY_CAPACITY):
        self.capacity = CAPACITY  # Maximum Number of memory storage
        self.memory = []  # Stored variables for real transition
        self.index = 0  # Index Variables for pointing storage location

    def push(self, state, action, state_next, reward):
        '''transition = (state, action, state_next, reward) is stored in memory'''

        if len(self.memory) < self.capacity:
            self.memory.append(None)  # if memory is not full 

        # Store using Transition
        self.memory[self.index] = Transition(state, action, state_next, reward)

        self.index = (self.index + 1) % self.capacity  # push it to backward 

    def sample(self, batch_size):
        '''batch_size分だけ、ランダムに保存内容を取り出す'''
        return random.sample(self.memory, batch_size)

    def __len__(self):
        '''関数lenに対して、現在の変数memoryの長さを返す'''
        return len(self.memory)