import pygame
import sys
import random
import time
import numpy as np
from pygame.locals import *

# 初始化pygame
pygame.init()
pygame.mixer.init()

# 游戏常量
BOARD_SIZE = 15  # 15x15的棋盘
GRID_SIZE = 40   # 每个格子的像素大小
PIECE_RADIUS = 18  # 棋子半径
MARGIN = 40      # 棋盘边距
WINDOW_WIDTH = BOARD_SIZE * GRID_SIZE + 2 * MARGIN  # 窗口宽度
WINDOW_HEIGHT = BOARD_SIZE * GRID_SIZE + 2 * MARGIN + 80  # 窗口高度（增加底部空间）
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BOARD_COLOR = (220, 179, 92)  # 棋盘颜色
HIGHLIGHT_COLOR = (255, 0, 0)  # 高亮颜色
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (200, 200, 200)
BUTTON_HOVER_COLOR = (180, 180, 180)

# 创建游戏窗口
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('五子棋')

# 加载音效
try:
    place_sound = pygame.mixer.Sound("place.wav")
    win_sound = pygame.mixer.Sound("win.wav")
except:
    print("音效文件未找到，游戏将继续但没有音效")
    place_sound = None
    win_sound = None

# 游戏状态
class GameState:
    def __init__(self):
        self.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)  # 0=空, 1=黑, 2=白
        self.current_player = 1  # 1=黑, 2=白
        self.game_over = False
        self.winner = 0  # 0=无, 1=黑, 2=白
        self.mode = "human"  # "human"或"ai"
        self.ai_difficulty = "medium"  # "easy", "medium", "hard"
        self.move_history = []  # 用于悔棋

    def reset(self):
        self.board.fill(0)
        self.current_player = 1
        self.game_over = False
        self.winner = 0
        self.move_history = []

    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != 0:
            return False
        
        self.board[row][col] = self.current_player
        self.move_history.append((row, col, self.current_player))
        
        if self.check_win(row, col):
            self.game_over = True
            self.winner = self.current_player
            if win_sound:
                win_sound.play()
        elif np.all(self.board != 0):
            self.game_over = True  # 平局
        
        self.current_player = 3 - self.current_player  # 切换玩家
        return True

    def undo_move(self):
        if not self.move_history or self.game_over:
            return False
        
        row, col, player = self.move_history.pop()
        self.board[row][col] = 0
        self.current_player = player
        self.game_over = False
        self.winner = 0
        return True

    def check_win(self, row, col):
        player = self.board[row][col]
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 水平, 垂直, 对角线
        
        for dr, dc in directions:
            count = 1  # 当前位置已经有一个棋子
            
            # 正向检查
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r += dr
                c += dc
            
            # 反向检查
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and self.board[r][c] == player:
                count += 1
                r -= dr
                c -= dc
            
            if count >= 5:
                return True
        
        return False

# AI逻辑
class AI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
    
    def make_move(self, game_state):
        if game_state.game_over:
            return None
        
        if self.difficulty == "easy":
            return self.easy_ai(game_state)
        elif self.difficulty == "medium":
            return self.medium_ai(game_state)
        else:
            return self.hard_ai(game_state)
    
    def easy_ai(self, game_state):
        # 简单AI: 随机落子+基础防守
        empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if game_state.board[i][j] == 0]
        
        # 检查是否有需要防守的四连
        for i, j in empty_positions:
            game_state.board[i][j] = 1  # 假设对手下这里
            if game_state.check_win(i, j):
                game_state.board[i][j] = 0  # 恢复
                return (i, j)
            game_state.board[i][j] = 0  # 恢复
        
        # 随机选择一个位置
        if empty_positions:
            return random.choice(empty_positions)
        return None
    
    def medium_ai(self, game_state):
        # 中等AI: 简单评估函数+常见棋型识别
        empty_positions = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if game_state.board[i][j] == 0]
        
        # 检查是否有立即获胜的机会
        for i, j in empty_positions:
            game_state.board[i][j] = 2  # 假设AI下这里
            if game_state.check_win(i, j):
                game_state.board[i][j] = 0  # 恢复
                return (i, j)
            game_state.board[i][j] = 0  # 恢复
        
        # 检查是否需要防守对手的四连
        for i, j in empty_positions:
            game_state.board[i][j] = 1  # 假设对手下这里
            if game_state.check_win(i, j):
                game_state.board[i][j] = 0  # 恢复
                return (i, j)
            game_state.board[i][j] = 0  # 恢复
        
        # 简单评估函数
        best_score = -1
        best_move = None
        
        for i, j in empty_positions:
            score = self.evaluate_position(game_state, i, j)
            if score > best_score:
                best_score = score
                best_move = (i, j)
        
        return best_move if best_move else random.choice(empty_positions) if empty_positions else None
    
    def evaluate_position(self, game_state, row, col):
        # 评估一个位置的得分
        score = 0
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        
        for dr, dc in directions:
            # 检查AI的棋型
            ai_count = 1  # 当前位置
            blocked = False
            
            # 正向检查
            r, c = row + dr, col + dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if game_state.board[r][c] == 2:  # AI的棋子
                    ai_count += 1
                elif game_state.board[r][c] == 1:  # 对手的棋子
                    blocked = True
                    break
                else:  # 空位
                    break
                r += dr
                c += dc
            
            # 反向检查
            r, c = row - dr, col - dc
            while 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE:
                if game_state.board[r][c] == 2:  # AI的棋子
                    ai_count += 1
                elif game_state.board[r][c] == 1:  # 对手的棋子
                    blocked = True
                    break
                else:  # 空位
                    break
                r -= dr
                c -= dc
            
            # 根据棋型给分
            if ai_count >= 5:
                score += 100000  # 必胜
            elif ai_count == 4 and not blocked:
                score += 10000   # 活四
            elif ai_count == 4 and blocked:
                score += 1000    # 冲四
            elif ai_count == 3 and not blocked:
                score += 100    # 活三
            elif ai_count == 3 and blocked:
                score += 10     # 眠三
            elif ai_count == 2 and not blocked:
                score += 5       # 活二
        
        return score
    
    def hard_ai(self, game_state):
        # 高级AI: 使用Minimax算法+Alpha-Beta剪枝
        # 这里简化实现，实际应用中需要更复杂的实现
        return self.medium_ai(game_state)  # 暂时用中等AI代替

# 绘制按钮函数
def draw_button(surface, text, x, y, width, height, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    button_rect = pygame.Rect(x, y, width, height)
    
    # 检查鼠标是否悬停在按钮上
    if button_rect.collidepoint(mouse):
        pygame.draw.rect(surface, active_color, button_rect)
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(surface, inactive_color, button_rect)
    
    # 绘制按钮文本
    font = pygame.font.Font(None, 24)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)
    
    return button_rect

# 绘制游戏界面
def draw_game(game_state):
    screen.fill(BOARD_COLOR)
    
    # 绘制棋盘网格
    for i in range(BOARD_SIZE):
        # 横线
        pygame.draw.line(screen, BLACK, 
                         (MARGIN, MARGIN + i * GRID_SIZE), 
                         (WINDOW_WIDTH - MARGIN, MARGIN + i * GRID_SIZE), 2)
        # 竖线
        pygame.draw.line(screen, BLACK, 
                         (MARGIN + i * GRID_SIZE, MARGIN), 
                         (MARGIN + i * GRID_SIZE, WINDOW_HEIGHT - MARGIN - 80), 2)
    
    # 绘制天元和星位
    star_points = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]
    for row, col in star_points:
        pygame.draw.circle(screen, BLACK, 
                           (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE), 5)
    
    # 绘制棋子
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if game_state.board[row][col] == 1:  # 黑棋
                pygame.draw.circle(screen, BLACK, 
                                   (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE), 
                                   PIECE_RADIUS)
            elif game_state.board[row][col] == 2:  # 白棋
                pygame.draw.circle(screen, WHITE, 
                                   (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE), 
                                   PIECE_RADIUS)
                pygame.draw.circle(screen, BLACK, 
                                   (MARGIN + col * GRID_SIZE, MARGIN + row * GRID_SIZE), 
                                   PIECE_RADIUS, 1)
    
    #    绘制游戏状态信息
    font = pygame.font.Font("msyh.ttc", 36)
    if game_state.game_over   :
        if game_state_state.winner == 1:
            text = font.render(r"黑方获胜!", True, TEXT_COLOR)
        elif game_state.winner == 2:
            text = font.render(r"白方获胜!", True, TEXT_COLOR)
        else:
            text = font.render(r"平局!", True, TEXT_COLOR)
    else:
        if game_state.current_player == 1:
            text = font.render(r"黑方回合", True, TEXT_COLOR)
        else:
            text = font.render(r"白方回合", True, TEXT_COLOR)
    
    screen.blit(text, (20, WINDOW_HEIGHT - 60))
    
    # 绘制控制按钮
    button_width = 100
    button_height = 40
    button_y = WINDOW_HEIGHT - 50
    
    # 重新开始按钮
    restart_button = draw_button(screen, r"Restart", 
                                WINDOW_WIDTH - 220, button_y, 
                                button_width, button_height, 
                                BUTTON_COLOR, BUTTON_HOVER_COLOR)
    
    # 悔棋按钮
    undo_button = draw_button(screen, r"悔棋", 
                             WINDOW_WIDTH - 110, button_y, 
                             button_width, button_height, 
                             BUTTON_COLOR, BUTTON_HOVER_COLOR)
    
    pygame.display.flip()

# 主游戏循环
def main():
    game_state = GameState()
    ai = AI(game_state.ai_difficulty)
    
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                x, y = event.pos
                
                # 检查是否在棋盘上落子
                if MARGIN <= x <= WINDOW_WIDTH - MARGIN and MARGIN <= y <= WINDOW_HEIGHT - 80 - MARGIN:
                    if not game_state.game_over:
                        col = round((x - MARGIN) / GRID_SIZE)
                        row = round((y - MARGIN) / GRID_SIZE)
                        
                        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                            if game_state.make_move(row, col):
                                if place_sound:
                                    place_sound.play()
                                
                                # AI回合
                                if game_state.mode == "ai" and not game_state.game_over and game_state.current_player == 2:
                                    ai_move = ai.make_move(game_state)
                                    if ai_move:
                                        game_state.make_move(ai_move[0], ai_move[1])
                                        if place_sound:
                                            place_sound.play()
                
                # 检查按钮点击（现在通过draw_button函数处理）
        
        # 绘制游戏界面
        draw_game(game_state)
        
        # 处理按钮点击
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        
        # 重新开始按钮区域
        restart_button = pygame.Rect(WINDOW_WIDTH - 220, WINDOW_HEIGHT - 50, 100, 40)
        # 悔棋按钮区域
        undo_button = pygame.Rect(WINDOW_WIDTH - 110, WINDOW_HEIGHT - 50, 100, 40)
        
        if click[0] == 1:
            if restart_button.collidepoint(mouse):
                game_state.reset()
            elif undo_button.collidepoint(mouse):
                if game_state.mode == "human" or (game_state.mode == "ai" and game_state.current_player == 1):
                    game_state.undo_move()
        
        clock.tick(30)

if __name__ == "__main__":
    main()