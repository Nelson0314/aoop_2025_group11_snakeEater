import base64
import json

mermaid_code = """graph TD
    classDef sensor fill:#e2f0d9,stroke:#a9d08e,color:#333;
    classDef state fill:#deebf7,stroke:#9bc2e6,color:#333;
    classDef ai fill:#e1d5e7,stroke:#b4a7d6,color:#333;
    classDef action fill:#fff2cc,stroke:#ffd966,color:#333;

    subgraph Sensors [1. Environmental Sensors]
        Vis[Vision: 3 pts]
        Food[Food Sensor]
        Combat[Combat Awareness]
        CurrDir[Current Direction]
    end

    subgraph StateVec [2. State Vector (12 Bits)]
        S1[Danger (3)]
        S2[Direction (4)]
        S3[Food Loc (4)]
        S4[Combat (1)]
    end

    subgraph Intelligence [3. Q-Learning Core]
        QTable[Q-Table Lookup]
    end

    subgraph Act [4. Chosen Action]
        Actions[Action Space (6)]
    end

    Vis --> S1
    CurrDir --> S2
    Food --> S3
    Combat --> S4

    S1 --> QTable
    S2 --> QTable
    S3 --> QTable
    S4 --> QTable

    QTable --> Actions

    class Vis,Food,Combat,CurrDir sensor;
    class S1,S2,S3,S4 state;
    class QTable ai;
    class Actions action;"""

# Mermaid.ink expects base64 encoded JSON: {"code": "..."}
data = {"code": mermaid_code, "mermaid": {"theme": "default"}}
json_str = json.dumps(data)
encoded = base64.urlsafe_b64encode(json_str.encode('utf-8')).decode('utf-8')

with open("state_diagram_mermaid_url.txt", "w") as f:
    f.write(f"https://mermaid.ink/img/{encoded}")
