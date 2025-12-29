from .qAgent import QLearningAgent
from . import config
import os

class SimpleQLearningAgent(QLearningAgent):
    def __init__(self, actions):
        super().__init__(actions)
        # Override file paths
        self.saveFile = os.path.join(config.BASE_DIR, "simple_qTable.pkl")
        self.loadFile = os.path.join(config.BASE_DIR, "simple_qTable.pkl")
        
    # Reuse chooseAction, learn, saveModel, loadModel from parent
    # They are generic enough to handle any state tuple.
