import pygame
from pygame.locals import *
import time
import random



SIZE = 40
BACKGROUND_COLOR = (30, 30, 50)
GRID_WIDTH = 800 // SIZE
GRID_HEIGHT = 600 // SIZE



class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * 3
        self.y = SIZE * 3


    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()
    

    def move(self):
        self.x = random.randint(1, GRID_WIDTH - 1) * SIZE
        self.y = random.randint(1, GRID_HEIGHT - 1) * SIZE
        # self.draw()




class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [SIZE]
        self.y = [SIZE]

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


    def move_up(self):
        self.direction = 'up'
    
    def move_down(self):
        self.direction = 'down'
    
    def move_right(self):
        self.direction = 'right'
    
    def move_left(self):
        self.direction = 'left'


    def draw(self):
        self.parent_screen.fill((BACKGROUND_COLOR))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()


    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        if self.direction == 'up':
            self.y[0] -= SIZE
        elif self.direction == 'down':
            self.y[0] += SIZE
        elif self.direction == 'left':
            self.x[0] -= SIZE
        elif self.direction == 'right':
            self.x[0] += SIZE
        self.draw()



class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        self.play_background_music()

        self.screen = pygame.display.set_mode((800, 600))
        # self.screen = pygame.display.set_mode((GRID_WIDTH, GRID_HEIGHT))
        self.snake = Snake(self.screen, 1)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()

    
    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(-1, 0)


    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 and  x1 <= x2 +SIZE and y2 <= y1 and y1 <= y2 + SIZE:
            return True
        return False
        
    
    def display_score(self):
        font = pygame.font.SysFont("arial", 20)
        score = font.render(f"Score:  {self.snake.length}", True , (255, 255, 255))
        self.screen.blit(score, (700, 10))
        # pygame.display.flip()


    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        #snake apple collision
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self. apple.y):
            # point_sound = pygame.mixer.Sound("resources/ding.mp3")
            # pygame.mixer.Sound.play(point_sound)
            self.play_sound("ding")
            self.apple.move()
            self.snake.increase_length()

        #snake self collision
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                # game_over_sound = pygame.mixer.Sound("resources/game_over.mp3")
                pygame.mixer.music.stop()
                self.play_sound("game_over")
                raise Exception("Game Over!")
            
            
    def show_game_over(self):
        self.screen.fill((BACKGROUND_COLOR))
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(f"Game Over! Score:  {self.snake.length}", True, (255, 255, 255))
        self.screen.blit(line1, (200, 250))
        line2 = font.render("Press Enter to play again or Escape to exit", True, (255, 255, 255))
        self.screen.blit(line2, (200, 300))
        pygame.display.flip()

    
    def reset(self):
        self.snake = Snake(self.screen, 1)
        # self.snake.draw()
        self.apple = Apple(self.screen)
        # self.apple.draw()


    def run(self):
        running = True
        pause = False
        game_over = False
        game_over_sound_played = False  # NEW


        pygame.display.set_caption("Snake Game")

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        if game_over:
                            game_over = False
                            self.reset()
                            self.play_background_music()
                        pause = False
                    # if event.key == K_p or event.key == K_SPACE:
                    #     pause = not pause
                    #     if pause:
                    #         pygame.mixer.music.pause()
                    #     else:
                    #         pygame.mixer.music.unpause()
                    if event.key == K_p or event.key == K_SPACE:
                        if not game_over:  
                            pause = not pause
                        if pause:
                            pygame.mixer.music.pause()
                        else:
                            pygame.mixer.music.unpause()

                    if not pause and not game_over:
                        if event.key == K_UP or event.key == K_w:
                            self.snake.move_up()
                        if event.key == K_DOWN or event.key == K_s:
                            self.snake.move_down()
                        if event.key == K_LEFT or event.key == K_a:
                            self.snake.move_left()
                        if event.key == K_RIGHT or event.key == K_d:
                            self.snake.move_right()
                elif event.type == QUIT:
                    running = False

            try:
                if not pause and not game_over:
                    self.play()
                elif pause and not game_over:
                    font = pygame.font.SysFont("arial", 30)
                    pause_text = font.render("Game Paused. Press 'P' or Space to Resume", True, (255, 255, 255))
                    self.screen.blit(pause_text, (200, 350))
                    pygame.display.flip()
            except Exception as e:
                if not game_over_sound_played:
                    pygame.mixer.music.stop()
                    self.play_sound("game_over")
                    game_over_sound_played = True  
                    self.show_game_over()
                    game_over = True
                    pause = False

                

            time.sleep(0.2)
        


if __name__ == "__main__":
    game = Game()
    game.run()
