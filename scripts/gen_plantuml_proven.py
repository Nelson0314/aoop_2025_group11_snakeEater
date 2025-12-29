import zlib
import base64
import string

def encode_plantuml(plantuml_code):
    # 1. UTF-8 Encode
    utf8_bytes = plantuml_code.encode('utf-8')
    
    # 2. Deflate Compression (no header)
    compressor = zlib.compressobj(level=9, wbits=-15)
    compressed_bytes = compressor.compress(utf8_bytes) + compressor.flush()
    
    # 3. Custom Base64 Mapping
    plantuml_b64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    
    current = 0
    rem = 0
    res = []
    
    for byte in compressed_bytes:
        current = (current << 8) | byte
        rem += 8
        while rem >= 6:
            rem -= 6
            res.append(plantuml_b64[(current >> rem) & 63])
            
    if rem > 0:
        res.append(plantuml_b64[(current << (6 - rem)) & 63])
        
    return "".join(res)

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

code = encode_plantuml(uml_code)
# Add some debug print to file to verify length
with open("state_diagram_url_proven.txt", "w") as f:
    f.write(f"http://www.plantuml.com/plantuml/png/{code}")
