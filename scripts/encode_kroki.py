import zlib
import base64
import textwrap

uml_code = """
@startuml
    skinparam classAttributeIconSize 0
    top to bottom direction

    class GAME {
        +init(screen, mode)
        +handleEvent()
        +update()
        +draw()
        +checkCollision(snake)
        +checkDeaths()
    }

    class SimpleGAME {
        +update()
    }
    GAME <|-- SimpleGAME

    class StrategyGAME {
        +spawn_strategy_snakes()
    }
    GAME <|-- StrategyGAME

    class Snake {
        +move()
        +draw()
        +grow()
    }
    
    class ComputerSnake {
        +chooseAction(state)
    }
    Snake <|-- ComputerSnake

    class playerSnake {
        +updateDirectionByMouse()
    }
    Snake <|-- playerSnake
    
    class KeyboardSnake {
        +updateDirectionByKeys()
    }
    Snake <|-- KeyboardSnake

    interface SnakeStrategy {
        +decide_action(snake, context)
    }
    class RandomStrategy
    class SimpleAIStrategy
    class AdvancedAIStrategy
    
    SnakeStrategy <|.. RandomStrategy
    SnakeStrategy <|.. SimpleAIStrategy
    SnakeStrategy <|.. AdvancedAIStrategy
    ComputerSnake o-- SnakeStrategy

    class QLearningAgent {
        +chooseAction(state)
        +learn(state, action, reward, next_state)
    }
    
    class SimpleQLearningAgent
    QLearningAgent <|-- SimpleQLearningAgent

    class SpatialGrid {
        +insert(snake)
        +get_potential_colliders(rect)
    }
    GAME o-- SpatialGrid : Composition
    
    GAME *-- Snake
    strategy_demo ..> StrategyGAME
    simple_learn ..> SimpleGAME
@enduml
"""

try:
    # Kroki expects:
    # 1. UTF-8 string
    data = uml_code.strip().encode('utf-8')
    # 2. Compressed using zlib (max compression)
    compressed = zlib.compress(data, level=9)
    # 3. Base64 (URL Safe)
    encoded = base64.urlsafe_b64encode(compressed).decode('ascii')
    
    url = f"https://kroki.io/plantuml/svg/{encoded}"
    print("KROKI_URL_START")
    print(url)
    print("KROKI_URL_END")
except Exception as e:
    print(f"Error: {e}")
