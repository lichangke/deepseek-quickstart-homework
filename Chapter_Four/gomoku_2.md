# 中国风五子棋游戏

以下是一个完整的HTML五子棋游戏，左侧背景采用中国风设计，所有代码都在一个HTML文件中：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>中国风五子棋</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'SimSun', '宋体', serif;
            background-color: #f8f3e6;
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        .chinese-bg {
            width: 30%;
            height: 100%;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%" viewBox="0 0 800 1000"><rect width="100%" height="100%" fill="%23f8f3e6"/><path d="M50,100 Q150,50 250,100 T450,100 T650,100" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M100,200 Q200,150 300,200 T500,200 T700,200" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M150,300 Q250,250 350,300 T550,300 T750,300" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M50,400 Q150,350 250,400 T450,400 T650,400" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M100,500 Q200,450 300,500 T500,500 T700,500" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M150,600 Q250,550 350,600 T550,600 T750,600" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M50,700 Q150,650 250,700 T450,700 T650,700" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M100,800 Q200,750 300,800 T500,800 T700,800" stroke="%23d4a76a" stroke-width="2" fill="none"/><path d="M150,900 Q250,850 350,900 T550,900 T750,900" stroke="%23d4a76a" stroke-width="2" fill="none"/><text x="50%" y="100" font-family="SimSun" font-size="48" fill="%23a67c52" text-anchor="middle">五子棋</text><text x="50%" y="180" font-family="SimSun" font-size="24" fill="%23a67c52" text-anchor="middle">黑白对弈</text><text x="50%" y="220" font-family="SimSun" font-size="24" fill="%23a67c52" text-anchor="middle">千古智慧</text></svg>');
            background-size: cover;
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            box-shadow: 5px 0 15px rgba(0, 0, 0, 0.1);
        }

        .game-container {
            width: 70%;
            height: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: #fff9e6;
        }

        .game-title {
            font-size: 36px;
            color: #8c4a2f;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
        }

        .game-board {
            width: 500px;
            height: 500px;
            background-color: #e6c88c;
            position: relative;
            border: 2px solid #8c4a2f;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
        }

        .grid-line {
            position: absolute;
            background-color: #5a3921;
        }

        .horizontal-line {
            width: 100%;
            height: 1px;
            left: 0;
        }

        .vertical-line {
            width: 1px;
            height: 100%;
            top: 0;
        }

        .star-point {
            position: absolute;
            width: 10px;
            height: 10px;
            background-color: #5a3921;
            border-radius: 50%;
            transform: translate(-50%, -50%);
        }

        .piece {
            position: absolute;
            width: 28px;
            height: 28px;
            border-radius: 50%;
            transform: translate(-50%, -50%);
            box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.3);
        }

        .black {
            background: radial-gradient(circle at 30% 30%, #666, #000);
        }

        .white {
            background: radial-gradient(circle at 30% 30%, #fff, #ccc);
        }

        .game-info {
            margin-top: 20px;
            font-size: 20px;
            color: #8c4a2f;
        }

        .restart-btn {
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #8c4a2f;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 16px;
            cursor: pointer;
            font-family: 'SimSun', '宋体', serif;
            transition: all 0.3s;
        }

        .restart-btn:hover {
            background-color: #a67c52;
            transform: translateY(-2px);
        }

        .chinese-poem {
            position: absolute;
            bottom: 50px;
            width: 80%;
            text-align: center;
            color: #8c4a2f;
            font-size: 18px;
            line-height: 1.8;
        }
    </style>
</head>
<body>
    <div class="chinese-bg">
        <div class="chinese-poem">
            <p>棋盘方寸间，</p>
            <p>黑白两重天。</p>
            <p>一子定乾坤，</p>
            <p>胜负皆随缘。</p>
        </div>
    </div>
    <div class="game-container">
        <h1 class="game-title">中国风五子棋</h1>
        <div class="game-board" id="gameBoard"></div>
        <div class="game-info" id="gameInfo">黑方回合</div>
        <button class="restart-btn" id="restartBtn">重新开始</button>
    </div>

    <script>
        document.addEventListener('DOMContentLoaded', function() {
            const board = document.getElementById('gameBoard');
            const gameInfo = document.getElementById('gameInfo');
            const restartBtn = document.getElementById('restartBtn');
            
            const BOARD_SIZE = 15;
            const CELL_SIZE = 500 / (BOARD_SIZE - 1);
            let currentPlayer = 'black';
            let gameOver = false;
            let boardState = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(null));
            
            // 创建棋盘
            function createBoard() {
                // 清除现有棋盘
                board.innerHTML = '';
                
                // 创建横线
                for (let i = 0; i < BOARD_SIZE; i++) {
                    const horizontalLine = document.createElement('div');
                    horizontalLine.className = 'grid-line horizontal-line';
                    horizontalLine.style.top = `${i * CELL_SIZE}px`;
                    board.appendChild(horizontalLine);
                }
                
                // 创建竖线
                for (let i = 0; i < BOARD_SIZE; i++) {
                    const verticalLine = document.createElement('div');
                    verticalLine.className = 'grid-line vertical-line';
                    verticalLine.style.left = `${i * CELL_SIZE}px`;
                    board.appendChild(verticalLine);
                }
                
                // 创建星位点
                const starPoints = [
                    [3, 3], [3, 11], [7, 7], [11, 3], [11, 11]
                ];
                
                starPoints.forEach(point => {
                    const starPoint = document.createElement('div');
                    starPoint.className = 'star-point';
                    starPoint.style.left = `${point[0] * CELL_SIZE}px`;
                    starPoint.style.top = `${point[1] * CELL_SIZE}px`;
                    board.appendChild(starPoint);
                });
            }
            
            // 放置棋子
            function placePiece(x, y) {
                if (gameOver || boardState[y][x] !== null) return;
                
                const piece = document.createElement('div');
                piece.className = `piece ${currentPlayer}`;
                piece.style.left = `${x * CELL_SIZE}px`;
                piece.style.top = `${y * CELL_SIZE}px`;
                board.appendChild(piece);
                
                boardState[y][x] = currentPlayer;
                
                if (checkWin(x, y)) {
                    gameOver = true;
                    const winner = currentPlayer === 'black' ? '黑方' : '白方';
                    gameInfo.textContent = `${winner}获胜！`;
                    return;
                }
                
                currentPlayer = currentPlayer === 'black' ? 'white' : 'black';
                gameInfo.textContent = `${currentPlayer === 'black' ? '黑方' : '白方'}回合`;
            }
            
            // 检查是否获胜
            function checkWin(x, y) {
                const directions = [
                    [1, 0],   // 水平
                    [0, 1],   // 垂直
                    [1, 1],   // 对角线
                    [1, -1]   // 反对角线
                ];
                
                for (const [dx, dy] of directions) {
                    let count = 1;
                    
                    // 正向检查
                    for (let i = 1; i < 5; i++) {
                        const nx = x + i * dx;
                        const ny = y + i * dy;
                        if (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE && 
                            boardState[ny][nx] === currentPlayer) {
                            count++;
                        } else {
                            break;
                        }
                    }
                    
                    // 反向检查
                    for (let i = 1; i < 5; i++) {
                        const nx = x - i * dx;
                        const ny = y - i * dy;
                        if (nx >= 0 && nx < BOARD_SIZE && ny >= 0 && ny < BOARD_SIZE && 
                            boardState[ny][nx] === currentPlayer) {
                            count++;
                        } else {
                            break;
                        }
                    }
                    
                    if (count >= 5) return true;
                }
                
                return false;
            }
            
            // 重置游戏
            function resetGame() {
                currentPlayer = 'black';
                gameOver = false;
                boardState = Array(BOARD_SIZE).fill().map(() => Array(BOARD_SIZE).fill(null));
                gameInfo.textContent = '黑方回合';
                createBoard();
            }
            
            // 棋盘点击事件
            board.addEventListener('click', function(e) {
                const rect = board.getBoundingClientRect();
                const x = Math.round((e.clientX - rect.left) / CELL_SIZE);
                const y = Math.round((e.clientY - rect.top) / CELL_SIZE);
                
                if (x >= 0 && x < BOARD_SIZE && y >= 0 && y < BOARD_SIZE) {
                    placePiece(x, y);
                }
            });
            
            // 重新开始按钮
            restartBtn.addEventListener('click', resetGame);
            
            // 初始化游戏
            resetGame();
        });
    </script>
</body>
</html>
```

## 游戏特点

1. **中国风设计**：
   - 左侧背景采用中国风SVG图案，包含书法风格的"五子棋"标题和装饰线条
   - 添加了中国古诗，增强文化氛围
   - 整体配色采用中国传统色彩（棕色、米色等）

2. **完整五子棋功能**：
   - 15×15标准棋盘
   - 黑白双方轮流落子
   - 自动判断胜负（横、竖、斜五子连线）
   - 重新开始按钮

3. **视觉效果**：
   - 棋子有渐变和阴影效果
   - 棋盘有木质纹理感
   - 星位点标记

4. **响应式设计**：
   - 适应不同屏幕尺寸

您可以将此代码保存为单个HTML文件，然后在浏览器中打开即可开始游戏。左侧是中国风背景，右侧是五子棋游戏区域。