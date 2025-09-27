# 《天机变》 - 卡牌逻辑数据结构 (Card Logic Data Structure)

版本: 2.0
日期: 2025-09-27

## 1. 核心理念

为真正实现 "数据驱动设计" 的核心理念，所有卡牌的逻辑行为都将通过一个结构化的JSON格式来定义。游戏引擎将负责解析这个结构并执行对应的游戏逻辑，而不是将卡牌效果硬编码在程序中。

本文档定义了该数据结构的标准。

## 2. 顶层结构

每张卡牌的 `.json` 文件都将遵循一个新的、扩展性更强的顶层结构。以一张基础牌为例：

```json
{
  "id": "basic_01_qian",
  "name": "乾",
  "symbol": "☰☰",
  "sequence": 1,
  "pinyin": "qian",
  "strokes": 12,
  "type": "basic",
  "core_mechanism": {
    "name": "天道酬勤",
    "description": "支付10金币和5生命值，在本轮的【解读阶段】，你爻辞效果中所有正向收益（获得金币、恢复生命、造成伤害）的数值翻倍。",
    "variants": {
      "di": {
        "name": "蓄力",
        "description": "你在【地部】发动【天道酬勤】时，支付的成本减半（只需5金币和2生命值）。",
        "effect": { }
      },
      "ren": {
        "name": "精进",
        "description": "你在【人部】发动【天道酬勤】时，除了收益翻倍，你还可以立即额外移动一格（可穿梭于不同“部”之间）。",
        "effect": { }
      },
      "tian": {
        "name": "君威",
        "description": "你在【天部】发动【天道酬勤】时，你可以指定一名盟友，使其也获得本轮收益翻倍的效果。但作为代价，在本轮结束时，你需要弃掉一张手牌。",
        "effect": { }
      }
    }
  }
}
```

## 3. 效果 (Effect) 对象结构

`"effect"` 对象是逻辑定义的核心。它由一个或多个 "动作(Action)" 组成，并可以包含条件、成本和选择。

一个 `effect` 对象可以是一个单独的 `action`，也可以是一个 `action` 数组。

```json
"effect": [
  { "action": "...", "params": { ... } },
  { "action": "...", "params": { ... } }
]
```

### 3.1 动作 (Action)

一个 "动作" 是游戏中最基本的操作单元。

**结构:**
`{ "action": "ACTION_TYPE", "params": { ... } }`

**常见动作类型 (`ACTION_TYPE`):**

| 类型 | 描述 | 参数 (`params`) |
|---|---|---|
| `MODIFY_RESOURCE` | 修改玩家资源 | `target`, `resource` (gold, health, hand_cards), `value` |
| `MOVE` | 移动棋子 | `target`, `destination`, `move_type` (normal, jump, force) |
| `APPLY_STATUS` | 对目标施加状态 | `target`, `status_id`, `duration`, `value` |
| `REMOVE_STATUS` | 移除目标状态 | `target`, `status_id` (or "all_negative") |
| `MODIFY_RULE` | 修改全局或玩家规则 | `rule_id`, `scope` (global, player), `modifier`, `duration` |
| `TRIGGER_EVENT` | 触发一个游戏事件 | `event_id` (e.g., "discourse", "litigation") |
| `CHOICE` | 给予玩家一个选择 | `target`, `options` (每个option包含description和effect) |
| `SWAP` | 交换玩家属性或位置 | `target_a`, `target_b`, `swap_type` (position, gold, hand_cards) |
| `LOOKUP` | 查看隐藏信息 | `target`, `info_type` (hand_cards, destiny_card) |
| `CREATE_ENTITY`| 在棋盘上创建实体 | `entity_type` (trap, marker, well), `position` |
| `EXECUTE_LATER` | 延迟执行效果 | `delay` (e.g., "next_turn_start"), `effect` |

### 3.2 参数详解

#### `target`

定义动作的目标。

*   **玩家目标:** `SELF`, `ALLY_SINGLE`, `ALLY_ALL`, `OPPONENT_SINGLE`, `PLAYER_ALL`, `CONTROLLER_OF_EFFECT`
*   **区域目标:** `CURRENT_ZONE`, `ADJACENT_ZONE`, `ANY_ZONE`, `PALACE_ZONES` (当前宫位所有区域)

#### `value`

定义动作的数值。可以是固定值，也可以是动态变量。

*   **固定值:** `10`, `-5`
*   **动态变量:**
    *   `VAR_PLAYER_YANG`: 玩家的阳气值
    *   `VAR_PLAYER_GOLD`: 玩家的金币
    *   `VAR_INPUT_VALUE`: 由前一个动作或选择决定的值
    *   `VAR_GAME_FUND`: 游戏基金的数额

#### `status_id`

定义状态效果。

*   `SHIELD`, `POISON`, `REGEN`, `CONFUSED`, `SLOWED`, `IMMUNE_TO_DAMAGE`, `IMMUNE_TO_NEGATIVE_EFFECTS`

#### `rule_id`

定义被修改的游戏规则。

*   `MOVEMENT_RANGE`, `HAND_LIMIT`, `GOLD_GAIN_MODIFIER`, `DAMAGE_MODIFIER`, `ZONE_REWARD_PENALTY_REVERSAL`

### 4. 示例：将《乾》卦地部效果数据化

```json
"di": {
  "name": "蓄力",
  "description": "你在【地部】发动【天道酬勤】时，支付的成本减半（只需5金币和2生命值）。",
  "effect": {
    "action": "CHOICE",
    "params": {
      "target": "SELF",
      "options": [
        {
          "description": "发动【天道酬勤】",
          "cost": [
            { "resource": "gold", "value": 5 },
            { "resource": "health", "value": 2 }
          ],
          "effect": {
            "action": "APPLY_STATUS",
            "params": {
              "target": "SELF",
              "status_id": "POSITIVE_GAIN_DOUBLED",
              "duration": 1
            }
          }
        },
        {
          "description": "不发动"
        }
      ]
    }
  }
}
```

### 5. 功能牌的实现

功能牌将通过 `APPLY_STATUS` 动作实现，将一个临时状态附加到基础牌上。

```json
// function_cuogua.json
{
  "id": "function_cuogua",
  "type": "function",
  "name": "错卦",
  "description": "将你基础牌的每一个爻都进行阴阳反转，变为一个全新的卦来解读。",
  "effect": {
    "action": "APPLY_STATUS",
    "params": {
      "target": "ATTACHED_BASE_CARD",
      "status_id": "HEXAGRAM_INVERTED",
      "duration": 1
    }
  }
}
```
游戏引擎在解读基础牌时，会检查其是否附有 `HEXAGRAM_INVERTED` 状态，若有，则在查找其效果前，先计算出反转后的卦象ID，再用新的ID去获取效果。

### 6. 结论

这个新的数据结构将提供足够的灵活性和精确度来定义游戏中所有复杂的卡牌逻辑，真正实现项目的数据驱动设计目标。这将极大地方便未来的内容更新、平衡性调整和Mod制作。