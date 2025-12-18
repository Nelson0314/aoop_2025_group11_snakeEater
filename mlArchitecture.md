# Machine Learning Architecture & Flow

這個文檔說明了目前的 **Q-Learning** 架構。

## 1. 訓練流程 (Training Loop)

每一隻 AI 蛇在每一幀 (Frame) 都會經歷以下步驟：

1.  **觀察環境 (Get State)**: 獲取當前的 11-bit 狀態。
2.  **查表決策 (Select Action)**:
    *   90% 機率：選擇 Q 值最高的動作 (經驗)。
    *   10% 機率：隨機選擇動作 (探索)。
3.  **執行動作 (Perform Action)**: 直走、左轉或右轉。
4.  **環境更新**: 移動蛇的位置，檢查碰撞。
5.  **領取獎勵 (Reward)**:
    *   **沒事發生**: +0.1 分 (生存獎勵)
    *   **吃到食物**: +50 分
    *   **擊殺敵人**: +200 分 (迫使別人撞到我)
    *   **撞牆/死**: -100 分
6.  **學習 (Update Q-Table)**: 根據公式更新 Q 表。
7.  **循環**: 回到步驟 1。

## 2. 狀態機定義 (Finite State Definition)

我們將連續的遊戲畫面簡化為有限的 **11 個 bit** (True/False)，組合成一個 Tuple 作為 State ID。
這意味著總共有 $2^{11} = 2048$ 種可能的狀態。

### 狀態組成 (11 bits)

| 類別 | 特徵 | 說明 |
| :--- | :--- | :--- |
| **危險偵測 (Danger)** <br> (3 bits) | `danger_straight` | 前方 3 格內有障礙物 (牆壁或別人身體) |
| | `danger_right` | 右前方 3 格內有障礙物 |
| | `danger_left` | 左前方 3 格內有障礙物 |
| **目前方向 (Moving)** <br> (4 bits) | `dir_left` | 目前是否向左移動 (Velocity X < 0) |
| | `dir_right` | 目前是否向右移動 (Velocity X > 0) |
| | `dir_up` | 目前是否向上移動 (Velocity Y < 0) |
| | `dir_down` | 目前是否向下移動 (Velocity Y > 0) |
| **食物方位 (Food)** <br> (4 bits) | `food_left` | 最近的食物在左邊 |
| | `food_right` | 最近的食物在右邊 |
| | `food_up` | 最近的食物在上方 |
| | `food_down` | 最近的食物在下方 |

## 3. 動作空間 (Action Space)

AI 只能選擇以下三種動作之一：

| Action ID | 動作 | 說明 |
| :---: | :--- | :--- |
| **0** | **直走** (Straight) | 保持目前方向不變 |
| **1** | **左轉** (Left) | 向左轉 `config.TURN_ANGLE` 度 |
| **2** | **右轉** (Right) | 向右轉 `config.TURN_ANGLE` 度 |

## 4. 學習公式 (Q-Learning Update)

$$Q(S, A) \leftarrow Q(S, A) + \alpha [R + \gamma \max Q(S', a) - Q(S, A)]$$

*   $\alpha$ (`LEARNING_RATE`): 學習率 (目前設 0.1)
*   $\gamma$ (`DISCOUNT_FACTOR`): 遠見程度 (目前設 0.9)
