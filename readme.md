



    # 《天机变》- 游戏资产 (Assets) 使用说明

版本: 1.0
日期: 2025-09-26

## 1. 简介

欢迎来到《天机变》的游戏资产库。本文件夹 (`/assets`) 包含了构建游戏所需的所有数据、图像和其他资源。

本文档旨在为所有开发者提供一个清晰的指引，说明资产的组织结构、命名规范以及如何在游戏引擎中正确地加载和使用它们。请在开始开发前仔细阅读本文档。

**核心设计哲学：数据驱动 (Data-Driven Design)**

本项目遵循严格的数据与视图分离原则。所有游戏逻辑（如卡牌效果、属性）都存储在纯文本的 `.json` 文件中，而所有视觉表现（如卡牌美术）都存储在 `.png` 文件中。**JSON文件是游戏逻辑的“单一事实来源 (Single Source of Truth)”**。

---

## 2. 文件夹结构

所有资产都位于 `assets` 文件夹下，其结构如下：
  
```

assets/
├── data/                      # 存放所有游戏逻辑数据 (JSON文件)
│   └── cards/
│       ├── basic/             # 64张基础牌
│       ├── destiny/           # 12张天命牌
│       ├── function/          # 5种功能牌
│       ├── natal/             # 8张本命卦牌
│       └── state/             # 游戏状态牌
│           ├── branches/      # 12张地支牌
│           ├── celestial/     # 7张星象牌
│           └── stems/         # 10张天干牌
│
└── images/                    # 存放所有视觉资源 (PNG文件)
└── cards/
├── backs/             # 各种牌背
├── basic/             # 基础牌美术
├── destiny/           # 天命牌美术
├── function/          # 功能牌美术
├── natal/             # 本命卦牌美术
├── state/             # 游戏状态牌美术
│   ├── branches/
│   ├── celestial/
│   └── stems/
└── ui_elements/       # UI元素，如卡牌模板





```
    **关键规则：镜像结构**

请注意，`data/cards/` 和 `images/cards/` 文件夹的**内部结构是完全一致的**。这种设计是为了简化资源加载。程序可以通过替换路径中的 `data` 为 `images`，轻易地找到任何数据文件所对应的图像文件。

---

## 3. 核心概念与命名规范

### 3.1 卡牌ID (Card ID)

游戏中的每一张卡牌都有一个**全局唯一的ID**，这是它在代码中的“身份证”。ID遵循 `[type]_[identifier]` 的格式。

*   **文件命名:** 所有与卡牌相关的文件（`.json` 和 `.png`）都必须以其卡牌ID命名。
    *   **示例:** `basic_01_qian.json`, `basic_01_qian.png`

*   **命名范式:**
    *   **基础牌:** `basic_[01-64]_[pinyin]`
    *   **功能牌:** `function_[pinyin]`
    *   **本命卦牌:** `natal_[pinyin]`
    *   **天命牌:** `destiny_[pinyin]`
    *   **天干牌:** `stem_[pinyin]`
    *   **地支牌:** `branch_[pinyin]`
    *   **星象牌:** `celestial_[pinyin]`

### 3.2 数据文件 (`.json`)

`.json` 文件定义了卡牌的一切**逻辑行为**。修改这些文件会直接改变游戏玩法。

*   **编码:** 所有 `.json` 文件必须使用 `UTF-8` 编码。
*   **结构:** 每种类型的卡牌都有其固定的JSON结构。请参考下面的“资产详情”部分。

### 3.3 图像文件 (`.png`)

`.png` 文件定义了卡牌的**视觉外观**。

*   **尺寸:** 当前占位图尺寸为 `500x700` 像素。最终美术资源应保持统一尺寸。
*   **替换规则:** 你可以随时替换任何一张 `.png` 图片以更新美术，**但文件名必须与对应的 `.json` 文件保持严格一致**。

---

## 4. 如何使用资产（编程指南）

### 4.1 加载一张卡牌

在游戏中加载并创建一张卡牌的推荐流程如下：

```javascript
// 伪代码示例
function loadCard(cardId) {
    // 1. 从ID中解析出类型和文件名
    const type = cardId.split('_'); // "basic"
    const filename = cardId;          // "basic_01_qian"

    // 2. 根据类型和文件名推导出数据和图像的路径
    // 注意: state类的牌有额外的子文件夹
    let subfolder = (type === 'stem' || type === 'branch' || type === 'celestial') ? getSubfolder(type) : '';
    const dataPath = `assets/data/cards/${type}/${subfolder}${filename}.json`;
    const imagePath = `assets/images/cards/${type}/${subfolder}${filename}.png`;

    // 3. 加载资源
    const cardData = loadJsonFile(dataPath);
    const cardImage = loadImageFile(imagePath);
    
    // 4. 在游戏中创建卡牌对象
    const cardObject = new Card(cardData, cardImage);
    return cardObject;
}

// 使用示例
let qianCard = loadCard("basic_01_qian");
  
```

### 4.2 构建牌库

要构建一个完整的牌库（例如，基础牌库），程序应该：

1. 读取 assets/data/cards/basic/ 目录下的所有文件名。
2. 从文件名中提取出卡牌ID（去除.json后缀）。
3. 对于每一个ID，调用 loadCard(id) 函数来创建卡牌对象。
4. 将所有创建的卡牌对象存入一个列表或数组中，然后进行洗牌。

------



## 5. 资产详情 (JSON Schema)

#### basic_[id].json





```
    {
  "id": "string",          // 唯一ID
  "name": "string",        // 中文名 (乾)
  "symbol": "string",      // 卦象符号 (☰)
  "sequence": "integer",   // 序卦传顺序 (1-64)
  "strokes": "integer",    // 总笔画数 (用于'论道'事件)
  "link": { ... },         // 对卦/综卦联动信息
  "effects": {
    "tian": "string",      // 天部效果描述
    "ren": "string",       // 人部效果描述
    "di": "string"        // 地部效果描述
  }
}
  
```

#### function_[id].json





```
    {
  "id": "string",
  "type": "function",
  "name": "string",        // 中文名 (错卦)
  "description": "string"  // 效果描述
}
  
```

#### natal_[id].json





```
    {
  "id": "string",
  "type": "natal",
  "name": "string",
  "symbol": "string",
  "passive": {
    "name": "string",
    "description": "string"
  },
  "active": {
    "name": "string",
    "description": "string"
  }
}
  
```

*(其他卡牌类型的JSON结构类似，都包含id, type, name等关键字段。)*

------

