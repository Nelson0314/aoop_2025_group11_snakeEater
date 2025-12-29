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
  <img src="https://mermaid.ink/img/eyJjb2RlIjogImNsYXNzRGlhZ3JhbVxuICAgICUlIFN0eWxpbmcgLSBMb3cgU2F0dXJhdGlvbiAvIFBhc3RlbFxuICAgIGNsYXNzRGVmIGRlZmF1bHQgZmlsbDojZjlmOWY5LHN0cm9rZTojOTk5LHN0cm9rZS13aWR0aDoxcHgsY29sb3I6IzMzMztcbiAgICBjbGFzc0RlZiBjb3JlIGZpbGw6I2UyZjBkOSxzdHJva2U6I2E5ZDA4ZTtcbiAgICBjbGFzc0RlZiBlbnRpdHkgZmlsbDojZGVlYmY3LHN0cm9rZTojOWJjMmU2O1xuICAgIGNsYXNzRGVmIGl0ZW0gZmlsbDojZmZmMmNjLHN0cm9rZTojZmZkOTY2O1xuICAgIGNsYXNzRGVmIGFpIGZpbGw6I2UxZDVlNyxzdHJva2U6I2I0YTdkNjtcblxuICAgIGNsYXNzIEdBTUUge1xuICAgICAgICArbW9kZTogc3RyXG4gICAgICAgICtzbmFrZXM6IExpc3RcbiAgICAgICAgK2Zvb2Q6IExpc3RcbiAgICAgICAgK2FnZW50OiBRTGVhcm5pbmdBZ2VudFxuICAgICAgICArc2V0VXAoKVxuICAgICAgICArdXBkYXRlKClcbiAgICAgICAgK2RyYXcoKVxuICAgICAgICArY2hlY2tDb2xsaXNpb24oKVxuICAgIH1cbiAgICBcbiAgICBjbGFzcyBTbmFrZSB7XG4gICAgICAgICtib2R5OiBMaXN0W1JlY3RdXG4gICAgICAgICtsZW5ndGg6IGludFxuICAgICAgICArc2NvcmU6IGludFxuICAgICAgICArZGlyZWN0aW9uOiBWZWN0b3IyXG4gICAgICAgICttb3ZlKClcbiAgICAgICAgK2RyYXcoKVxuICAgICAgICArZ3JvdygpXG4gICAgICAgICtzZXRfc2tpbigpXG4gICAgfVxuICAgIFxuICAgIGNsYXNzIFBsYXllclNuYWtlIHtcbiAgICAgICAgPDxQbGF5ZXIgQ29udHJvbHM-PlxuICAgICAgICArdXBkYXRlRGlyZWN0aW9uQnlNb3VzZSgpXG4gICAgfVxuICAgIFxuICAgIGNsYXNzIENvbXB1dGVyU25ha2Uge1xuICAgICAgICA8PEFJIENvbnRyb2xsZWQ-PlxuICAgICAgICArYW5nbGU6IGZsb2F0XG4gICAgICAgICtzdGF0ZU9sZDogdHVwbGVcbiAgICAgICAgK3BlcmZvcm1BY3Rpb24oYWN0aW9uKVxuICAgICAgICArdXBkYXRlRGlyZWN0aW9uKClcbiAgICB9XG5cbiAgICBjbGFzcyBGb29kIHtcbiAgICAgICAgK3g6IGludFxuICAgICAgICAreTogaW50XG4gICAgICAgICt0eXBlOiBzdHJcbiAgICAgICAgK2dyb3d0aFZhbHVlOiBpbnRcbiAgICAgICAgK2RyYXcoKVxuICAgIH1cbiAgICBjbGFzcyBTbWFsbEZvb2RcbiAgICBjbGFzcyBNZWRpdW1Gb29kXG4gICAgY2xhc3MgTGFyZ2VGb29kXG4gICAgXG4gICAgY2xhc3MgUUxlYXJuaW5nQWdlbnQge1xuICAgICAgICArcVRhYmxlOiBkaWN0XG4gICAgICAgICtlcHNpbG9uOiBmbG9hdFxuICAgICAgICArbHI6IGZsb2F0XG4gICAgICAgICtnZXRRVmFsdWUoc3RhdGUsIGFjdGlvbilcbiAgICAgICAgK2Nob29zZUFjdGlvbihzdGF0ZSlcbiAgICAgICAgK2xlYXJuKHN0YXRlLCBhY3Rpb24sIHJld2FyZCwgbmV4dF9zdGF0ZSlcbiAgICB9XG5cbiAgICAlJSBSZWxhdGlvbnNoaXBzXG4gICAgR0FNRSAqLS0gU25ha2UgOiBtYW5hZ2VzXG4gICAgR0FNRSAqLS0gRm9vZCA6IG1hbmFnZXNcbiAgICBHQU1FIC0tPiBRTGVhcm5pbmdBZ2VudCA6IGludGVncmF0ZXNcbiAgICBTbmFrZSA8fC0tIFBsYXllclNuYWtlIDogaW5oZXJpdGFuY2VcbiAgICBTbmFrZSA8fC0tIENvbXB1dGVyU25ha2UgOiBpbmhlcml0YW5jZVxuICAgIEZvb2QgPHwtLSBTbWFsbEZvb2QgOiBpbmhlcml0YW5jZVxuICAgIEZvb2QgPHwtLSBNZWRpdW1Gb29kIDogaW5oZXJpdGFuY2VcbiAgICBGb29kIDx8LS0gTGFyZ2VGb29kIDogaW5oZXJpdGFuY2VcblxuICAgICUlIEFwcGx5aW5nIFN0eWxlc1xuICAgIGNsYXNzIEdBTUUgY29yZVxuICAgIGNsYXNzIFNuYWtlIGVudGl0eVxuICAgIGNsYXNzIFBsYXllclNuYWtlIGVudGl0eVxuICAgIGNsYXNzIENvbXB1dGVyU25ha2UgZW50aXR5XG4gICAgY2xhc3MgRm9vZCBpdGVtXG4gICAgY2xhc3MgU21hbGxGb29kIGl0ZW1cbiAgICBjbGFzcyBNZWRpdW1Gb29kIGl0ZW1cbiAgICBjbGFzcyBMYXJnZUZvb2QgaXRlbVxuICAgIGNsYXNzIFFMZWFybmluZ0FnZW50IGFpIiwgIm1lcm1haWQiOiB7InRoZW1lIjogImRlZmF1bHQifX0=" alt="Class Diagram" width="100%"/>
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