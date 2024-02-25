import pygame
import random
import os

def typing_game(custom_words):
    # 初始化pygame
    pygame.init()

    # 屏幕大小
    WIDTH, HEIGHT = 800, 600

    # 颜色定义
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # 设置屏幕
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("记忆游戏")

    # 字体设置
    font = pygame.font.SysFont(None, 48)

    # 单词列表
    words = custom_words

    # 游戏参数
    speed = 1
    score = 0
    clock = pygame.time.Clock()

    # 准备一个下落的单词
    def new_word():
        word = random.choice(words)
        x = random.randint(0, WIDTH - 100)
        y = -50  # 初始位置在屏幕顶部以上
        return {'word': word, 'x': x, 'y': y}

    word_list = [new_word()]

    # 用户输入框
    input_text = ''
    input_font = pygame.font.SysFont(None, 48)

    # 是否需要添加新单词的标志
    need_new_word = False

    # 退出按钮矩形区域
    quit_button_rect = pygame.Rect(10, 10, 100, 50)

    # 主循环
    running = True
    while running:
        screen.fill(WHITE)

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]  # 删除最后一个字符
                else:
                    input_text += event.unicode

                    # 检查用户输入是否与单词匹配
                    for word in word_list:
                        if word['word'] == input_text.lower():
                            word_list.remove(word)
                            score += 1
                            input_text = ''  # 匹配成功后清空输入框
                            need_new_word = True  # 设置需要添加新单词的标志
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if quit_button_rect.collidepoint(event.pos):
                    running = False

        # 如果需要添加新单词，则添加
        if need_new_word:
            word_list.append(new_word())
            need_new_word = False

        # 更新单词位置
        for word in word_list:
            word['y'] += speed
            if word['y'] > HEIGHT:
                running = False  # 到达底部，游戏失败
                break

        # 渲染单词
        for word in word_list:
            text_surface = font.render(word['word'], True, BLACK)
            screen.blit(text_surface, (word['x'], word['y']))

        # 渲染得分
        score_surface = font.render("Score: " + str(score), True, BLACK)
        screen.blit(score_surface, (10, 10))

        # 渲染输入框
        input_surface = input_font.render("Input: " + input_text, True, BLACK)
        screen.blit(input_surface, (10, HEIGHT - 50))

        # 绘制退出按钮
        pygame.draw.rect(screen, RED, quit_button_rect)
        quit_text = font.render("Quit", True, BLACK)
        screen.blit(quit_text, (quit_button_rect.x + 10, quit_button_rect.y + 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    if running == False:
        os.system("python main.py")
