from libs.Constants import *

from libs.DRLAgents.AgentUtils.DQN import *

import copy
import random
from collections import deque

import numpy as np

import torch
import torch.nn as nn

from torch.utils.tensorboard import SummaryWriter

class DQNAgent:
    def __init__(self, 
                 num_states         = NUM_STATES,
                 hidden_size        = HIDDEN_SIZE,
                 num_action         = NUM_ACTIONS, 
                 memory_capacity    = MEMORY_CAPACITY,
                 learning_rate      = LR,
                 epsilon_init       = EPSILON_INIT,
                 epsilon_eval       = EPSILON_EVAL,
                 epsilon_min        = EPSILON_MIN,
                 batch_size         = BATCH_SIZE,
                 discount_factor    = DISCOUNT_FACTOR,
                 device             = DEVICE,
                 save_path          = SAVE_PATH,
                 train_mode         = True):
        
        self.network = DQN(
            num_states=num_states,
            num_action=num_action
        ).to(device)

        self.target_network     = copy.deepcopy(self.network)
        self.optimizer          = torch.optim.Adam(self.network.parameters(), lr=learning_rate)
        self.memory             = deque(maxlen=memory_capacity)
        self.batch_size         = batch_size
        self.discount_factor    = discount_factor
        self.train_mode         = train_mode

        self.epsilon            = epsilon_init
        self.epsilon_eval       = epsilon_eval
        self.epsilon_min        = epsilon_min
        self.epsilon_delta      = (epsilon_init - epsilon_min)/EXPLORE_STEP if train_mode else 0.

        self.save_path          = save_path

        self.writer             = SummaryWriter(self.save_path)
        self.action_size        = num_action
        self.device             = device
        
    def load_model(self, load_path):
        print(f"... Load Model from {load_path}/ckpt ...")
        checkpoint = torch.load(load_path+'/ckpt', map_location=self.device)
        self.network.load_state_dict(checkpoint["network"])
        self.target_network.load_state_dict(checkpoint["network"])
        self.optimizer.load_state_dict(checkpoint["optimizer"])

    def train(self):
        self.train_mode = True
        self.network.train(self.train_mode)
    
    def eval(self):
        self.train_mode = False
        self.network.train(self.train_mode)
        
    # Epsilon greedy 기법에 따라 행동 결정 
    def get_action(self, state):
        #  네트워크 모드 설정
        self.network.train(self.train_mode)
        epsilon = self.epsilon if self.train_mode else self.epsilon_eval

        # 랜덤하게 행동 결정
        if epsilon > random.random():  
            action = np.random.randint(0, self.action_size)
        # 네트워크 연산에 따라 행동 결정
        else:
            q = self.network(torch.FloatTensor(state).to(self.device))
            action = torch.argmax(q, axis=-1, keepdim=True).data.cpu().numpy()
        return action

    # 리플레이 메모리에 데이터 추가 (상태, 행동, 보상, 다음 상태, 게임 종료 여부)
    def append_sample(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    # 학습 수행
    def train_model(self):
        batch      = random.sample(self.memory, self.batch_size)
        state      = np.stack([b[0] for b in batch], axis=0)
        action     = np.stack([b[1] for b in batch], axis=0)
        reward     = np.stack([b[2] for b in batch], axis=0)
        next_state = np.stack([b[3] for b in batch], axis=0)
        done       = np.stack([b[4] for b in batch], axis=0)

        state, action, reward, next_state, done = map(lambda x: torch.FloatTensor(x).to(self.device),
                                                        [state, action, reward, next_state, done])

        eye = torch.eye(self.action_size).to(self.device)
        one_hot_action = eye[action.view(-1).long()]
        q = (self.network(state) * one_hot_action).sum(1, keepdims=True)

        with torch.no_grad():
            next_q = self.target_network(next_state)
            target_q = reward + next_q.max(1, keepdims=True).values * ((1 - done) * self.discount_factor)

        loss = F.smooth_l1_loss(q, target_q)

        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # 엡실론 감소
        self.epsilon = max(self.epsilon_min, self.epsilon - self.epsilon_delta)

        return loss.item()

    # 타겟 네트워크 업데이트
    def update_target(self):
        self.target_network.load_state_dict(self.network.state_dict())

    # 네트워크 모델 저장 
    def save_model(self):
        print(f"... Save Model to {self.save_path}/ckpt ...")
        torch.save({
            "network" : self.network.state_dict(),
            "optimizer" : self.optimizer.state_dict(),
        }, self.save_path+'/ckpt')

    # 학습 기록 
    def write_summary(self, score, loss, epsilon, step):
        self.writer.add_scalar("Episode Reward", score, step)
        self.writer.add_scalar("Episode Loss", loss, step)
        # self.writer.add_scalar("model/epsilon", epsilon, step)