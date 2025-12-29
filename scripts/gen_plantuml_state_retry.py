import zlib
import string

def make_plantuml_url(plantuml_code):
    # Standard PlantUML encoding logic
    # 1. Encode to UTF-8
    curr = plantuml_code.encode('utf-8')
    
    # 2. Deflate compression
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed = compressor.compress(curr) + compressor.flush()
    
    # 3. Custom Base64
    # PlantUML alphabet: 0-9A-Za-z-_
    # Standard Base64: A-Za-z0-9+/
    # We need to map 6-bit chunks to the custom alphabet
    
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    
    res = []
    current_byte = 0
    bit_count = 0
    
    for b in compressed:
        current_byte = (current_byte << 8) | b
        bit_count += 8
        while bit_count >= 6:
            bit_count -= 6
            index = (current_byte >> bit_count) & 0x3F
            res.append(alphabet[index])
            
    if bit_count > 0:
        index = (current_byte << (6 - bit_count)) & 0x3F
        res.append(alphabet[index])
        
    return "http://www.plantuml.com/plantuml/png/" + "".join(res)

uml_code = """@startuml
skinparam handwritten false
skinparam monochrome false
hide circle
skinparam packageStyle rectangle
skinparam BackgroundColor White
skinparam RectangleBackgroundColor #f9f9f9
skinparam RectangleBorderColor #666
skinparam defaultFontName monospace
skinparam linetype ortho

title State Representation

package "Sensors" #e2f0d9 {
  [Vision] as Vis
  [Food] as Food
  [Combat] as Combat
  [Dir] as CurrDir
}

package "State (12 Bits)" #deebf7 {
  object "Danger" as S1
  object "Direction" as S2
  object "Food" as S3
  object "Enemy" as S4
}

package "Q-Learning" #e1d5e7 {
    map "Q-Table" as QTable {
        Key => State
        Value => Q-Values
    }
}

package "Actions (6)" #fff2cc {
    map "Action" as Actions {
        0 => Straight
        1 => Left
        2 => Right
        3 => Boost
    }
}

Vis --> S1
CurrDir --> S2
Food --> S3
Combat --> S4

S1 --> QTable
S2 --> QTable
S3 --> QTable
S4 --> QTable

QTable --> Actions

@enduml"""

# Use a slightly simplified diagram to avoid length limits initially
url = make_plantuml_url(uml_code)

with open("state_diagram_url_retry.txt", "w") as f:
    f.write(url)
