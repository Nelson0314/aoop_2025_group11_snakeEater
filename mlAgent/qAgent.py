from mlAgent import config

class QLearningAgent:
    def __init__(self, actions, learningRate=config.LEARNING_RATE, discountFactor=config.DISCOUNT_FACTOR, epsilon=config.EPSILON):
        self.qTable = {}  # (state, action) -> value
        self.actions = actions  # List of possible actions
        self.lr = learningRate
        self.gamma = discountFactor
        self.epsilon = epsilon
        self.modelFile = config.MODEL_FILE_NAME

    def getQValue(self, state, action):
        return self.qTable.get((state, action), 0.0)

    def chooseAction(self, state):
        """Epsilon-greedy action selection"""
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        
        # Exploitation: choose action with max Q value
        qValues = [self.getQValue(state, a) for a in self.actions]
        maxQ = max(qValues)
        
        # Handle ties randomly
        bestActions = [a for a, q in zip(self.actions, qValues) if q == maxQ]
        return random.choice(bestActions)

    def learn(self, state, action, reward, nextState):
        """Update Q-value using the Q-learning update rule"""
        currentQ = self.getQValue(state, action)
        
        # Max Q value for the next state
        nextMaxQ = max([self.getQValue(nextState, a) for a in self.actions])
        
        # Q-learning formula
        newQ = currentQ + self.lr * (reward + self.gamma * nextMaxQ - currentQ)
        self.qTable[(state, action)] = newQ

    def saveModel(self, filepath=None):
        if filepath is None:
            filepath = self.modelFile
        with open(filepath, "wb") as f:
            pickle.dump(self.qTable, f)
        print(f"Model saved to {filepath}")

    def loadModel(self, filepath=None):
        if filepath is None:
            filepath = self.modelFile
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.qTable = pickle.load(f)
            print(f"Model loaded from {filepath}")
        else:
            print("No saved model found, starting fresh.")
