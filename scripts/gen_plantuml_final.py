import zlib
import base64

def plantuml_encode(text):
    """Encode text for PlantUML server URL."""
    zlibbed_str = zlib.compress(text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return encode64(compressed_string)

def encode64(b):
    """Encodes the byte string b into PlantUML's Base64."""
    _b64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    r = ""
    for i in range(0, len(b), 3):
        if i + 2 == len(b):
            r += append3bytes(b[i], b[i+1], 0)
        elif i + 1 == len(b):
            r += append3bytes(b[i], 0, 0)
        else:
            r += append3bytes(b[i], b[i+1], b[i+2])
    return r

def append3bytes(b1, b2, b3):
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    _b64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    return _b64[c1] + _b64[c2] + _b64[c3] + _b64[c4]

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

url = "http://www.plantuml.com/plantuml/png/" + plantuml_encode(uml_code)
with open("state_diagram_url_final.txt", "w") as f:
    f.write(url)
