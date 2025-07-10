import pygame
import random
import sys

class SnakeGame:
    def __init__(self):
        """初始化游戏"""
        pygame.init()
        
        # 游戏窗口设置
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("SNAKE GAME")
        
        # 游戏参数设置
        self.cell_size = 20
        self.grid_width = self.width // self.cell_size  # 40列
        self.grid_height = self.height // self.cell_size  # 30行
        
        # 颜色定义
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.green = (0, 255, 0)
        self.red = (255, 0, 0)
        
        # 游戏状态
        self.game_state = "start"  # start, running, over
        self.score = 0
        self.speed = 5  # 初始速度：每秒5格
        self.max_speed = 15  # 最大速度
        
        # 蛇的初始设置
        self.reset_snake()
        
        # 食物初始位置
        self.food_pos = self.generate_food()
        
        # 计时器
        self.last_move_time = 0
        self.move_interval = 1000 // self.speed  # 移动间隔(毫秒)
        
        # 字体设置
        try:
            self.font = pygame.font.Font(None, 36)
        except:
            self.font = pygame.font.SysFont(None, 36)  # 使用系统默认字体
    
    def reset_snake(self):
        """重置蛇的状态"""
        self.snake_pos = [
            [self.grid_width // 2, self.grid_height // 2],  # 蛇头
            [self.grid_width // 2 - 1, self.grid_height // 2],
            [self.grid_width // 2 - 2, self.grid_height // 2]
        ]
        self.direction = "RIGHT"  # 初始方向
        self.next_direction = "RIGHT"  # 下一方向
    
    def generate_food(self):
        """随机生成食物位置"""
        while True:
            food_pos = [
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1)
            ]
            # 确保食物不会生成在蛇身上
            if food_pos not in self.snake_pos:
                return food_pos
    
    def handle_events(self):
        """处理用户输入事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # 键盘控制
            if event.type == pygame.KEYDOWN:
                if self.game_state == "start" and event.key == pygame.K_SPACE:
                    self.game_state = "running"
                elif self.game_state == "over" and event.key == pygame.K_SPACE:
                    self.game_state = "start"
                    self.score = 0
                    self.speed = 5
                    self.reset_snake()
                    self.food_pos = self.generate_food()
                elif self.game_state == "running":
                    # 方向键控制
                    if event.key == pygame.K_UP and self.direction != "DOWN":
                        self.next_direction = "UP"
                    elif event.key == pygame.K_DOWN and self.direction != "UP":
                        self.next_direction = "DOWN"
                    elif event.key == pygame.K_LEFT and self.direction != "RIGHT":
                        self.next_direction = "LEFT"
                    elif event.key == pygame.K_RIGHT and self.direction != "LEFT":
                        self.next_direction = "RIGHT"
    
    def update(self):
        """更新游戏状态"""
        if self.game_state != "running":
            return
        
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_interval:
            return
        
        self.last_move_time = current_time
        self.direction = self.next_direction
        
        # 移动蛇头
        head = self.snake_pos[0].copy()
        if self.direction == "UP":
            head[1] -= 1
        elif self.direction == "DOWN":
            head[1] += 1
        elif self.direction == "LEFT":
            head[0] -= 1
        elif self.direction == "RIGHT":
            head[0] += 1
        
        # 检查碰撞
        # 边界碰撞
        if (head[0] < 0 or head[0] >= self.grid_width or 
            head[1] < 0 or head[1] >= self.grid_height):
            self.game_state = "over"
            return
        
        # 自身碰撞
        if head in self.snake_pos:
            self.game_state = "over"
            return
        
        # 插入新蛇头
        self.snake_pos.insert(0, head)
        
        # 检查是否吃到食物
        if head == self.food_pos:
            self.score += 1
            self.food_pos = self.generate_food()
            
            # 每得5分增加速度
            if self.score % 5 == 0 and self.speed < self.max_speed:
                self.speed = min(self.speed * 1.1, self.max_speed)
                self.move_interval = 1000 // self.speed
        else:
            # 没吃到食物则移除尾部
            self.snake_pos.pop()
    
    def draw(self):
        """绘制游戏界面"""
        self.screen.fill(self.black)
        
        if self.game_state == "start":
            # 开始界面
            title = self.font.render("SNAKE GAME", True, self.white)
            start_text = self.font.render("Press SPACE to start", True, self.white)
            
            self.screen.blit(title, (self.width // 2 - title.get_width() // 2, 
                                    self.height // 2 - 50))
            self.screen.blit(start_text, (self.width // 2 - start_text.get_width() // 2, 
                                         self.height // 2 + 20))
        
        elif self.game_state == "running":
            # 游戏区域边界
            pygame.draw.rect(self.screen, self.white, 
                            (0, 0, self.width, self.height), 2)
            
            # 绘制蛇
            for pos in self.snake_pos:
                pygame.draw.rect(self.screen, self.green, 
                                (pos[0] * self.cell_size, pos[1] * self.cell_size, 
                                 self.cell_size, self.cell_size))
            
            # 绘制食物
            pygame.draw.rect(self.screen, self.red, 
                            (self.food_pos[0] * self.cell_size, 
                             self.food_pos[1] * self.cell_size, 
                             self.cell_size, self.cell_size))
            
            # 显示分数
            score_text = self.font.render(f"Score: {self.score}", True, self.white)
            self.screen.blit(score_text, (self.width - score_text.get_width() - 20, 20))
        
        elif self.game_state == "over":
            # 游戏结束界面
            over_text = self.font.render("GAME OVER", True, self.white)
            score_text = self.font.render(f"Final Score: {self.score}", True, self.white)
            restart_text = self.font.render("Press SPACE to restart", True, self.white)
            
            self.screen.blit(over_text, (self.width // 2 - over_text.get_width() // 2, 
                                         self.height // 2 - 50))
            self.screen.blit(score_text, (self.width // 2 - score_text.get_width() // 2, 
                                          self.height // 2))
            self.screen.blit(restart_text, (self.width // 2 - restart_text.get_width() // 2, 
                                           self.height // 2 + 50))
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        clock = pygame.time.Clock()
        
        while True:
            self.handle_events()
            self.update()
            self.draw()
            clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    game = SnakeGame()
    game.run()