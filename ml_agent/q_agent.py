import random
import pickle
import os

class QLearningAgent:
    def __init__(self, actions, learning_rate=0.1, discount_factor=0.9, epsilon=0.1):
        self.q_table = {}  # (state, action) -> value
        self.actions = actions  # List of possible actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon
        self.model_file = "q_table.pkl"

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state):
        """Epsilon-greedy action selection"""
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(self.actions)
        
        # Exploitation: choose action with max Q value
        q_values = [self.get_q_value(state, a) for a in self.actions]
        max_q = max(q_values)
        
        # Handle ties randomly
        best_actions = [a for a, q in zip(self.actions, q_values) if q == max_q]
        return random.choice(best_actions)

    def learn(self, state, action, reward, next_state):
        """Update Q-value using the Q-learning update rule"""
        current_q = self.get_q_value(state, action)
        
        # Max Q value for the next state
        next_max_q = max([self.get_q_value(next_state, a) for a in self.actions])
        
        # Q-learning formula
        new_q = current_q + self.lr * (reward + self.gamma * next_max_q - current_q)
        self.q_table[(state, action)] = new_q

    def save_model(self, filepath=None):
        if filepath is None:
            filepath = self.model_file
        with open(filepath, "wb") as f:
            pickle.dump(self.q_table, f)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath=None):
        if filepath is None:
            filepath = self.model_file
        if os.path.exists(filepath):
            with open(filepath, "rb") as f:
                self.q_table = pickle.load(f)
            print(f"Model loaded from {filepath}")
        else:
            print("No saved model found, starting fresh.")
