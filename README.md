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
<table style="font-family: monospace; border-spacing: 20px;">
    <!-- GAME (Core) -->
    <tr>
        <td colspan="4" align="center">
            <div style="border: 1px solid #999; border-radius: 5px; background: #e2f0d9; color: #333; width: 300px; text-align: left; overflow: hidden; box-shadow: 2px 2px 5px rgba(0,0,0,0.1);">
                <div style="background: #a9d08e; padding: 5px; text-align: center; font-weight: bold; border-bottom: 1px solid #999;">GAME</div>
                <div style="padding: 10px; font-size: 12px; line-height: 1.5;">
                    + mode: str<br>
                    + snakes: List<br>
                    + food: List<br>
                    + agent: QLearningAgent<br>
                    <hr style="border: 0; border-top: 1px solid #ccc; margin: 5px 0;">
                    + setUp()<br>
                    + update()<br>
                    + draw()<br>
                    + checkCollision()
                </div>
            </div>
            <div style="font-size: 20px; color: #666; margin: 5px;">| constructs |</div>
        </td>
    </tr>

    <!-- Second Row: Snake, Food, Agent -->
    <tr>
        <!-- Snake Branch -->
        <td valign="top" align="center">
            <div style="border: 1px solid #999; border-radius: 5px; background: #deebf7; color: #333; width: 220px; text-align: left; overflow: hidden;">
                <div style="background: #9bc2e6; padding: 5px; text-align: center; font-weight: bold; border-bottom: 1px solid #999;">Snake</div>
                <div style="padding: 10px; font-size: 12px; line-height: 1.5;">
                    + body: List[Rect]<br>
                    + length: int<br>
                    + score: int<br>
                    + direction: Vector2<br>
                    <hr style="border: 0; border-top: 1px solid #ccc; margin: 5px 0;">
                    + move()<br>
                    + draw()<br>
                    + grow()<br>
                    + set_skin()
                </div>
            </div>
            <div style="font-size: 20px; color: #666;">▲</div>
            
            <!-- Snake Subclasses -->
             <div style="display: flex; gap: 10px; justify-content: center; margin-top: 5px;">
                <!-- Player Snake -->
                <div style="border: 1px solid #999; border-radius: 5px; background: #deebf7; color: #333; width: 140px; text-align: left;">
                    <div style="background: #9bc2e6; padding: 3px; text-align: center; font-weight: bold; font-size: 11px;">PlayerSnake</div>
                    <div style="padding: 5px; font-size: 10px;">
                        &lt;&lt;Player&gt;&gt;<br>
                        + updateDirectionByMouse()
                    </div>
                </div>
                <!-- Computer Snake -->
                <div style="border: 1px solid #999; border-radius: 5px; background: #deebf7; color: #333; width: 140px; text-align: left;">
                    <div style="background: #9bc2e6; padding: 3px; text-align: center; font-weight: bold; font-size: 11px;">ComputerSnake</div>
                    <div style="padding: 5px; font-size: 10px;">
                        &lt;&lt;AI&gt;&gt;<br>
                        + angle: float<br>
                        + stateOld: tuple<br>
                        + performAction()<br>
                    </div>
                </div>
            </div>
        </td>

        <!-- Connector Space -->
        <td width="20"></td>

        <!-- Food Branch -->
        <td valign="top" align="center">
            <div style="border: 1px solid #999; border-radius: 5px; background: #fff2cc; color: #333; width: 220px; text-align: left; overflow: hidden;">
                <div style="background: #ffd966; padding: 5px; text-align: center; font-weight: bold; border-bottom: 1px solid #999;">Food</div>
                <div style="padding: 10px; font-size: 12px; line-height: 1.5;">
                    + x, y: int<br>
                    + type: str<br>
                    + growthValue: int<br>
                    <hr style="border: 0; border-top: 1px solid #ccc; margin: 5px 0;">
                    + draw()
                </div>
            </div>
            <div style="font-size: 20px; color: #666;">▲</div>
             <!-- Food Subclasses as a simple list block -->
            <div style="border: 1px dashed #999; border-radius: 5px; background: #fff2cc; color: #666; width: 200px; padding: 5px; font-size: 11px;">
                Subclasses:<br>
                SmallFood, MediumFood, LargeFood
            </div>
        </td>
    </tr>
    
    <!-- Third Branch: Agent (Connected to GAME somewhat separately in layout but logic wise it's a part) -->
    <tr>
        <td colspan="4" align="center" style="padding-top: 20px;">
             <div style="font-size: 20px; color: #666;">| integrates |</div>
             <div style="border: 1px solid #999; border-radius: 5px; background: #e1d5e7; color: #333; width: 280px; text-align: left; overflow: hidden;">
                <div style="background: #b4a7d6; padding: 5px; text-align: center; font-weight: bold; border-bottom: 1px solid #999;">QLearningAgent</div>
                <div style="padding: 10px; font-size: 12px; line-height: 1.5;">
                    + qTable: dict<br>
                    + epsilon: float<br>
                    + lr: float<br>
                    <hr style="border: 0; border-top: 1px solid #ccc; margin: 5px 0;">
                    + getQValue(state, action)<br>
                    + chooseAction(state)<br>
                    + learn(state, action, reward, next)
                </div>
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