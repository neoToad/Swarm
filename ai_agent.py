from main import SwarmGame
import torch
import pygame
from collections import deque
import numpy as np
import random
from model import Linear_QNet, QTrainer
from h_plots import plot

pygame.init()
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # Randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 5)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        MID_ZONE = pygame.Rect(550, 865, 330, 500)
        P1_ZONE = pygame.Rect(540, 860, 63, 200)
        P2_ZONE = pygame.Rect(85, 240, 365, 535)
        P3_ZONE = pygame.Rect(590, 795, 625, 740)
        P4_ZONE = pygame.Rect(1113, 1300, 355, 515)

        for unit in game.all_sprites:
            mid_zone = MID_ZONE == unit.rect.colliderect(MID_ZONE)
            p1_zone = P1_ZONE == unit.rect.colliderect(P1_ZONE)
            p2_zone = P2_ZONE == unit.rect.colliderect(P2_ZONE)
            p3_zone = P3_ZONE == unit.rect.colliderect(P3_ZONE)
            p4_zone = P4_ZONE == unit.rect.colliderect(P4_ZONE)


            state = [
                # Danger base attacked
                # (unit in unit.player_group and unit in game.bases and unit.get_damage()),

                # Base health low
                (unit in game.bases and unit.current_health < unit.maximum_health // 3),

                # Units low
                (len(unit.player_group) < 15),

                # Current zone
                mid_zone,
                p1_zone,
                p2_zone,
                p3_zone,
                p4_zone,

                #other units
                len(unit.player_group) > len(game.players["Player01"]['group']),
                len(unit.player_group) > len(game.players["Player02"]['group']),
                len(unit.player_group) > len(game.players["Player03"]['group']),
                len(unit.player_group) > len(game.players["Player04"]['group'])
            ]

            return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # pop left if max mem is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # List of tuples

        else:
            mini_sample = self.memory
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # Random moves: tradeoff exploration/exploitation
        self.epsilon = 80 - self.n_games
        self.final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            self.final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            try:
                self.final_move[move] = 1
            except IndexError:
                pass

        return self.final_move


def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SwarmGame()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        # for unit in game.all_sprites:
        #     if unit not in game.bases and unit not in game.players['Player01']['group']:
        #         unit.set_target(final_move)

        # for base in game.bases:
        #     if base not in game.players['Player01']['group']:
        reward, score, done = game.run_game(final_move)
        #         state_new = agent.get_state(game)
        #         agent.train_short_memory(state_old, final_move, reward, state_new, done)
        #         agent.remember(state_old, final_move, reward, state_new, done)
        # reward, done, score = game.players['Player02']['reward'], game.players['Player02']['dead'], game.players['Player02']['score']
        # reward, done, score = game.players['Player03']['reward'], game.players['Player03']['dead'], game.players['Player03']['score']
        # reward, done, score = game.players['Player04']['reward'], game.players['Player04']['dead'], game.players['Player04']['score']

        state_new = agent.get_state(game)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if game.game_over:
            # train the long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()