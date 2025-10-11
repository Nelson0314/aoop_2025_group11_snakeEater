# 貪食蛇大逃殺


> 一款使用 Python 與 Pygame 打造的對戰型貪吃蛇類型遊戲。本專案以物件導向程式設計為核心，計畫配合機器學習實現電腦對手的行為模式。

---

## 🌟 核心功能 (Core Features)

* **策略性擊殺機制**: 遊戲的核心玩法。當任何一條蛇的頭部撞擊到另一條蛇的身體時，前者將被擊殺。
* **死亡轉化**: 被擊殺的蛇會分解成大量的食物，為戰場提供豐富的資源獎勵。
* **無邊界地圖**: 蛇碰到地圖邊界時不會死亡，而是會沿著邊緣滑行，讓戰術應用更加靈活。
* **身體穿越**: 蛇頭可以自由穿越**自己的身體**，讓您可以做出意想不到的包圍與反殺操作。
* **物件導向架構**: 採用清晰的物件導向設計，為未來的 AI 開發與功能擴充打下堅實基礎。

## 🏛️ 物件導向結構 (OOP Design)

本專案的核心是物件導向的設計，主要包含以下幾個類別：

* `food`: 代表地圖上的食物物件。
* `map`: 管理遊戲世界的邊界與整體狀態。
* `snake` (基礎類別): 定義了所有蛇共有的屬性（身體、長度）與方法（移動、成長、繪製）。
* `playerSnake` (繼承 `snake`): 處理玩家輸入的蛇類別。
* `computerSnake` (繼承 `snake`): 為 AI 控制的蛇類別

## 🛠️ 技術棧 (Tech Stack)

* **主要語言**: Python 3
* **遊戲開發**: Pygame
* **數值運算**: NumPy

## 🚀 如何安裝與執行 (Installation & Usage)

```bash
# 1. 取得專案並進入目錄
git clone [https://github.com/Nelson0314/aoop_2025_group11_snakeEater.git](https://github.com/Nelson0314/aoop_2025_group11_snakeEater.git)
cd aoop_2025_group11_snakeEater

# 2. (建議) 建立並啟用虛擬環境
# Windows: python -m venv venv && .\venv\Scripts\activate
# macOS/Linux: python3 -m venv venv && source venv/bin/activate

# 3. 安裝所有必要的套件
pip install -r requirements.txt

# 4. 執行遊戲
python src/main.py
