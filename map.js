// map.js

/**
 * This module is responsible for generating and providing the game map data,
 * including zone definitions and adjacencies. It is the single source of truth for the board layout.
 */

// This is the raw data originally from game_map.html
const rawMapData = {
    center: { x: 400, y: 400 },
    palaces: [
        { id: 'Li',   name: '离', symbol: '☲', luoshu: 9, element: 'fire',  angle: -22.5, direction: '正南', imagery: '火, 光明, 附丽' },
        { id: 'Kun',  name: '坤', symbol: '☷', luoshu: 2, element: 'earth', angle: 22.5,  direction: '西南', imagery: '地, 柔顺, 承载' },
        { id: 'Dui',  name: '兑', symbol: '☱', luoshu: 7, element: 'metal', angle: 67.5,  direction: '正西', imagery: '泽, 喜悦, 言说' },
        { id: 'Qian', name: '乾', symbol: '☰', luoshu: 6, element: 'metal', angle: 112.5, direction: '西北', imagery: '天, 刚健, 创造' },
        { id: 'Kan',  name: '坎', symbol: '☵', luoshu: 1, element: 'water', angle: 157.5, direction: '正北', imagery: '水, 险陷, 智慧' },
        { id: 'Gen',  name: '艮', symbol: '☶', luoshu: 8, element: 'earth', angle: 202.5, direction: '东北', imagery: '山, 静止, 笃实' },
        { id: 'Zhen', name: '震', symbol: '☳', luoshu: 3, element: 'wood',  angle: 247.5, direction: '正东', imagery: '雷, 奋起, 行动' },
        { id: 'Xun',  name: '巽', symbol: '☴', luoshu: 4, element: 'wood',  angle: 292.5, direction: '东南', imagery: '风, 顺入, 命令' }
    ],
    departments: [
        { id: 'Tian', name: '天', innerRadius: 120, outerRadius: 200 },
        { id: 'Ren',  name: '人', innerRadius: 200, outerRadius: 300 },
        { id: 'Di',   name: '地', innerRadius: 300, outerRadius: 400 }
    ],
    zones: {}
};

/**
 * Creates the basic structure for all zones.
 */
function generateZoneShells(data) {
    data.palaces.forEach(palace => {
        data.departments.forEach(dept => {
            const zoneId = `Gong_${palace.id}-Bu_${dept.id}`;
            data.zones[zoneId] = {
                description: `${palace.name}宫之${dept.name}部`,
                adjacencies: []
            };
        });
    });
    data.zones['Gong_Zhong'] = {
        description: '中宫/太极部',
        adjacencies: [], // Adjacency is governed by specialRules
        specialRules: [
            'Player must exit upon next move.',
            'Target of exit is the unoccupied Earth-Dept zone with the lowest Luoshu number.',
            'Player suffers 10% gold penalty upon entry.'
        ]
    };
}

/**
 * Dynamically generates the adjacency list for every zone based on game rules.
 */
function generateAdjacencies(data) {
    const palaceIds = data.palaces.map(p => p.id);
    const numPalaces = palaceIds.length;

    for (const zoneId in data.zones) {
        if (zoneId === 'Gong_Zhong') continue;

        const [gong, bu] = zoneId.split('-');
        const palaceId = gong.split('_')[1];
        const deptId = bu.split('_')[1];
        const adj = data.zones[zoneId].adjacencies;

        const currentPalaceIndex = palaceIds.indexOf(palaceId);

        if (deptId === 'Tian') {
            adj.push(`Gong_${palaceId}-Bu_Ren`);
            adj.push('Gong_Zhong');
        } else if (deptId === 'Ren') {
            adj.push(`Gong_${palaceId}-Bu_Tian`);
            adj.push(`Gong_${palaceId}-Bu_Di`);
        } else if (deptId === 'Di') {
            adj.push(`Gong_${palaceId}-Bu_Ren`);
            const prevPalaceId = palaceIds[(currentPalaceIndex + numPalaces - 1) % numPalaces];
            const nextPalaceId = palaceIds[(currentPalaceIndex + 1) % numPalaces];
            adj.push(`Gong_${prevPalaceId}-Bu_Di`);
            adj.push(`Gong_${nextPalaceId}-Bu_Di`);
        }
    }
}

/**
 * Generates the complete map data object.
 * @returns {object} The fully processed map data.
 */
export function getMapData() {
    // Use a deep copy to avoid modifying the raw data on subsequent calls
    const data = JSON.parse(JSON.stringify(rawMapData));
    generateZoneShells(data);
    generateAdjacencies(data);
    return data;
}