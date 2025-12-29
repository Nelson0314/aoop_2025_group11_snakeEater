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

<div align="center">

<h3>System Architecture</h3>

<table border="0" cellspacing="10" cellpadding="10" width="80%">
  <!-- Level 1: Core -->
  <tr>
    <td colspan="3" align="center">
        <kbd><strong>GAME</strong></kbd><br>
        <sub>Core Controller</sub><br>
        <br>
        <span style="font-size: 20px;">⬇️</span>
    </td>
  </tr>

  <!-- Level 2: Sub-Systems -->
  <tr>
    <!-- Entities -->
    <td align="center" valign="top" width="33%">
        <kbd><strong>Snake</strong></kbd><br>
        <sub>Base Entity</sub><br>
        <span style="font-size: 20px;">⬇️</span><br>
        <br>
        <table border="0">
            <tr>
                <td align="center"><kbd>Player<br>Snake</kbd></td>
                <td align="center"><kbd>Computer<br>Snake</kbd></td>
            </tr>
        </table>
    </td>

    <!-- Items -->
    <td align="center" valign="top" width="33%">
        <kbd><strong>Food</strong></kbd><br>
        <sub>Item System</sub><br>
        <span style="font-size: 20px;">⬇️</span><br>
        <br>
        <kbd>Small</kbd> <kbd>Medium</kbd> <kbd>Large</kbd>
    </td>

    <!-- AI -->
    <td align="center" valign="top" width="33%">
        <kbd><strong>QLearningAgent</strong></kbd><br>
        <sub>AI Brain</sub><br>
        <br>
        <div align="left">
        <small>
        • Q-Table<br>
        • Epsilon-Greedy<br>
        • Bellman Eq.
        </small>
        </div>
    </td>
  </tr>
</table>

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