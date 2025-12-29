import zlib
import textwrap

def encode(text):
    """
    Encodes text string to PlantUML URL format.
    """
    # 1. UTF-8 Encode
    data = text.encode('utf-8')
    
    # 2. Deflate Compression (Raw, no zlib header)
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed_data = compressor.compress(data) + compressor.flush()

    # 3. Custom Base64 Encoding
    # Start with standard, but we have to do it manually or via mapping.
    # PlantUML mapping is unique.
    # It takes 3 bytes (24 bits) -> 4 chars (6 bits each).
    # 0-63 value maps to: 0-9, A-Z, a-z, -, _
    
    plantuml_alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    
    res = ""
    i = 0
    while i < len(compressed_data):
        b1 = compressed_data[i]
        b2 = compressed_data[i+1] if i+1 < len(compressed_data) else 0
        b3 = compressed_data[i+2] if i+2 < len(compressed_data) else 0
        
        # 24-bit integer
        triple = (b1 << 16) | (b2 << 8) | b3
        
        # Four 6-bit indices
        c1 = (triple >> 18) & 0x3F
        c2 = (triple >> 12) & 0x3F
        c3 = (triple >> 6) & 0x3F
        c4 = triple & 0x3F
        
        res += plantuml_alphabet[c1]
        res += plantuml_alphabet[c2]
        res += plantuml_alphabet[c3]
        res += plantuml_alphabet[c4]
        
        i += 3
        
    # Handling padding logic specific to PlantUML?
    # Actually, PlantUML doesn't use padding chars like '='.
    # It just truncates.
    # If len % 3 == 1: we have 2 extra bytes (0), used 2 chars?
    # Wait, my manual encoding above always produces 4 chars for 3 bytes.
    # If we have 1 byte left: b1, 0, 0. We need 2 chars?
    # If we have 2 bytes left: b1, b2, 0. We need 3 chars?
    
    if len(compressed_data) % 3 == 1:
        res = res[:-2] # Check logic? 
        # 1 byte -> 8 bits. We need 2 packs of 6 bits? No 8 bits = 6 + 2.
        # So we need 2 chars. 4 chars generated, remove last 2.
    elif len(compressed_data) % 3 == 2:
        res = res[:-1] # Check logic?
        # 2 bytes -> 16 bits. 6 + 6 + 4.
        # So we need 3 chars. 4 generated, remove last 1.
        
    return res

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
    encoded = encode(uml_code.strip())
    url = f"https://www.plantuml.com/plantuml/png/{encoded}"
    print("PLANTUML_URL_START")
    print(url)
    print("PLANTUML_URL_END")
except Exception as e:
    print(f"Error: {e}")
