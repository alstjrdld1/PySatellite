from .ActorCritic import *

import numpy as np
import datetime

from torch.utils.tensorboard import SummaryWriter

class PPOAgent(ActorCritic):
    def __init__(self, 
                 save_path="./ptfiles",
                 learning_rate=0.1,
                 device=torch.device("cpu")):
        
        super(PPOAgent, self).__init__()
        
        self.device = device
        self.network = ActorCritic().to(device)
        self.optimizer = torch.optim.Adam(self.network.parameters(), lr=learning_rate)
        self.memory = list()
        self.writer = SummaryWriter(save_path)

        self.load_model = False

    def load_pt(self, 
                data_path=""):
        pass

    # 정책을 통해 행동 결정 
    def get_action(self, state, training=True):
        # 네트워크 모드 설정
        self.network.train(training)

        # 네트워크 연산에 따라 행동 결정
        pi, _ = self.network(torch.FloatTensor(state).to(self.device))
        action = torch.multinomial(pi, num_samples=1).cpu().numpy()
        return action
    
    # 리플레이 메모리에 데이터 추가 (상태, 행동, 보상, 다음 상태, 게임 종료 여부)
    def append_sample(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
    
    # 학습 수행
    def train_model(self):
        self.network.train()
        
        state      = np.stack([m[0] for m in self.memory], axis=0)
        action     = np.stack([m[1] for m in self.memory], axis=0)
        reward     = np.stack([m[2] for m in self.memory], axis=0)
        next_state = np.stack([m[3] for m in self.memory], axis=0)
        done       = np.stack([m[4] for m in self.memory], axis=0)
        self.memory.clear()

        state, action, reward, next_state, done = map(lambda x: torch.FloatTensor(x).to(self.device),
                                                    [state, action, reward, next_state, done])
        
        # prob_old, adv, ret 계산 
        with torch.no_grad():
            pi_old, value = self.network(state)
            prob_old = pi_old.gather(1, action.long())
            _, next_value = self.network(next_state)
            delta = reward + (1 - done) * discount_factor * next_value - value
            adv = delta.clone()
            adv, done = map(lambda x: x.view(n_step, -1).transpose(0,1).contiguous(), [adv, done])
            for t in reversed(range(n_step-1)):
                adv[:, t] += (1 - done[:, t]) * discount_factor * _lambda * adv[:, t+1]
            adv = adv.transpose(0,1).contiguous().view(-1, 1)
            
            ret = adv + value

    # 네트워크 모델 저장
    def save_model(self):
        print(f"... Save Model to {self.save_path}/ckpt ...")
        torch.save({
            "network" : self.network.state_dict(),
            "optimizer" : self.optimizer.state_dict(),
        }, self.save_path+'/ckpt')

    # 학습 기록 
    def write_summary(self, score, actor_loss, critic_loss, step):
        self.writer.add_scalar("run/score", score, step)
        self.writer.add_scalar("model/actor_loss", actor_loss, step)
        self.writer.add_scalar("model/critic_loss", critic_loss, step)
