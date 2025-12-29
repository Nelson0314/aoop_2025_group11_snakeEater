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

### State Representation

The agent perceives the environment through a **12-bit state vector** tuple:

| Index | Feature | Description |
| :---: | :--- | :--- |
| **0** | **Danger Forward** | Collision risk ahead within vision range. |
| **1** | **Danger Right** | Collision risk to the relative right. |
| **2** | **Danger Left** | Collision risk to the relative left. |
| **3** | **Direction Left** | Moving West currently. |
| **4** | **Direction Right** | Moving East currently. |
| **5** | **Direction Up** | Moving North currently. |
| **6** | **Direction Down** | Moving South currently. |
| **7** | **Food Left** | Closest food is to the West. |
| **8** | **Food Right** | Closest food is to the East. |
| **9** | **Food Up** | Closest food is to the North. |
| **10** | **Food Down** | Closest food is to the South. |
| **11** | **Combat Aware** | Enemy head detected near strategic body segments (Cut-off risk). |

### Action Space

The agent chooses from **6 discrete actions** at each step:

| ID | Action | Effect |
| :---: | :--- | :--- |
| **0** | **Straight** | Maintain current direction. |
| **1** | **Turn Left** | Rotate angle counter-clockwise. |
| **2** | **Turn Right** | Rotate angle clockwise. |
| **3** | **Boost Straight** | Accelerate forward (Consumes score). |
| **4** | **Boost Left** | Accelerate and turn left. |
| **5** | **Boost Right** | Accelerate and turn right. |

<div align="center">
  <img src="https://mermaid.ink/img/eyJjb2RlIjogImdyYXBoIFREXG4gICAgY2xhc3NEZWYgc2Vuc29yIGZpbGw6I2UyZjBkOSxzdHJva2U6I2E5ZDA4ZSxjb2xvcjojMzMzO1xuICAgIGNsYXNzRGVmIHN0YXRlIGZpbGw6I2RlZWJmNyxzdHJva2U6IzliYzJlNixjb2xvcjojMzMzO1xuICAgIGNsYXNzRGVmIGFpIGZpbGw6I2UxZDVlNyxzdHJva2U6I2I0YTdkNixjb2xvcjojMzMzO1xuICAgIGNsYXNzRGVmIGFjdGlvbiBmaWxsOiNmZmYyY2Msc3Ryb2tlOiNmZmQ5NjYsY29sb3I6IzMzMztcblxuICAgIHN1YmdyYXBoIFNlbnNvcnMgWzEuIEVudmlyb25tZW50YWwgU2Vuc29yc11cbiAgICAgICAgVmlzW1Zpc2lvbjogMyBwdHNdXG4gICAgICAgIEZvb2RbRm9vZCBTZW5zb3JdXG4gICAgICAgIENvbWJhdFtDb21iYXQgQXdhcmVuZXNzXVxuICAgICAgICBDdXJyRGlyW0N1cnJlbnQgRGlyZWN0aW9uXVxuICAgIGVuZFxuXG4gICAgc3ViZ3JhcGggU3RhdGVWZWMgWzIuIFN0YXRlIFZlY3RvciAoMTIgQml0cyldXG4gICAgICAgIFMxW0RhbmdlciAoMyldXG4gICAgICAgIFMyW0RpcmVjdGlvbiAoNCldXG4gICAgICAgIFMzW0Zvb2QgTG9jICg0KV1cbiAgICAgICAgUzRbQ29tYmF0ICgxKV1cbiAgICBlbmRcblxuICAgIHN1YmdyYXBoIEludGVsbGlnZW5jZSBbMy4gUS1MZWFybmluZyBDb3JlXVxuICAgICAgICBRVGFibGVbUS1UYWJsZSBMb29rdXBdXG4gICAgZW5kXG5cbiAgICBzdWJncmFwaCBBY3QgWzQuIENob3NlbiBBY3Rpb25dXG4gICAgICAgIEFjdGlvbnNbQWN0aW9uIFNwYWNlICg2KV1cbiAgICBlbmRcblxuICAgIFZpcyAtLT4gUzFcbiAgICBDdXJyRGlyIC0tPiBTMlxuICAgIEZvb2QgLS0-IFMzXG4gICAgQ29tYmF0IC0tPiBTNFxuXG4gICAgUzEgLS0-IFFUYWJsZVxuICAgIFMyIC0tPiBRVGFibGVcbiAgICBTMyAtLT4gUVRhYmxlXG4gICAgUzQgLS0-IFFUYWJsZVxuXG4gICAgUVRhYmxlIC0tPiBBY3Rpb25zXG5cbiAgICBjbGFzcyBWaXMsRm9vZCxDb21iYXQsQ3VyckRpciBzZW5zb3I7XG4gICAgY2xhc3MgUzEsUzIsUzMsUzQgc3RhdGU7XG4gICAgY2xhc3MgUVRhYmxlIGFpO1xuICAgIGNsYXNzIEFjdGlvbnMgYWN0aW9uOyIsICJtZXJtYWlkIjogeyJ0aGVtZSI6ICJkZWZhdWx0In19" alt="State Diagram" width="100%"/>
</div>

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

<div align="center">
  <img src="https://www.plantuml.com/plantuml/png/RLHDRnCn4BtdL_ZOq4P275TLrKtuKAL4K0BbW11orfDTArxFClQI1kX_PsnliquWbymyZz-yUPxardb9lc_DnEsqxIJ9LbH6EbTwJthJUxYhqAxrBn0liv8MBLODOGjYAus3xAYJrKxMiFO70uAWyjBM9YzmZLIurxOUhZPQWQWqLLnrhaBydWZ-p9cp9kojMg114byQxI6Ub4IuJ-3SS5KgHr90EVeqcII-T-NgJIIzR5518Poda3WhT-0AiTJEXtoBgCQCnx6-4FTBa6HPU1doU0tyv-vY6iA-Kz93YXN9VOgg1geT2p7QQRIC7OMiGyUaP8Fga9fz_SX-VGkO0LlxfX1wQ5GXmJ5JElZAX8Luu03fLHhevp_zsRGXOgdVWxcvXWz67e169TVN2H4Bj9xGk9kRSRJNpqtdXnNs3dAY1ROThye9LNdtJ6D09QAu2ONO6fHfAi-yxmqxxVlEX0Uzx82sI6qPErt8-3NzZuYy-rj-hEJauz6Ymp7oXsvyv-27RnwawJCtarlZoxJIcC0vv2jGkcypO2cfXfWFmEbY92a_FibD65RfAdQ1pcaJNkmulQ4igS7VHraNqPGhaOrUDOWE1alYyJIj23SzBR_Y7znUaheI5XxvlLCjJnRN_iLiDgnT8LffUQlTU11DFCDdivlpsQ9hK1CJkqaYk_x3rxDLok6JnPZ47X4VFHwnpESHpBo-1QluZ-el" alt="Class Diagram" width="100%"/>
</div>

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