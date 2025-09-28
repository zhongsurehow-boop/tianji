// game.js - Core Game Engine for 天机变

import { getMapData } from './map.js';

// =================================================================
// 1. GLOBAL STATE & LIBRARIES
// =================================================================

const cardLibrary = {}; // Will hold all card data, keyed by cardId
const mapData = getMapData(); // Get the fully generated map data
let gameState = {}; // The single source of truth for the game's state

// =================================================================
// 2. INITIALIZATION
// =================================================================

export async function initGame() {
    console.log("Game Engine Initializing...");
    logMessage("正在加载游戏资源...");

    try {
        await loadCardData();
        logMessage(`成功加载 ${Object.keys(cardLibrary).length} 张基础卡牌。`);
        logMessage(`地图数据已加载，共 ${Object.keys(mapData.zones).length} 个区域。`);

        setupNewGame();
        addMapClickListeners();
        logMessage("游戏设置完成，棋局开始。");

        render(gameState);
        setPhase('MOVEMENT'); // Start the first phase

    } catch (error) {
        console.error("Failed to initialize game:", error);
        logMessage(`游戏初始化失败: ${error.message}`);
    }
}

async function loadCardData() {
    const manifestResponse = await fetch('assets/data/card_manifest.json');
    if (!manifestResponse.ok) throw new Error("Could not load card_manifest.json");
    const manifest = await manifestResponse.json();

    const cardIds = manifest.basic_cards;
    const cardPromises = cardIds.map(id =>
        fetch(`assets/data/cards/basic/${id}.json`).then(res => res.ok ? res.json() : Promise.reject(new Error(id)))
    );

    const cards = await Promise.all(cardPromises);
    cards.forEach(cardData => { cardLibrary[cardData.id] = cardData; });
}

function setupNewGame() {
    gameState = {
        players: [
            { id: 1, name: "玩家一", location: "Gong_Qian-Bu_Di", color: "#e74c3c", gold: 100, health: 20, hand: [] },
            { id: 2, name: "玩家二", location: "Gong_Kun-Bu_Di", color: "#3498db", gold: 100, health: 20, hand: [] }
        ],
        decks: { basic: shuffle(Object.keys(cardLibrary)) },
        discardPiles: { basic: [] },
        gamePhase: "INIT",
        activePlayerId: 1,
        turn: 1,
        actionLog: []
    };
    // Deal initial hands
    dealCardToPlayer(1, 5);
    dealCardToPlayer(2, 5);
}

function addMapClickListeners() {
    const svg = document.getElementById('game-board');
    if (!svg) return;
    svg.querySelectorAll('.zone, #Gong_Zhong').forEach(zone => {
        zone.addEventListener('click', (event) => handleZoneClick(event.currentTarget.id));
    });
}

// =================================================================
// 3. GAME LOOP & PHASE MANAGEMENT
// =================================================================

const PHASES = ['TIME', 'PLACEMENT', 'MOVEMENT', 'INTERPRETATION', 'RESOLUTION', 'UPKEEP'];

function setPhase(newPhase) {
    gameState.gamePhase = newPhase;
    logMessage(`进入 [${newPhase}] 阶段。`);

    switch (newPhase) {
        case 'MOVEMENT':
            logMessage(`轮到玩家 ${gameState.activePlayerId} 行动。请在地图上点击一个相邻区域进行移动。`);
            break;
        case 'UPKEEP':
            endTurn();
            break;
    }
    render(gameState);
}

function endTurn() {
    gameState.activePlayerId = gameState.activePlayerId === 1 ? 2 : 1;
    if (gameState.activePlayerId === 1) {
        gameState.turn++;
        logMessage(`第 ${gameState.turn} 轮开始。`);
    }
    setPhase('MOVEMENT');
}

// =================================================================
// 4. CORE LOGIC & PLAYER ACTIONS
// =================================================================

function dealCardToPlayer(playerId, count) {
    const player = gameState.players.find(p => p.id === playerId);
    if (!player) return;

    for (let i = 0; i < count; i++) {
        if (gameState.decks.basic.length > 0) {
            const cardId = gameState.decks.basic.pop();
            player.hand.push(cardId);
        } else {
            logMessage("[警告] 基础牌库已空，无法抽牌。");
            // TODO: Implement reshuffling discard pile
            break;
        }
    }
    logMessage(`向玩家 ${playerId} 发了 ${count} 张牌。`);
}

function handleZoneClick(zoneId) {
    if (gameState.gamePhase !== 'MOVEMENT') {
        logMessage("提示: 当前不是移动阶段。");
        return;
    }

    const player = gameState.players.find(p => p.id === gameState.activePlayerId);
    const currentZone = mapData.zones[player.location];

    if (currentZone.adjacencies.includes(zoneId)) {
        logMessage(`玩家 ${player.id} 选择了有效移动: ${zoneId}`);
        const moveAction = {
            action: "MOVE",
            params: { target: `PLAYER_${player.id}`, destination: zoneId }
        };
        executeAction(moveAction, player.id);
        render(gameState);
        setPhase('UPKEEP');
    } else {
        logMessage(`[无效移动] 从 ${player.location} 无法直接移动到 ${zoneId}。`);
    }
}

function executeAction(action, sourcePlayerId) {
    const { params } = action;
    const player = gameState.players.find(p => p.id === sourcePlayerId);

    logMessage(`执行动作: ${action.action} (玩家 ${sourcePlayerId})`);

    switch (action.action) {
        case 'MOVE':
            player.location = params.destination;
            logMessage(`玩家 ${sourcePlayerId} 移动到了 ${mapData.zones[params.destination].description}`);
            break;
        case 'GAIN_RESOURCE':
            if (params.resource === 'gold') player.gold += params.value;
            if (params.resource === 'health') player.health += params.value;
            logMessage(`玩家 ${sourcePlayerId} 获得了 ${params.value} ${params.resource}。`);
            break;
        default:
            logMessage(`[警告] 未知的动作类型: ${action.action}`);
    }
}

// =================================================================
// 5. UI & RENDERER
// =================================================================

function render(state) {
    state.players.forEach(player => {
        const zoneDesc = mapData.zones[player.location]?.description || '场外';
        document.getElementById(`p${player.id}-location`).textContent = zoneDesc;
        document.getElementById(`p${player.id}-gold`).textContent = player.gold;
        document.getElementById(`p${player.id}-health`).textContent = player.health;
        renderPlayerHand(player);
    });

    document.getElementById('current-phase').textContent = state.gamePhase;
    renderPlayerPawns(state.players);
}

function renderPlayerHand(player) {
    const handContainer = document.getElementById(`p${player.id}-hand`);
    if (!handContainer) return;
    handContainer.innerHTML = ''; // Clear existing cards

    player.hand.forEach(cardId => {
        const card = cardLibrary[cardId];
        const cardElement = document.createElement('div');
        cardElement.className = 'card';
        cardElement.textContent = card.name;
        cardElement.title = card.id; // Show ID on hover
        handContainer.appendChild(cardElement);
    });
}

function renderPlayerPawns(players) {
    let pawnsGroup = document.getElementById('player-pawns');
    if (!pawnsGroup) {
        pawnsGroup = document.createElementNS("http://www.w3.org/2000/svg", 'g');
        pawnsGroup.id = 'player-pawns';
        document.getElementById('game-board').appendChild(pawnsGroup);
    }
    pawnsGroup.innerHTML = '';

    players.forEach(player => {
        const zoneElement = document.getElementById(player.location);
        if (zoneElement) {
            const bbox = zoneElement.getBBox();
            const cx = bbox.x + bbox.width / 2;
            const cy = bbox.y + bbox.height / 2;
            const pawn = document.createElementNS("http://www.w3.org/2000/svg", 'circle');
            pawn.setAttribute('cx', cx + (player.id === 1 ? -8 : 8));
            pawn.setAttribute('cy', cy);
            pawn.setAttribute('r', 12);
            pawn.setAttribute('fill', player.color);
            pawn.setAttribute('stroke', 'white');
            pawn.setAttribute('stroke-width', 2);
            pawn.style.pointerEvents = 'none';
            pawnsGroup.appendChild(pawn);
        }
    });
}

function logMessage(message) {
    const logContainer = document.getElementById('game-log');
    if (!logContainer) return;
    const p = document.createElement('p');
    const timestamp = new Date().toLocaleTimeString('en-GB');
    p.innerHTML = `<span style="color: #888;">[${timestamp}]</span> ${message}`;
    logContainer.appendChild(p);
    logContainer.scrollTop = logContainer.scrollHeight;
}

// =================================================================
// 6. UTILITIES
// =================================================================

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}