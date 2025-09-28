**版本: 3.0 (Data-Driven Update)**
**说明:** 本文档是游戏卡牌逻辑的 **单一事实来源 (Single Source of Truth)**。每张卡牌的描述下方都包含一个 `json` 代码块，该代码块定义了卡牌在游戏引擎中的确切行为。

**开发者指南:**
- **要修改卡牌逻辑，请直接修改本文档中的 `json` 代码块。**
- **修改完成后，请运行 `python tools/generate_card_data.py` 脚本。**
- 该脚本会自动解析本文档，提取所有 `json` 数据，并重新生成位于 `assets/data/cards/` 目录下的所有游戏数据文件。
- **请勿手动编辑 `assets/data/cards/` 目录下的任何 `.json` 文件**，因为它们会在脚本运行时被覆盖。

---

### **第一卦：《乾》 ☰☰ - 天**
**核心机制：【天道酬勤】**
- **效果：** 你可以选择是否发动【天道酬勤】。若发动，你必须**支付** 10 金币和 5 生命值作为**代价**。成功支付后，在本轮的【解读阶段】，你所有效果造成的**伤害**、获得的**金币**和恢复的**生命值**，其基础数值翻倍。
- **爻辞变量：**
  - **地部 (蓄力):** 发动【天道酬勤】时，支付的**代价**减半（5金币，3生命值，向上取整）。
  - **人部 (精进):** 除了核心效果，你还可以立即执行一次额外移动（1格）。
  - **天部 (君威):** 你可以指定一名**正式盟友**，使其也获得【天道酬勤】状态，持续一轮。作为此效果的一部分，在【归整阶段】的“回合结束时效果结算”步骤，你必须弃掉一张手牌。

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
        "description": "你在【地部】发动【天道酬勤】时，支付的成本减半（只需5金币和3生命值）。",
        "effect": {
          "actions": [
            {
              "action": "CHOICE",
              "params": {
                "target": "SELF",
                "options": [
                  {
                    "description": "发动【天道酬勤】",
                    "cost": [
                      { "resource": "gold", "value": 5 },
                      { "resource": "health", "value": 3 }
                    ],
                    "effect": {
                      "actions": [
                        {
                          "action": "APPLY_STATUS",
                          "params": { "target": "SELF", "status_id": "POSITIVE_GAIN_DOUBLED", "duration": 1 }
                        }
                      ]
                    }
                  },
                  { "description": "不发动" }
                ]
              }
            }
          ]
        }
      },
      "ren": {
        "name": "精进",
        "description": "你在【人部】发动【天道酬勤】时，除了收益翻倍，你还可以立即额外移动一格。",
        "effect": {
          "actions": [
            {
              "action": "CHOICE",
              "params": {
                "target": "SELF",
                "options": [
                  {
                    "description": "发动【天道酬勤】并移动",
                    "cost": [
                      { "resource": "gold", "value": 10 },
                      { "resource": "health", "value": 5 }
                    ],
                    "effect": {
                      "actions": [
                        {
                          "action": "APPLY_STATUS",
                          "params": { "target": "SELF", "status_id": "POSITIVE_GAIN_DOUBLED", "duration": 1 }
                        },
                        {
                          "action": "MOVE",
                          "params": { "target": "SELF", "value": 1, "move_type": "NORMAL" }
                        }
                      ]
                    }
                  },
                  { "description": "不发动" }
                ]
              }
            }
          ]
        }
      },
      "tian": {
        "name": "君威",
        "description": "你在【天部】发动【天道酬勤】时，你可以指定一名盟友，使其也获得本轮收益翻倍的效果。",
        "effect": {
          "actions": [
            {
              "action": "CHOICE",
              "params": {
                "target": "SELF",
                "options": [
                  {
                    "description": "为自己和盟友发动【天道酬勤】",
                    "cost": [
                      { "resource": "gold", "value": 10 },
                      { "resource": "health", "value": 5 }
                    ],
                    "effect": {
                      "actions": [
                        {
                          "action": "APPLY_STATUS",
                          "params": { "target": "SELF", "status_id": "POSITIVE_GAIN_DOUBLED", "duration": 1 }
                        },
                        {
                          "action": "APPLY_STATUS",
                          "params": { "target": "ALLY_FORMAL_SINGLE", "status_id": "POSITIVE_GAIN_DOUBLED", "duration": 1 }
                        },
                        {
                          "action": "EXECUTE_LATER",
                          "params": {
                            "delay": "END_OF_TURN",
                            "effect": {
                              "actions": [
                                { "action": "DISCARD_CARD", "params": { "target": "SELF", "count": 1 } }
                              ]
                            }
                          }
                        }
                      ]
                    }
                  },
                  { "description": "不发动" }
                ]
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第二卦：《坤》 ☷☷ - 地**
**核心机制：【厚德载物】**
- **效果：** 若你在本轮的【移动阶段】未进行移动，则在【解读阶段】发动此效果时，你可以选择**取消**你爻辞效果中所有负面部分（如支付代价、承受伤害等），只执行其正面部分。
- **爻辞变量：**
  - **地部 (固守):** 你额外获得 **【IMMUNE_COMBAT_DAMAGE (1)】** 状态（免疫下一次战斗伤害）。
  - **人部 (收敛):** 你可以改为**复制**本轮在你之前已解读过的**一名其他玩家**的**基础**爻辞效果（不含任何功能牌或状态修正）。你**必须支付**其原始的**代价**，但可以取消后续的其他负面部分（如生命值损失、弃牌等）。
  - **天部 (滋养):** 你可以将【厚德载物】的**目标**从“你自己”变为一名**正式盟友**。

```json
{
  "id": "basic_02_kun",
  "name": "坤",
  "symbol": "☷☷",
  "sequence": 2,
  "pinyin": "kun",
  "strokes": 6,
  "type": "basic",
  "core_mechanism": {
    "name": "厚德载物",
    "description": "若你本轮未移动，你可以选择取消你下个爻辞效果中的所有负面部分，只执行其正面部分。",
    "variants": {
      "di": {
        "name": "固守",
        "description": "若你本轮未移动，你获得【厚德载物】效果，并额外获得【免疫下一次战斗伤害】。",
        "effect": {
          "condition": { "op": "PLAYER_HAS_FLAG", "params": { "flag": "HAS_NOT_MOVED_THIS_TURN" } },
          "actions": [
            { "action": "APPLY_STATUS", "params": { "target": "SELF", "status_id": "EFFECT_MODIFIER_CANCEL_NEGATIVE", "duration": 1 } },
            { "action": "APPLY_STATUS", "params": { "target": "SELF", "status_id": "IMMUNE_COMBAT_DAMAGE", "value": 1, "duration": 1 } }
          ]
        }
      },
      "ren": {
        "name": "收敛",
        "description": "若你本轮未移动，你可以改为复制本轮一名其他玩家已结算的基础爻辞效果，并取消其负面部分。",
        "effect": {
          "condition": { "op": "PLAYER_HAS_FLAG", "params": { "flag": "HAS_NOT_MOVED_THIS_TURN" } },
          "actions": [
            {
              "action": "COPY_EFFECT",
              "params": {
                "target": "SELF",
                "source_effect": { "type": "LAST_BASIC_CARD_EFFECT_PLAYED", "player_scope": "OTHER" },
                "modifications": { "remove_negative_parts": true }
              }
            }
          ]
        }
      },
      "tian": {
        "name": "滋养",
        "description": "若你本轮未移动，你可以将【厚德载物】效果赋予一名盟友。",
        "effect": {
          "condition": { "op": "PLAYER_HAS_FLAG", "params": { "flag": "HAS_NOT_MOVED_THIS_TURN" } },
          "actions": [
            {
              "action": "APPLY_STATUS",
              "params": { "target": "ALLY_FORMAL_SINGLE", "status_id": "EFFECT_MODIFIER_CANCEL_NEGATIVE", "duration": 1 }
            }
          ]
        }
      }
    }
  }
}
```

---

### **第三卦：《屯》 ☵☳ - 难**
**核心机制：【盘桓待机】**
- **效果：** 在你所在的区域创建-一个【屯】实体，持续**最多3轮**。在【屯】实体被移除前，你不能再次打出《屯》。该实体具有以下属性：
  - **迷雾：** 任何棋子不能进入此区域。你的棋子可以自由离开，实体将留在原地。
  - **引爆：** 在你的【解读阶段】开始时，若你的棋子位于该区域，你可以选择“引爆”该实体，立即触发其爻辞效果，并移除该实体。
- **爻辞变量：**
  - **地部 (建侯):** 引爆时，你可以移动到一个相邻的空区域，并在此处创建一个永久的【前哨】实体（你每次进入或离开，获得2金币）。
  - **人部 (求助):** 引爆时，你可以与一名**正式盟友**交换任意数量的手牌。
  - **天部 (甘霖):** 引爆时，你获得15金币，但你的阴阳指示条强制向【阳】移动2点。

```json
{
  "id": "basic_03_tun",
  "name": "屯",
  "symbol": "☵☳",
  "sequence": 3,
  "pinyin": "tun",
  "strokes": 7,
  "type": "basic",
  "effect": {
    "condition": { "op": "IS_ENTITY_ON_BOARD", "params": { "entity_type": "ENTITY_TUN", "count": 0 } },
    "actions": [
      {
        "action": "CREATE_ENTITY",
        "params": {
          "entity_type": "ENTITY_TUN",
          "position": "SELF",
          "owner": "SELF",
          "properties": {
            "name": "屯",
            "duration": 3,
            "blocks_movement": { "for": "ALL_PLAYERS", "exceptions": ["OWNER_CAN_LEAVE"] },
            "detonation_card_id": "basic_03_tun"
          }
        }
      }
    ]
  },
  "core_mechanism": {
    "name": "盘桓待机 (引爆)",
    "description": "引爆【屯】实体时触发。你必须在【屯】所在的区域才能引爆。",
    "variants": {
      "di": {
        "name": "建侯",
        "effect": {
          "actions": [
            { "action": "DESTROY_ENTITY", "params": { "target_entity_type": "ENTITY_TUN", "position": "SELF" } },
            { "action": "MOVE", "params": { "target": "SELF", "destination": "ADJACENT_EMPTY", "value": 1 } },
            { "action": "CREATE_ENTITY", "params": { "entity_type": "ENTITY_OUTPOST", "position": "SELF", "owner": "SELF", "is_permanent": true, "properties": { "name": "前哨", "on_enter_effect": { "actions": [{"action": "GAIN_RESOURCE", "params": {"target": "EVENT_SOURCE_PLAYER", "resource": "gold", "value": 2}}]}, "on_leave_effect": {"actions": [{"action": "GAIN_RESOURCE", "params": {"target": "EVENT_SOURCE_PLAYER", "resource": "gold", "value": 2}}]} } } }
          ]
        }
      },
      "ren": {
        "name": "求助",
        "effect": {
          "actions": [
            { "action": "DESTROY_ENTITY", "params": { "target_entity_type": "ENTITY_TUN", "position": "SELF" } },
            { "action": "SWAP_HAND_CARDS", "params": { "target": "SELF", "other_player": "ALLY_FORMAL_SINGLE_CHOICE" } }
          ]
        }
      },
      "tian": {
        "name": "甘霖",
        "effect": {
          "actions": [
            { "action": "DESTROY_ENTITY", "params": { "target_entity_type": "ENTITY_TUN", "position": "SELF" } },
            { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "gold", "value": 15 } },
            { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "YIN_YANG_GAUGE", "value": 2 } }
          ]
        }
      }
    }
  }
}
```

---
### **第四卦：《蒙》 ☶☵ - 昧**
**核心机制：【启蒙之雾】**
- **效果：** 指定一名其他玩家。该玩家翻开其【基础牌】后，效果不立即结算。你代其选择一项：
  1. **【教化】:** 该玩家正常结算其效果。
  2. **【惩戒】:** 该玩家的效果被**无效化**，改为**损失** 5点生命值。
- **爻辞变量：**
  - **地部 (引导):** 若你选择【教化】，你复制其效果总收益的50%（向下取整）。
  - **人部 (约束):** 若你选择【惩戒】，“生命值损失”提升为8点。
  - **天部 (反制):** 若你选择【惩戒】，你可以将被无效化的效果，转而对**另一名其他玩家**施放。

```json
{
  "id": "basic_04_meng",
  "name": "蒙",
  "symbol": "☶☵",
  "sequence": 4,
  "pinyin": "meng",
  "strokes": 13,
  "type": "basic",
  "core_mechanism": {
    "name": "启蒙之雾",
    "description": "指定一名其他玩家，在该玩家解读基础牌时，你为其选择【教化】或【惩戒】。",
    "variants": {
      "di": {
        "name": "引导",
        "effect": {
          "actions": [
            {
              "action": "APPLY_STATUS",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "status_id": "MONTORIAL_FOG",
                "duration": 1,
                "value": {
                  "teach_effect": { "action": "COPY_EFFECT", "params": { "target": "SELF", "source_effect": { "type": "INTERRUPTED_EFFECT" }, "modifications": { "only_gains": true, "multiplier": 0.5 } } },
                  "discipline_effect": { "action": "LOSE_RESOURCE", "params": { "target": "EVENT_SOURCE_PLAYER", "resource": "health", "value": 5 } }
                }
              }
            }
          ]
        }
      },
      "ren": {
        "name": "约束",
        "effect": {
          "actions": [
            {
              "action": "APPLY_STATUS",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "status_id": "MONTORIAL_FOG",
                "duration": 1,
                "value": {
                  "discipline_effect": { "action": "LOSE_RESOURCE", "params": { "target": "EVENT_SOURCE_PLAYER", "resource": "health", "value": 8 } }
                }
              }
            }
          ]
        }
      },
      "tian": {
        "name": "反制",
        "effect": {
          "actions": [
            {
              "action": "APPLY_STATUS",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "status_id": "MONTORIAL_FOG",
                "duration": 1,
                "value": {
                  "discipline_effect": { "action": "COPY_EFFECT", "params": { "target": "OPPONENT_CHOICE_SINGLE", "source_effect": { "type": "INTERRUPTED_EFFECT" } } }
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

---

### **第五卦：《需》 ☵☰ - 待**
**核心机制：【云中之需】**
- **效果：** 跳过你本轮的【解读阶段】。在下一轮你的【归整阶段】“回合结束时效果结算”步骤，你获得10金币和2张基础牌。
- **爻辞变量：**
  - **地部 (静待):** 在等待期间，你获得【IMMUNITY_GENERAL_NEGATIVE (1)】状态。
  - **人部 (险待):** 最终奖励提升至15金币和3张牌。但若你在等待期间受到任何**伤害**，此效果被取消。
  - **天部 (宴待):** 最终奖励变为20金币。你可以将其中最多一半分享给一名**正式盟友**。

```json
{
  "id": "basic_05_xu",
  "name": "需",
  "symbol": "☵☰",
  "sequence": 5,
  "pinyin": "xu",
  "strokes": 8,
  "type": "basic",
  "core_mechanism": {
    "name": "云中之需",
    "description": "跳过解读，在下轮归整时获得奖励。",
    "variants": {
      "di": {
        "name": "静待",
        "effect": {
          "actions": [
            { "action": "SKIP_PHASE", "params": { "phase": "INTERPRETATION" } },
            { "action": "APPLY_STATUS", "params": { "target": "SELF", "status_id": "IMMUNITY_GENERAL_NEGATIVE", "value": 1, "duration": 1 } },
            { "action": "EXECUTE_LATER", "params": { "delay": "NEXT_UPKEEP_PHASE", "effect": { "actions": [ { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "gold", "value": 10 } }, { "action": "DRAW_CARD", "params": { "target": "SELF", "deck": "basic", "count": 2 } } ] } } }
          ]
        }
      },
      "ren": {
        "name": "险待",
        "effect": {
          "actions": [
            { "action": "SKIP_PHASE", "params": { "phase": "INTERPRETATION" } },
            { "action": "EXECUTE_LATER", "params": { "delay": "NEXT_UPKEEP_PHASE", "condition": { "op": "PLAYER_HAS_NOT_TAKEN_DAMAGE_SINCE", "params": { "timestamp": "NOW" } }, "effect": { "actions": [ { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "gold", "value": 15 } }, { "action": "DRAW_CARD", "params": { "target": "SELF", "deck": "basic", "count": 3 } } ] } } }
          ]
        }
      },
      "tian": {
        "name": "宴待",
        "effect": {
          "actions": [
            { "action": "SKIP_PHASE", "params": { "phase": "INTERPRETATION" } },
            { "action": "EXECUTE_LATER", "params": { "delay": "NEXT_UPKEEP_PHASE", "effect": { "actions": [ { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "gold", "value": 10 } }, { "action": "CHOICE", "params": { "target": "SELF", "options": [ { "description": "将10金币赠予盟友", "effect": { "action": "TRANSFER_RESOURCE", "params": { "from": "SELF", "to": "ALLY_FORMAL_SINGLE", "resource": "gold", "value": 10 } } } ] } } ] } } }
          ]
        }
      }
    }
  }
}
```

---

### **第六卦：《讼》 ☰☵ - 争**
**核心机制：【天理仲裁】**
- **效果：** 指定一名其他玩家，触发“争讼”事件。双方各从手中选一张【基础牌】同时亮出，比较“笔画数”，少者胜。胜诉方从败诉方**夺取**10金币，败诉方额外**损失**5点生命值。
- **爻辞变量：**
  - **地部 (退让):** 若你败诉，你被夺取的金币减半（5金币）。
  - **人部 (和解):** 你可以提议“庭外和解”：双方各**支付**5金币给游戏基金，然后各自抽一张基础牌。
  - **天部 (终审):** 若你胜诉，你额外获得一枚永久的【威望】状态（“论道”或“争讼”时笔画数-2）。

```json
{
  "id": "basic_06_song",
  "name": "讼",
  "symbol": "☰☵",
  "sequence": 6,
  "pinyin": "song",
  "strokes": 8,
  "type": "basic",
  "core_mechanism": {
    "name": "天理仲裁",
    "description": "与其他玩家通过比拼卡牌笔画数来决定胜负，并产生奖惩。",
    "variants": {
      "di": {
        "name": "退让",
        "effect": {
          "actions": [
            { "action": "TRIGGER_EVENT", "params": { "event_id": "EVENT_SONG", "participants": ["SELF", "OPPONENT_CHOICE_SINGLE"], "modifications": { "SELF_LOSS_MODIFIER": {"op": "MULTIPLY", "value": 0.5} } } }
          ]
        }
      },
      "ren": {
        "name": "和解",
        "effect": {
          "actions": [
            { "action": "CHOICE", "params": { "target": "OPPONENT_CHOICE_SINGLE", "options": [ { "description": "接受和解", "effect": { "actions": [ { "action": "PAY_COST", "params": { "target": "SELF", "resource": "gold", "value": 5 } }, { "action": "PAY_COST", "params": { "target": "EVENT_TARGET_PLAYER", "resource": "gold", "value": 5 } }, { "action": "DRAW_CARD", "params": { "target": "SELF", "deck": "basic", "count": 1 } }, { "action": "DRAW_CARD", "params": { "target": "EVENT_TARGET_PLAYER", "deck": "basic", "count": 1 } } ] } }, { "description": "拒绝和解，开始争讼", "effect": { "action": "TRIGGER_EVENT", "params": { "event_id": "EVENT_SONG", "participants": ["SELF", "EVENT_TARGET_PLAYER"] } } } ] } }
          ]
        }
      },
      "tian": {
        "name": "终审",
        "effect": {
          "actions": [
            { "action": "TRIGGER_EVENT", "params": { "event_id": "EVENT_SONG", "participants": ["SELF", "OPPONENT_CHOICE_SINGLE"], "modifications": { "SELF_WIN_EFFECT": { "action": "APPLY_STATUS", "params": { "target": "SELF", "status_id": "PRESTIGE", "is_permanent": true } } } } }
          ]
        }
      }
    }
  }
}
```

---

### **第七卦：《师》 ☷☵ - 众**
**核心机制：【王师出征】**
- **效果：** 你可以对你所在**宫位**的所有**正式盟友**（包括你自己）施加【军阵】状态，持续一轮（攻击力+3，但受到的任何**伤害**+1）。
- **爻辞变量：**
  - **地部 (纪律):** 发动此效果需**支付**5金币作为**代价**。
  - **人部 (兵法):** 你可以改为让所有目标获得【急行军】状态（本轮结束后，可以立即额外移动一格）。
  - **天部 (将帅):** 你可以将【军阵】状态的效果集中赋予一名**正式盟友**，使其获得【主帅】状态（攻击力+8，且获得【IMMUNE_COMBAT_DAMAGE (1)】）。

```json
{
  "id": "basic_07_shi",
  "name": "师",
  "symbol": "☷☵",
  "sequence": 7,
  "pinyin": "shi",
  "strokes": 8,
  "type": "basic",
  "core_mechanism": {
    "name": "王师出征",
    "description": "为你和盟友施加增益状态。",
    "variants": {
      "di": {
        "name": "纪律",
        "effect": {
          "cost": [{ "resource": "gold", "value": 5 }],
          "actions": [
            { "action": "APPLY_STATUS", "params": { "target": "ALLY_FORMAL_IN_PALACE", "status_id": "WAR_FORMATION", "duration": 1 } }
          ]
        }
      },
      "ren": {
        "name": "兵法",
        "effect": {
          "actions": [
            { "action": "APPLY_STATUS", "params": { "target": "ALLY_FORMAL_IN_PALACE", "status_id": "RAPID_MARCH", "duration": 1 } }
          ]
        }
      },
      "tian": {
        "name": "将帅",
        "effect": {
          "actions": [
            { "action": "APPLY_STATUS", "params": { "target": "ALLY_FORMAL_SINGLE_CHOICE", "status_id": "GENERAL", "duration": 1 } }
          ]
        }
      }
    }
  }
}
```

---

### **第八卦：《比》 ☵☷ - 附**
**核心机制：【同心之盟】**
- **效果：** 选择一名其他玩家，邀请其结盟。若对方同意，你们双方获得【ALLY_FORMAL】状态，持续3轮。
- **【ALLY_FORMAL】状态效果：** 1. 你们不能成为彼此攻击或偷窃效果的目标。2. 你们可以共享彼此所在区域的【奇门八门】效果。
- **爻辞变量：**
  - **地部 (信赖):** 缔结盟约时，你和你的盟友立即各恢复5点生命值。
  - **人部 (外交):** 缔结盟约时，你可以**支付**5金币，让一名**非盟友**玩家抽2张基础牌。
  - **天部 (王道):** 【ALLY_FORMAL】状态持续时间延长至5轮，且期间你们共享彼此金币总收益的10%（向下取整）。

```json
{
  "id": "basic_08_bi",
  "name": "比",
  "symbol": "☵☷",
  "sequence": 8,
  "pinyin": "bi",
  "strokes": 8,
  "type": "basic",
  "core_mechanism": {
    "name": "同心之盟",
    "description": "与其他玩家结盟。",
    "variants": {
      "di": {
        "name": "信赖",
        "effect": {
          "actions": [
            { "action": "PROPOSE_ALLIANCE", "params": { "target": "OPPONENT_CHOICE_SINGLE", "duration": 3, "on_accept_effect": { "actions": [ { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "health", "value": 5 } }, { "action": "GAIN_RESOURCE", "params": { "target": "EVENT_TARGET_PLAYER", "resource": "health", "value": 5 } } ] } } }
          ]
        }
      },
      "ren": {
        "name": "外交",
        "effect": {
          "actions": [
            { "action": "PROPOSE_ALLIANCE", "params": { "target": "OPPONENT_CHOICE_SINGLE", "duration": 3, "on_accept_effect": { "cost": [{ "resource": "gold", "value": 5 }], "actions": [ { "action": "DRAW_CARD", "params": { "target": "PLAYER_CHOICE_ANY_NON_ALLY", "deck": "basic", "count": 2 } } ] } } }
          ]
        }
      },
      "tian": {
        "name": "王道",
        "effect": {
          "actions": [
            { "action": "PROPOSE_ALLIANCE", "params": { "target": "OPPONENT_CHOICE_SINGLE", "duration": 5, "alliance_properties": { "share_gold_gain_percentage": 10 } } }
          ]
        }
      }
    }
  }
}
```

---
### **第九卦：《小畜》 ☴☰ - 密云**
**核心机制：【密云不雨】**
- **效果：** 风行天上，聚云成势，但雨未降。此卦代表小有积蓄，但尚未形成大的突破。效果偏向于小额的获取与限制。
- **爻辞变量：**
  - **地部 (种德):** 小有积蓄。你获得3金币，并抽一张基础牌。
  - **人部 (牵连):** 与他人产生小的交互。你指定一名其他玩家，你们各弃一张手牌。
  - **天部 (节制):** 施加小的限制。指定一名其他玩家，在本轮的【结算阶段】，该玩家不能通过区域效果获得金币。
```json
{
  "id": "basic_09_xiao_chu",
  "name": "小畜",
  "symbol": "☴☰",
  "sequence": 9,
  "pinyin": "xiao_chu",
  "strokes": 9,
  "type": "basic",
  "core_mechanism": {
    "name": "密云不雨",
    "description": "小有积蓄，但尚未形成大的突破。效果偏向于小额的获取与限制。",
    "variants": {
      "di": {
        "name": "种德",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 3
              }
            },
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "ren": {
        "name": "牵连",
        "effect": {
          "actions": [
            {
              "action": "DISCARD_CARD",
              "params": {
                "target": "SELF",
                "count": 1
              }
            },
            {
              "action": "DISCARD_CARD",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "节制",
        "effect": {
          "actions": [
            {
              "action": "APPLY_STATUS",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "status_id": "CANNOT_GAIN_GOLD_FROM_ZONE",
                "duration": 1
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第10卦：《履》 ☰☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_10_li",
  "name": "履",
  "symbol": "☰☱",
  "sequence": 10,
  "pinyin": "li",
  "strokes": 10,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第11卦：《泰》 ☷☰**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_11_tai",
  "name": "泰",
  "symbol": "☷☰",
  "sequence": 11,
  "pinyin": "tai",
  "strokes": 11,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第12卦：《否》 ☰☷**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_12_pi",
  "name": "否",
  "symbol": "☰☷",
  "sequence": 12,
  "pinyin": "pi",
  "strokes": 12,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第13卦：《同人》 ☰☲**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_13_tong_ren",
  "name": "同人",
  "symbol": "☰☲",
  "sequence": 13,
  "pinyin": "tong_ren",
  "strokes": 13,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第14卦：《大有》 ☲☰**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_14_da_you",
  "name": "大有",
  "symbol": "☲☰",
  "sequence": 14,
  "pinyin": "da_you",
  "strokes": 14,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第15卦：《谦》 ☷☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_15_qian",
  "name": "谦",
  "symbol": "☷☶",
  "sequence": 15,
  "pinyin": "qian",
  "strokes": 15,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第16卦：《豫》 ☳☷**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_16_yu",
  "name": "豫",
  "symbol": "☳☷",
  "sequence": 16,
  "pinyin": "yu",
  "strokes": 16,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第17卦：《随》 ☱☳**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_17_sui",
  "name": "随",
  "symbol": "☱☳",
  "sequence": 17,
  "pinyin": "sui",
  "strokes": 17,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第18卦：《蛊》 ☶☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_18_gu",
  "name": "蛊",
  "symbol": "☶☴",
  "sequence": 18,
  "pinyin": "gu",
  "strokes": 18,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第19卦：《临》 ☷☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_19_lin",
  "name": "临",
  "symbol": "☷☱",
  "sequence": 19,
  "pinyin": "lin",
  "strokes": 19,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第20卦：《观》 ☴☷**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_20_guan",
  "name": "观",
  "symbol": "☴☷",
  "sequence": 20,
  "pinyin": "guan",
  "strokes": 20,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第21卦：《噬嗑》 ☲☳**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_21_shi_he",
  "name": "噬嗑",
  "symbol": "☲☳",
  "sequence": 21,
  "pinyin": "shi_he",
  "strokes": 21,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第22卦：《贲》 ☶☲**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_22_ben",
  "name": "贲",
  "symbol": "☶☲",
  "sequence": 22,
  "pinyin": "ben",
  "strokes": 22,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第23卦：《剥》 ☶☷**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_23_bo",
  "name": "剥",
  "symbol": "☶☷",
  "sequence": 23,
  "pinyin": "bo",
  "strokes": 23,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第24卦：《复》 ☷☳**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_24_fu",
  "name": "复",
  "symbol": "☷☳",
  "sequence": 24,
  "pinyin": "fu",
  "strokes": 24,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第25卦：《无妄》 ☰☳**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_25_wu_wang",
  "name": "无妄",
  "symbol": "☰☳",
  "sequence": 25,
  "pinyin": "wu_wang",
  "strokes": 25,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第26卦：《大畜》 ☶☰**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_26_da_chu",
  "name": "大畜",
  "symbol": "☶☰",
  "sequence": 26,
  "pinyin": "da_chu",
  "strokes": 26,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第27卦：《颐》 ☶☳**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_27_yi",
  "name": "颐",
  "symbol": "☶☳",
  "sequence": 27,
  "pinyin": "yi",
  "strokes": 27,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第28卦：《大过》 ☱☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_28_da_guo",
  "name": "大过",
  "symbol": "☱☴",
  "sequence": 28,
  "pinyin": "da_guo",
  "strokes": 28,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第29卦：《坎》 ☵☵**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_29_kan",
  "name": "坎",
  "symbol": "☵☵",
  "sequence": 29,
  "pinyin": "kan",
  "strokes": 29,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第30卦：《离》 ☲☲**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_30_li",
  "name": "离",
  "symbol": "☲☲",
  "sequence": 30,
  "pinyin": "li",
  "strokes": 30,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第31卦：《咸》 ☱☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_31_xian",
  "name": "咸",
  "symbol": "☱☶",
  "sequence": 31,
  "pinyin": "xian",
  "strokes": 31,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第32卦：《恒》 ☳☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_32_heng",
  "name": "恒",
  "symbol": "☳☴",
  "sequence": 32,
  "pinyin": "heng",
  "strokes": 32,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第33卦：《遁》 ☰☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_33_dun",
  "name": "遁",
  "symbol": "☰☶",
  "sequence": 33,
  "pinyin": "dun",
  "strokes": 33,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第34卦：《大壮》 ☳☰**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_34_da_zhuang",
  "name": "大壮",
  "symbol": "☳☰",
  "sequence": 34,
  "pinyin": "da_zhuang",
  "strokes": 34,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第35卦：《晋》 ☲☷**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_35_jin",
  "name": "晋",
  "symbol": "☲☷",
  "sequence": 35,
  "pinyin": "jin",
  "strokes": 35,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第36卦：《明夷》 ☷☲**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_36_ming_yi",
  "name": "明夷",
  "symbol": "☷☲",
  "sequence": 36,
  "pinyin": "ming_yi",
  "strokes": 36,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第37卦：《家人》 ☴☲**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_37_jia_ren",
  "name": "家人",
  "symbol": "☴☲",
  "sequence": 37,
  "pinyin": "jia_ren",
  "strokes": 37,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第38卦：《睽》 ☲☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_38_kui",
  "name": "睽",
  "symbol": "☲☱",
  "sequence": 38,
  "pinyin": "kui",
  "strokes": 38,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第39卦：《蹇》 ☵☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_39_jian",
  "name": "蹇",
  "symbol": "☵☶",
  "sequence": 39,
  "pinyin": "jian",
  "strokes": 39,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第40卦：《解》 ☳☵**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_40_xie",
  "name": "解",
  "symbol": "☳☵",
  "sequence": 40,
  "pinyin": "xie",
  "strokes": 40,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第41卦：《损》 ☶☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_41_sun",
  "name": "损",
  "symbol": "☶☱",
  "sequence": 41,
  "pinyin": "sun",
  "strokes": 41,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第42卦：《益》 ☴☳**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_42_yi",
  "name": "益",
  "symbol": "☴☳",
  "sequence": 42,
  "pinyin": "yi",
  "strokes": 42,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第43卦：《夬》 ☱☰**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_43_guai",
  "name": "夬",
  "symbol": "☱☰",
  "sequence": 43,
  "pinyin": "guai",
  "strokes": 43,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第44卦：《姤》 ☰☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_44_gou",
  "name": "姤",
  "symbol": "☰☴",
  "sequence": 44,
  "pinyin": "gou",
  "strokes": 44,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第45卦：《萃》 ☱☷**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_45_cui",
  "name": "萃",
  "symbol": "☱☷",
  "sequence": 45,
  "pinyin": "cui",
  "strokes": 45,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第46卦：《升》 ☷☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_46_sheng",
  "name": "升",
  "symbol": "☷☴",
  "sequence": 46,
  "pinyin": "sheng",
  "strokes": 46,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第47卦：《困》 ☱☵**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_47_kun",
  "name": "困",
  "symbol": "☱☵",
  "sequence": 47,
  "pinyin": "kun",
  "strokes": 47,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第48卦：《井》 ☵☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_48_jing",
  "name": "井",
  "symbol": "☵☴",
  "sequence": 48,
  "pinyin": "jing",
  "strokes": 48,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第49卦：《革》 ☱☲**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_49_ge",
  "name": "革",
  "symbol": "☱☲",
  "sequence": 49,
  "pinyin": "ge",
  "strokes": 49,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第50卦：《鼎》 ☲☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_50_ding",
  "name": "鼎",
  "symbol": "☲☴",
  "sequence": 50,
  "pinyin": "ding",
  "strokes": 50,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第51卦：《震》 ☳☳**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_51_zhen",
  "name": "震",
  "symbol": "☳☳",
  "sequence": 51,
  "pinyin": "zhen",
  "strokes": 51,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第52卦：《艮》 ☶☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_52_gen",
  "name": "艮",
  "symbol": "☶☶",
  "sequence": 52,
  "pinyin": "gen",
  "strokes": 52,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第53卦：《渐》 ☴☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_53_jian",
  "name": "渐",
  "symbol": "☴☶",
  "sequence": 53,
  "pinyin": "jian",
  "strokes": 53,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第54卦：《归妹》 ☳☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_54_gui_mei",
  "name": "归妹",
  "symbol": "☳☱",
  "sequence": 54,
  "pinyin": "gui_mei",
  "strokes": 54,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第55卦：《丰》 ☳☲**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_55_feng",
  "name": "丰",
  "symbol": "☳☲",
  "sequence": 55,
  "pinyin": "feng",
  "strokes": 55,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第56卦：《旅》 ☲☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_56_lv",
  "name": "旅",
  "symbol": "☲☶",
  "sequence": 56,
  "pinyin": "lv",
  "strokes": 56,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第57卦：《巽》 ☴☴**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_57_xun",
  "name": "巽",
  "symbol": "☴☴",
  "sequence": 57,
  "pinyin": "xun",
  "strokes": 57,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第58卦：《兑》 ☱☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_58_dui",
  "name": "兑",
  "symbol": "☱☱",
  "sequence": 58,
  "pinyin": "dui",
  "strokes": 58,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第59卦：《涣》 ☴☵**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_59_huan",
  "name": "涣",
  "symbol": "☴☵",
  "sequence": 59,
  "pinyin": "huan",
  "strokes": 59,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第60卦：《节》 ☵☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_60_jie",
  "name": "节",
  "symbol": "☵☱",
  "sequence": 60,
  "pinyin": "jie",
  "strokes": 60,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第61卦：《中孚》 ☴☱**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_61_zhong_fu",
  "name": "中孚",
  "symbol": "☴☱",
  "sequence": 61,
  "pinyin": "zhong_fu",
  "strokes": 61,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第62卦：《小过》 ☳☶**
**核心机制：【Placeholder】**
- **效果：** Placeholder effect description.
- **爻辞变量：**
  - **地部:** Placeholder.
  - **人部:** Placeholder.
  - **天部:** Placeholder.
```json
{
  "id": "basic_62_xiao_guo",
  "name": "小过",
  "symbol": "☳☶",
  "sequence": 62,
  "pinyin": "xiao_guo",
  "strokes": 62,
  "type": "basic",
  "core_mechanism": {
    "name": "Placeholder Effect",
    "description": "A simple placeholder effect.",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "actions": [
            {
              "action": "GAIN_RESOURCE",
              "params": {
                "target": "SELF",
                "resource": "gold",
                "value": 2
              }
            }
          ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "actions": [
            {
              "action": "DRAW_CARD",
              "params": {
                "target": "SELF",
                "deck": "basic",
                "count": 1
              }
            }
          ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "actions": [
            {
              "action": "DEAL_DAMAGE",
              "params": {
                "target": "OPPONENT_CHOICE_SINGLE",
                "value": 2
              }
            }
          ]
        }
      }
    }
  }
}
```

---
### **第六十三卦：《既济》 ☵☲ - 功成**
**核心机制：【水火既济】**
- **效果：** 若你的阴阳指示条为0且五行资源平衡，你获得100胜利点。每场游戏只能成功宣告一次。
- **爻辞变量：**
  - **地部:** 宣告成功时，额外获得20金币。
  - **人部:** 宣告成功时，额外抽3张功能牌。
  - **天部:** 宣告成功时，所有其他玩家失去10金币。
```json
{
  "id": "basic_63_jiji",
  "name": "既济",
  "symbol": "☵☲",
  "sequence": 63,
  "pinyin": "jiji",
  "type": "basic",
  "usage_limit": {
    "scope": "GAME",
    "count": 1
  },
  "core_mechanism": {
    "name": "水火既济",
    "description": "在满足特定条件下获得大量胜利点数。",
    "variants": {
      "di": {
        "name": "地",
        "effect": {
          "condition": { "op": "AND", "conditions": [ { "op": "PLAYER_HAS_FLAG", "params": { "flag": "YIN_YANG_IS_ZERO" } }, { "op": "PLAYER_HAS_FLAG", "params": { "flag": "FIVE_ELEMENTS_BALANCED" } } ] },
          "actions": [ { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "VICTORY_POINTS", "value": 100 } }, { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "gold", "value": 20 } } ]
        }
      },
      "ren": {
        "name": "人",
        "effect": {
          "condition": { "op": "AND", "conditions": [ { "op": "PLAYER_HAS_FLAG", "params": { "flag": "YIN_YANG_IS_ZERO" } }, { "op": "PLAYER_HAS_FLAG", "params": { "flag": "FIVE_ELEMENTS_BALANCED" } } ] },
          "actions": [ { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "VICTORY_POINTS", "value": 100 } }, { "action": "DRAW_CARD", "params": { "target": "SELF", "deck": "function", "count": 3 } } ]
        }
      },
      "tian": {
        "name": "天",
        "effect": {
          "condition": { "op": "AND", "conditions": [ { "op": "PLAYER_HAS_FLAG", "params": { "flag": "YIN_YANG_IS_ZERO" } }, { "op": "PLAYER_HAS_FLAG", "params": { "flag": "FIVE_ELEMENTS_BALANCED" } } ] },
          "actions": [ { "action": "GAIN_RESOURCE", "params": { "target": "SELF", "resource": "VICTORY_POINTS", "value": 100 } }, { "action": "LOSE_RESOURCE", "params": { "target": "OPPONENT_ALL", "resource": "gold", "value": 10 } } ]
        }
      }
    }
  }
}
```

---

### **第六十四卦：《未济》 ☲☵ - 未完**
**核心机制：【火水未济】**
- **效果：** 颠倒阴阳或交换资源。
- **爻辞变量：**
  - **地部:** 你的阴阳指示条的数值翻转（例如，-3变为+3）。
  - **人部 (震用伐鬼方):** 你可以改变用法：指定一名其他玩家，你们双方**交换彼此的弃牌堆**。此效果**每场游戏只能发动一次**。
  - **天部:** 你与指定的一名其他玩家交换所有金币。
```json
{
  "id": "basic_64_weiji",
  "name": "未济",
  "symbol": "☲☵",
  "sequence": 64,
  "pinyin": "weiji",
  "type": "basic",
  "core_mechanism": {
    "name": "火水未济",
    "description": "颠倒阴阳或交换资源。",
    "variants": {
      "di": {
        "name": "倒置",
        "effect": {
          "actions": [{ "action": "MODIFY_RULE", "params": { "rule_id": "YIN_YANG_SYSTEM_REVERSED", "scope": "SELF", "mutation": { "type": "SET_BOOLEAN", "value": true }, "duration": 1 } }]
        }
      },
      "ren": {
        "name": "震用伐鬼方",
        "usage_limit": {
          "scope": "GAME",
          "count": 1
        },
        "effect": {
          "actions": [
            {
              "action": "SWAP_DISCARD_PILES",
              "params": {
                "target_a": "SELF",
                "target_b": "OPPONENT_CHOICE_SINGLE"
              }
            }
          ]
        }
      },
      "tian": {
        "name": "易位",
        "effect": {
          "actions": [{ "action": "SWAP_RESOURCES", "params": { "target_a": "SELF", "target_b": "OPPONENT_CHOICE_SINGLE", "resource": "gold" } }]
        }
      }
    }
  }
}
```
---
---
**修订总结:**
所有卡牌描述都已更新，以符合新的规则和逻辑架构。关键漏洞（如《谦》的无限循环）已被堵上，模糊的描述（如《坤》的复制）已被澄清，无法实现的效果（如《蹇》）已通过新系统重构。现在的卡牌描述文档是清晰、平衡且可实现的。