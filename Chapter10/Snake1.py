import curses
import random
import time

class SnakeGame:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        # 初始化游戏窗口
        self.stdscr.nodelay(True)  # 非阻塞输入
        self.stdscr.timeout(100)   # 控制游戏速度(毫秒)
        
        # 初始化游戏状态
        self.reset_game()
        
        # 初始化颜色(如果终端支持)
        self.init_colors()
        
    def init_colors(self):
        """初始化颜色对"""
        if curses.has_colors():
            curses.start_color()
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # 蛇身绿色
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)     # 食物红色
            curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)   # 边界白色
    
    def reset_game(self):
        """重置游戏状态"""
        # 游戏区域大小
        self.height, self.width = self.stdscr.getmaxyx()
        self.game_height = self.height - 5
        self.game_width = self.width - 4
        
        # 蛇的初始位置和方向
        self.snake = [
            [self.game_height//2, self.game_width//2],
            [self.game_height//2, self.game_width//2 - 1],
            [self.game_height//2, self.game_width//2 - 2]
        ]
        self.direction = curses.KEY_RIGHT
        
        # 游戏状态
        self.score = 0
        self.game_over = False
        self.paused = False
        self.started = False
        
        # 生成第一个食物
        self.food = self.generate_food()
    
    def generate_food(self):
        """随机生成食物位置"""
        while True:
            food = [
                random.randint(1, self.game_height - 2),
                random.randint(1, self.game_width - 2)
            ]
            if food not in self.snake:
                return food
    
    def draw_game(self):
        """绘制游戏界面"""
        self.stdscr.clear()
        
        # 绘制标题
        title = "Python Snake Game"
        self.stdscr.addstr(0, (self.width - len(title)) // 2, title)
        
        # 绘制分数
        score_text = f"Score: {self.score}"
        self.stdscr.addstr(1, (self.width - len(score_text)) // 2, score_text)
        
        # 绘制游戏边界
        if curses.has_colors():
            self.stdscr.attron(curses.color_pair(3))
        
        # 上边界
        self.stdscr.addstr(3, 2, "#" * (self.game_width - 1))
        # 下边界
        self.stdscr.addstr(self.game_height + 2, 2, "#" * (self.game_width - 1))
        # 左右边界
        for i in range(4, self.game_height + 2):
            self.stdscr.addstr(i, 2, "#")
            self.stdscr.addstr(i, self.game_width, "#")
        
        if curses.has_colors():
            self.stdscr.attroff(curses.color_pair(3))
        
        # 绘制蛇
        if curses.has_colors():
            self.stdscr.attron(curses.color_pair(1))
        
        for i, segment in enumerate(self.snake):
            if i == 0:  # 蛇头
                self.stdscr.addch(segment[0] + 3, segment[1] + 2, '@')
            else:  # 蛇身
                self.stdscr.addch(segment[0] + 3, segment[1] + 2, 'o')
        
        if curses.has_colors():
            self.stdscr.attroff(curses.color_pair(1))
        
        # 绘制食物
        if curses.has_colors():
            self.stdscr.attron(curses.color_pair(2))
        
        self.stdscr.addch(self.food[0] + 3, self.food[1] + 2, '★')
        
        if curses.has_colors():
            self.stdscr.attroff(curses.color_pair(2))
        
        # 绘制控制提示
        if not self.started:
            hint = "Press any key to start. Use arrow keys to control the snake."
            self.stdscr.addstr(self.height - 2, (self.width - len(hint)) // 2, hint)
        elif self.paused:
            hint = "Game Paused - Press SPACE to continue"
            self.stdscr.addstr(self.height - 2, (self.width - len(hint)) // 2, hint)
        elif self.game_over:
            game_over_text = f"Game Over! Final Score: {self.score}"
            restart_hint = "Press R to restart, Q to quit"
            self.stdscr.addstr(self.height - 3, (self.width - len(game_over_text)) // 2, game_over_text)
            self.stdscr.addstr(self.height - 2, (self.width - len(restart_hint)) // 2, restart_hint)
        
        self.stdscr.refresh()
    
    def handle_input(self):
        """处理键盘输入"""
        key = self.stdscr.getch()
        
        if self.game_over:
            if key == ord('r') or key == ord('R'):
                self.reset_game()
            elif key == ord('q') or key == ord('Q'):
                return False  # 退出游戏
        elif not self.started and key != -1:
            self.started = True
        elif key == ord(' '):  # 空格键暂停/继续
            self.paused = not self.paused
        elif not self.paused and self.started:
            # 方向键控制，防止180度转向
            if (key == curses.KEY_UP and self.direction != curses.KEY_DOWN or
                key == curses.KEY_DOWN and self.direction != curses.KEY_UP or
                key == curses.KEY_LEFT and self.direction != curses.KEY_RIGHT or
                key == curses.KEY_RIGHT and self.direction != curses.KEY_LEFT):
                self.direction = key
        
        return True  # 继续游戏
    
    def game_logic(self):
        """游戏逻辑处理"""
        if not self.started or self.paused or self.game_over:
            return
        
        # 移动蛇
        head = self.snake[0].copy()
        
        if self.direction == curses.KEY_UP:
            head[0] -= 1
        elif self.direction == curses.KEY_DOWN:
            head[0] += 1
        elif self.direction == curses.KEY_LEFT:
            head[1] -= 1
        elif self.direction == curses.KEY_RIGHT:
            head[1] += 1
        
        # 检查碰撞
        if (head[0] <= 0 or head[0] >= self.game_height - 1 or
            head[1] <= 0 or head[1] >= self.game_width - 1 or
            head in self.snake):
            self.game_over = True
            return
        
        # 插入新头部
        self.snake.insert(0, head)
        
        # 检查是否吃到食物
        if head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            # 没吃到食物则移除尾部
            self.snake.pop()
    
    def run(self):
        """主游戏循环"""
        running = True
        while running:
            self.draw_game()
            running = self.handle_input()
            self.game_logic()
            
            # 控制游戏速度
            time.sleep(0.1)

def main(stdscr):
    # 初始化curses
    curses.curs_set(0)  # 隐藏光标
    stdscr.keypad(True)  # 启用特殊键
    
    # 创建游戏实例并运行
    game = SnakeGame(stdscr)
    game.run()

if __name__ == "__main__":
    curses.wrapper(main)