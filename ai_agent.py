import torch
import random
import numpy as np
from collections import deque
# from game import SnakeGameAI, Direction, Point
# from model import Linear_QNet, QTrainer
# from helper import plot\
from Base import Base

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class BaseAI(Base):
    def __init__(self, screen, player, all_units, lasers_group, bases):
        super().__init__(screen, player, all_units, lasers_group, bases)

