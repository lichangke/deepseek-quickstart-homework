# 五子棋游戏 HTML 实现

以下是一个完整的五子棋游戏 HTML 实现，包含所有代码在一个文件中：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>五子棋游戏</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #f5f5dc;
            margin: 0;
            padding: 20px;
        }
        
        h1 {
            color: #8b4513;
            margin-bottom: 10px;
        }
        
        .game-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 20px;
        }
        
        .board {
            display: grid;
            grid-template-columns: repeat(15, 30px);
            grid-template-rows: repeat(15, 30px);
            background-color: #deb887;
            border: 2px solid #8b4513;
            position: relative;
        }
        
        .cell {
            width: 30px;
            height: 30px;
            box-sizing: border-box;
            position: relative;
            cursor: pointer;
        }
        
        .cell::before, .cell::after {
            content: '';
            position: absolute;
            background-color: #000;
        }
        
        .cell::before {
            width: 100%;
            height: 1px;
            top: 50%;
            left: 0;
            transform: translateY(-50%);
        }
        
        .cell::after {
            width: 1px;
            height: 100%;
            left: 50%;
            top: 0;
            transform: translateX(-50%);
        }
        
        .piece {
            position: absolute;
            width: 26px;
            height: 26px;
            border-radius: 50%;
            top: 2px;
            left: 2px;
            z-index: 1;
        }
        
        .black {
            background: radial-gradient(circle at 30% 30%, #666, #000);
            box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }
        
        .white {
            background: radial-gradient(circle at 30% 30%, #fff, #ccc);
            box-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
        }
        
        .controls {
            margin-top: 20px;
            display: flex;
            gap: 15px;
        }
        
        button {
            padding: 8px 15px;
            background-color: #8b4513;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        
        button:hover {
            background-color: #a0522d;
        }
        
        .status {
            margin-top: 15px;
            font-size: 18px;
            color: #8b4513;
            font-weight: bold;
            height: 24px;
        }
        
        .star-point {
            position: absolute;
            width: 6px;
            height: 6px;
            background-color: #000;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }
    </style>
</head>
<body>
    <h1>五子棋游戏</h1>
    <div class="game-container">
        <div class="status" id="status">黑方回合</div>
        <div class="board" id="board"></div>
        <div class="controls">
            <button id="restart">重新开始</button>
            <button id="undo">悔棋</button>
        </div>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const boardSize = 15;
            const board = document.getElementById('board');
            const statusDisplay = document.getElementById('status');
            const restartButton = document.getElementById('restart');
            const undoButton = document.getElementById('undo');
            
            let gameState = Array(boardSize).fill().map(() => Array(boardSize).fill(null));
            let currentPlayer = 'black';
            let gameHistory = [];
            let gameOver = false;
            
            // 初始化棋盘
            function initializeBoard() {
                board.innerHTML = '';
                
                // 创建棋盘格子
                for (let row = 0; row < boardSize; row++) {
                    for (let col = 0; col < boardSize; col++) {
                        const cell = document.createElement('div');
                        cell.className = 'cell';
                        cell.dataset.row = row;
                        cell.dataset.col = col;
                        cell.addEventListener('click', () => handleCellClick(row, col));
                        board.appendChild(cell);
                    }
                }
                
                // 添加星位点
                const starPoints = [
                    [3, 3], [3, 11], [3, 7],
                    [7, 3], [7, 11], [7, 7],
                    [11, 3], [11, 11], [11, 7]
                ];
                
                starPoints.forEach(([row, col]) => {
                    const starPoint = document.createElement('div');
                    starPoint.className = 'star-point';
                    starPoint.style.left = `${col * 30 + 15}px`;
                    starPoint.style.top = `${row * 30 + 15}px`;
                    board.appendChild(starPoint);
                });
            }
            
            // 处理点击格子
            function handleCellClick(row, col) {
                if (gameOver || gameState[row][col] !== null) return;
                
                // 保存当前状态到历史记录
                gameHistory.push({
                    state: JSON.parse(JSON.stringify(gameState)),
                    player: currentPlayer
                });
                
                // 更新游戏状态
                gameState[row][col] = currentPlayer;
                
                // 在棋盘上放置棋子
                placePiece(row, col, currentPlayer);
                
                // 检查胜利条件
                if (checkWin(row, col)) {
                    const winner = currentPlayer === 'black' ? '黑方' : '白方';
                    statusDisplay.textContent = `${winner}获胜！`;
                    gameOver = true;
                    return;
                }
                
                // 切换玩家
                currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
                statusDisplay.textContent = `${currentPlayer === 'black' ? '黑方' : '白方'}回合`;
            }
            
            // 在棋盘上放置棋子
            function placePiece(row, col, player) {
                const piece = document.createElement('div');
                piece.className = `piece ${player}`;
                piece.style.top = `${row * 30 + 2}px`;
                piece.style.left = `${col * 30 + 2}px`;
                board.appendChild(piece);
            }
            
            // 检查胜利条件
            function checkWin(row, col) {
                const directions = [
                    [0, 1],   // 水平
                    [1, 0],    // 垂直
                    [1, 1],    // 对角线
                    [1, -1]    // 反对角线
                ];
                
                for (const [dx, dy] of directions) {
                    let count = 1;
                    
                    // 正向检查
                    for (let i = 1; i < 5; i++) {
                        const newRow = row + i * dx;
                        const newCol = col + i * dy;
                        
                        if (
                            newRow < 0 || newRow >= boardSize ||
                            newCol < 0 || newCol >= boardSize ||
                            gameState[newRow][newCol] !== currentPlayer
                        ) {
                            break;
                        }
                        count++;
                    }
                    
                    // 反向检查
                    for (let i = 1; i < 5; i++) {
                        const newRow = row - i * dx;
                        const newCol = col - i * dy;
                        
                        if (
                            newRow < 0 || newRow >= boardSize ||
                            newCol < 0 || newCol >= boardSize ||
                            gameState[newRow][newCol] !== currentPlayer
                        ) {
                            break;
                        }
                        count++;
                    }
                    
                    if (count >= 5) return true;
                }
                
                return false;
            }
            
            // 重新开始游戏
            function restartGame() {
                gameState = Array(boardSize).fill().map(() => Array(boardSize).fill(null));
                currentPlayer = 'black';
                gameHistory = [];
                gameOver = false;
                statusDisplay.textContent = '黑方回合';
                initializeBoard();
            }
            
            // 悔棋
            function undoMove() {
                if (gameHistory.length === 0 || gameOver) return;
                
                const lastMove = gameHistory.pop();
                gameState = lastMove.state;
                currentPlayer = lastMove.player;
                gameOver = false;
                statusDisplay.textContent = `${currentPlayer === 'black' ? '黑方' : '白方'}回合`;
                
                // 重新渲染棋盘
                board.querySelectorAll('.piece').forEach(piece => piece.remove());
                for (let row = 0; row < boardSize; row++) {
                    for (let col = 0; col < boardSize; col++) {
                        if (gameState[row][col] !== null) {
                            placePiece(row, col, gameState[row][col]);
                        }
                    }
                }
            }
            
            // 事件监听
            restartButton.addEventListener('click', restartGame);
            undoButton.addEventListener('click', undoMove);
            
            // 初始化游戏
            initializeBoard();
        });
    </script>
</body>
</html>
```

## 游戏功能说明

1. **基本规则**：
   - 标准15×15五子棋棋盘
   - 黑方先行，轮流落子
   - 先形成五子连线者获胜

2. **界面功能**：
   - 清晰的棋盘和棋子显示
   - 显示当前回合玩家
   - 重新开始按钮
   - 悔棋按钮

3. **技术实现**：
   - 使用纯HTML/CSS/JavaScript实现
   - 响应式设计
   - 使用CSS Grid布局棋盘
   - 使用二维数组跟踪游戏状态

您可以将此代码保存为单个HTML文件，然后在浏览器中打开即可开始游戏。