# SnakeEater AI

A comprehensive update to the classic Snake game, featuring a reinforcement learning-based AI agent. This project demonstrates the integration of modern game development practices with machine learning using Python and Pygame.

## Project Overview

SnakeEater AI features a battle royale environment. The project showcases:
*   **Machine Learning**: An intelligent agent trained using Q-Learning to survive and compete.
*   **Game Development**: A robust game engine built on Pygame with optimized rendering and collision detection.
*   **UI/UX**: Modern user interface with dynamic text, scoreboards, and smooth visual effects.

## Machine Learning Model (Q-Learning)

The AI agent uses **Q-Learning**, a reinforcement learning algorithm, to make decisions. The process follows this cycle:

```mermaid
graph TD
    %% Styling
    classDef state fill:#e2f0d9,stroke:#a9d08e,color:#333;
    classDef action fill:#fff2cc,stroke:#ffd966,color:#333;
    classDef reward fill:#deebf7,stroke:#9bc2e6,color:#333;
    classDef update fill:#e1d5e7,stroke:#b4a7d6,color:#333;

    A([Start]) --> B[Observe State]
    B --> C{Choose Action}
    C -- Exploration --> D[Random Action]
    C -- Exploitation --> E[Best Q-Value Action]
    D --> F[Execute Action]
    E --> F
    F --> G[Get Reward / Penalty]
    G --> H[Update Q-Table]
    H --> B

    class B state
    class C,D,E,F action
    class G reward
    class H update
```

## Features

*   **Intelligent Adversaries**: Computer snakes trained to hunt food and avoid collisions.
*   **Spectator Mode**: Watch the AI learn and evolve in real-time (`learn.py`).
*   **Visual Polish**: Custom textures for snakes and backgrounds, particle effects, and polished UI elements.
*   **Audio Integration**: Background music and sound effects for immersive gameplay.
*   **Optimization**: Implemented **Spatial Grid** system (`spatial.py`) for efficient collision detection, enabling high-performance training.

## Architecture

The project is organized into a modular structure to ensure maintainability and scalability:

*   **`src/`**: Core source code.
    *   **`game.py`**: Main game loop, rendering logic, and state management.
    *   **`snake.py`**: Snake entity logic, including movement and AI behavior.
    *   **`spatial.py`**: Spatial grid implementation for optimized collision detection (O(N) performance).
    *   **`mlAgent/`**: Q-Learning implementation (`qAgent.py`, `config.py`).
*   **`scripts/`**: Utility scripts for building executables and generating assets.
*   **`assets/`**: Game resources including images and audio files.
*   **`main.py`**: Entry point for the standard game mode (Human vs AI).
*   **`learn.py`**: Entry point for the training/spectator mode (AI vs AI).

## Class Structure

```mermaid
classDiagram
    %% Styling - Low Saturation / Pastel
    classDef default fill:#f9f9f9,stroke:#999,stroke-width:1px,color:#333;
    classDef core fill:#e2f0d9,stroke:#a9d08e;
    classDef entity fill:#deebf7,stroke:#9bc2e6;
    classDef item fill:#fff2cc,stroke:#ffd966;
    classDef ai fill:#e1d5e7,stroke:#b4a7d6;

    class GAME {
        +mode: str
        +snakes: List
        +food: List
        +agent: QLearningAgent
        +setUp()
        +update()
        +draw()
        +checkCollision()
    }
    
    class Snake {
        +body: List[Rect]
        +length: int
        +score: int
        +direction: Vector2
        +move()
        +draw()
        +grow()
        +set_skin()
    }
    
    class PlayerSnake {
        <<Player Controls>>
        +updateDirectionByMouse()
    }
    
    class ComputerSnake {
        <<AI Controlled>>
        +angle: float
        +stateOld: tuple
        +performAction(action)
        +updateDirection()
    }

    class Food {
        +x: int
        +y: int
        +type: str
        +growthValue: int
        +draw()
    }
    class SmallFood
    class MediumFood
    class LargeFood
    
    class QLearningAgent {
        +qTable: dict
        +epsilon: float
        +lr: float
        +getQValue(state, action)
        +chooseAction(state)
        +learn(state, action, reward, next_state)
    }

    %% Relationships
    GAME *-- Snake : manages
    GAME *-- Food : manages
    GAME --> QLearningAgent : integrates
    Snake <|-- PlayerSnake : inheritance
    Snake <|-- ComputerSnake : inheritance
    Food <|-- SmallFood : inheritance
    Food <|-- MediumFood : inheritance
    Food <|-- LargeFood : inheritance

    %% Applying Styles
    class GAME core
    class Snake entity
    class PlayerSnake entity
    class ComputerSnake entity
    class Food item
    class SmallFood item
    class MediumFood item
    class LargeFood item
    class QLearningAgent ai
```

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Nelson0314/aoop_2025_group11_snakeEater.git
    cd aoop_2025_group11_snakeEater
    ```

2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Play Mode
To play the game against AI opponents:
```bash
python main.py
```
*   **Controls**: 
    *   **Mouse Move**: Steer your snake.
    *   **Mouse Left Click (Hold)**: Boost speed (Consumes score/length).
*   **Goal**: Eat food to grow, avoid walls and other snakes. Cut off opponents to kill them.

![Play Mode](docs/main.png)

### Spectator / Training Mode
To watch the AI training process:
```bash
python learn.py
```
*   **Controls**:
    *   `A` / `D`: Switch between different AI snakes to spectate.
    *   `G`: Toggle "God View" to see the entire map.

![Spectator Mode](docs/learn.png)


## Credits

**Group 11**
*   Nelson0314

Developed for AOOP 2025.