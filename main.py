import pygame
import sys
import getpass
import json
from lists import *
from main_requests import *
from transp import *
from game import *
# 初始化pygame
pygame.init()
print("\033[32m注：此处输出的点击情况是根据卡片而定\033[0m")
# 设置屏幕尺寸
SCREEN_WIDTH = 660
SCREEN_HEIGHT = 480
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.DOUBLEBUF)
pygame.display.set_caption("用户中心")
clock = pygame.time.Clock()
# 设置颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
BACKGROUND = (255, 255, 205)
# 设置字体
font = pygame.font.Font("字魂白鸽天行体.ttf", 30)
# 当前用户
current_user = {"username": getpass.getuser()} if getpass.getuser() else None  # 获取当前系统登录的用户名
#常量
beisong = False
fh = False
search_t = False
rectangles = []
jianji = False
#定义
def bar(num):
    if num <= 1000:
        message = "你背了{}个单词，你才刚刚开始背单词，加油！".format(num)
        progress = "{}/1000".format(num)
    else:
        message = "你背了{}个单词，你背单词的数量已经超过中国99.9999%的人，加油！".format(num)
        progress = "{}/{}".format(num, num)
    return message
def bar1(num):
    if num <= 1000:
        message = "你背了{}个单词，你才刚刚开始背单词，加油！".format(num)
        progress = "{}/1000".format(num)
    else:
        message = "你背了{}个单词，你背单词的数量已经超过中国99.9999%的人，加油！".format(num)
        progress = "{}/{}".format(num, num)
    return progress
def clear_screen():
    screen.fill(BACKGROUND)
def write(texts,file_name):
    erjinzhi = []
    for i in texts:
        erjinzhi.append(str(ord(i)))  # 将整数转换为字符串
    with open(file_name, 'a+') as f:
        f.write(','.join(erjinzhi) + '|')  # 使用逗号将整数列表连接为一个字符串，并添加分隔符
def read(file_name):
    try:
        with open(file_name, 'r') as f:
            content = f.read()  # 读取文件的所有内容
            int_lists = []
            for line in content.split('|'):
                if line.strip():  # 跳过空行
                    int_list = [int(num) for num in line.split(',')]  # 解析每行的内容为整数列表
                    int_lists.append(int_list)
            return int_lists
    except FileNotFoundError:
        print("文件不存在！")
        return []
    except Exception as e:
        print("读取文件时出现错误：", e)
        return []
def decode_read(lists):
    t_lists = []
    for int_list in lists:
        t_list = []
        for i in int_list:
            t_list.append(chr(i))
        t_lists.append(''.join(t_list))
    return t_lists
def draw_user_center():
    global tlist
    screen.fill(WHITE)
    draw_text("用户中心", font, BLACK, 300, 50)
    if current_user:
        draw_text("欢迎回来，" + current_user["username"], font, BLACK, 250, 150)
        draw_text(str(bar(len(tlist))),font,(255,0,0),30,350)
        draw_text(str(bar1(len(tlist))),font,(255,0,0),300,400)
    else:
        draw_text("未登录", font, BLACK, 250, 150)

    if current_user:
        logout_button = pygame.Rect(250, 250, 140, 32)
        draw_text("注销", font, BLACK, 285, 255)
    else:
        logout_button = pygame.Rect(250, 250, 140, 32)
        draw_text("登录", font, BLACK, 285, 255)

    back_button = pygame.Rect(250, 300, 140, 32)
    draw_text("返回", font, BLACK, 285, 305)

    pygame.display.flip()

    return logout_button, back_button  # 返回注销按钮对象和返回按钮对象

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def logout():
    global current_user
    current_user = None
    print("注销成功！")
    draw_user_center()

def login():
    global current_user
    current_user = {"username": getpass.getuser()} if getpass.getuser() else None
    print("登录成功！")
    draw_user_center()
def back():
    global rectangles, user_center_shown, beisong, search_t, jianji, fanhuii, play_music
    clear_screen()
    #绘制卡片
    for rect_info in rectangles:
        pygame.draw.rect(screen, [255, 0, 0], rect_info["rect"], 0)
        pygame.draw.rect(screen, [0, 0, 0], rect_info["rect"].inflate(3, 3), 3)
        text = font.render(tlist[rectangles.index(rect_info)], True, (255, 255, 255))
        text_rect = text.get_rect(center=rect_info["rect"].center)
        screen.blit(text, text_rect)
    # 显示用户中心按钮
    draw_text("用户中心", font, BLACK, 535, 15)
    draw_text("首页", font, BLACK, 20, 15)
    draw_text("单词背诵", font, BLACK, 100, 15)
    draw_text("记忆游戏", font, BLACK, 350, 15)
    draw_text("退出", font, BLUE, 250, 15)
    user_center_shown = False
    beisong = False
    search_t = False
    jianji = False
    fanhuii = False
    play_music = False
    pygame.display.update()
tlist = []
tlist = decode_read(read("jizhu.pc3"))
nojizhu = decode_read(read("nojizhu.pc3"))
dh = len(tlist)
print(dh)
if tlist == ['']:
    tlist = ["请去背诵单词"]
print(tlist)
# 主循环
def main():
    #常量
    input_text = ''
    fanhuii = False
    play_music = False
    x = 450
    trans = ""
    letter_num = 0
    last_letter_x = 265
    global beisong,rectangles,fh,search_t,jianji
    search_t = False
    original_page_shown = False
    # if dh > 7:
    #     dh = 7
    clock = pygame.time.Clock()
    # 记录卡片的原始位置
    original_positions = []
    #绘制卡片
    for i in range(dh):
        rect = pygame.Rect(x, 150, 200, 300)
        pygame.draw.rect(screen, [255, 0, 0], rect, 0)
        pygame.draw.rect(screen, [0, 0, 0], rect.inflate(3, 3), 3)
        text = font.render(tlist[i], True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)
        rectangles.append({"rect": rect, "clicked": False})
        original_positions.append(rect.topleft)  # 保存卡片的原始位置
        x -= 20
        

    pygame.display.flip()
    #首页按钮绘制
    draw_text("首页", font, BLACK, 20, 15)
    user_center_button = pygame.Rect(500, 10, 140, 32)  # 移动用户中心按钮到屏幕上方
    user_center_button_copy = pygame.Rect(500, 10, 140, 32)
    draw_text("用户中心", font, BLACK, 535, 15)  # 调整用户中心按钮的位置
    dcbs = pygame.Rect(75, 10, 140, 32)
    draw_text("单词背诵", font, BLACK, 100, 15)
    user_center_shown = False  # 标记用户中心是否已显示
    draw_text("记忆游戏", font, BLACK, 350, 15)
    youxi = pygame.Rect(315, 20, 140, 32)
    fanhui = pygame.Rect(425, 435, 140, 32)
    draw_text("退出", font, BLUE, 250, 15)
    tuichu = pygame.Rect(215, 10, 140, 32)
    tc = pygame.Rect(215, 10, 140, 32)
    jzl = pygame.Rect(235, 85, 140, 32)
    searcht = pygame.Rect(570, 20, 140, 32)
    searcht_copy = pygame.Rect(570, 20, 140, 32)
    mjz = pygame.Rect(395, 155, 140, 32)
    inp_en = pygame.Rect(120, 25, 440, 32)
    while True:
        searcht.move_ip(-1, 0)
        clock.tick(0)
        if beisong:
            # 在输入框中显示输入的文本
            draw_text(input_text, font, BLACK, 122, 20)
            pygame.display.update()  # 更新屏幕显示 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                #判断点击卡片功能
                for rect_info in rectangles:
                    if rect_info["rect"].collidepoint(mouse_pos):
                        print("点击了某张卡片")
                        rect_info["clicked"] = not rect_info["clicked"]
                        if not rect_info["clicked"] and rect_info["rect"].left < 400:
                            rect_info["rect"].topleft = original_positions[rectangles.index(rect_info)]
                        break
                else:
                    print("点击了空白处")
                    for rect_info in rectangles:
                        if rect_info["rect"].left < 400:
                            rect_info["rect"].topleft = original_positions[rectangles.index(rect_info)]
                #点击用户中心
                if user_center_button.collidepoint(mouse_pos):
                    user_center_shown = True
                #用户界面逻辑
                if user_center_shown:
                    logout_button, back_button = draw_user_center()
                    if logout_button.collidepoint(mouse_pos):
                        if current_user:
                            logout()
                        else:
                            login()
                    elif back_button.collidepoint(mouse_pos):
                        user_center_shown = False
                #点击单词背诵
                if dcbs.collidepoint(mouse_pos):
                    beisong = True
                #点击返回
                elif fanhui.collidepoint(mouse_pos):
                    back()
                    tuichu.clamp_ip(tc)
                    user_center_button.clamp_ip(user_center_button_copy)
                    # print(tuichu)
                #点击退出
                elif tuichu.collidepoint(mouse_pos):
                    sys.exit()
                #点击搜索
                elif searcht.collidepoint(mouse_pos):
                    print(translate(input_text))
                    draw_text(trans, font, BLUE, 270, 60)
                    pygame.display.update()
                    search_t = True
                    draw_text("记住了？", font, BLUE, 230, 160)
                    jzl = pygame.Rect(195, 155, 140, 32)
                    draw_text("没记住？", font, BLUE, 430, 160)
                    mjz = pygame.Rect(395, 155, 140, 32)
                    trans = translate(input_text)
                #点击记住了
                elif jzl.collidepoint(mouse_pos):
                    print("您已记住此单词:",input_text)
                    write(input_text,"jizhu.pc3")
                elif mjz.collidepoint(mouse_pos):
                    print("已记录此单词:",input_text)
                    write(input_text,"nojizhu.pc3")
                elif dianji.collidepoint(mouse_pos):
                    jianji = True
                elif fanhui.collidepoint(mouse_pos):
                    fanhuii = True
                    back()
                elif youxi.collidepoint(mouse_pos):
                    li = decode_read(read(random.choice(["jizhu.pc3","nojizhu.pc3"])))
                    typing_game(li)
            elif event.type == pygame.KEYDOWN:
                if inp_en.collidepoint(mouse_pos):
                    if event.key >= pygame.K_a and event.key <= pygame.K_z:
                        # 添加按下的字母到输入文本中
                        input_text += chr(event.key)
                        print(chr(event.key))
                    elif event.key == pygame.K_MINUS:
                        print("-")
                        input_text +="-"
                        # letter_num+=1
                        # last_letter_x = 265+letter_num*10
                    elif event.key == pygame.K_BACKSPACE:
                        if len(input_text) > 0:
                            input_text = input_text[:-1]
                    elif event.key == pygame.K_SPACE:
                        input_text+=" "
                    elif event.unicode.isalpha():
                        # 添加按下的字母到输入文本中
                        input_text += event.unicode
                    else:
                        print("无效字符")
        if beisong:
            # 在输入框中显示输入的文本
            clock.tick(2)
            draw_text(input_text, font, BLACK, 122, 20)
            pygame.display.update()  # 更新屏幕显示
        # 更新卡片的位置
        for rect_info in rectangles:
            if rect_info["clicked"]:
                if rect_info["rect"].left > 0:
                    rect_info["rect"].move_ip(-5, 0)  # 向左移动 5 像素
        # 清空屏幕
        screen.fill([255, 255, 205])
        if len(nojizhu) != 0:
            pygame.draw.circle(screen, GREEN, (315, 85),5, 0)
            draw_text("你还有"+str(len(nojizhu))+"个单词没背会,点我查看",pygame.font.SysFont('华文宋体',16),GREEN,320,76)
            dianji = pygame.Rect(315, 85, 240, 32)
        # 重新绘制卡片
        for rect_info in rectangles:
            pygame.draw.rect(screen, [255, 0, 0], rect_info["rect"], 0)
            pygame.draw.rect(screen, [0, 0, 0], rect_info["rect"].inflate(3, 3), 3)
            text = font.render(tlist[rectangles.index(rect_info)], True, (255, 255, 255))
            text_rect = text.get_rect(center=rect_info["rect"].center)
            screen.blit(text, text_rect)

        # 显示用户中心按钮
        draw_text("用户中心", font, BLACK, 535, 15)
        draw_text("首页", font, BLACK, 20, 15)
        draw_text("单词背诵", font, BLACK, 100, 15)
        draw_text("记忆游戏", font, BLACK, 350, 15)
        draw_text("退出", font, BLUE, 250, 15)
        # 显示用户中心界面
        if user_center_shown:
            draw_user_center()
        #显示背诵页面
        if beisong:
            tuichu.move_ip(900,0)
            user_center_button.move_ip(900,0)
            # print(tuichu)
            screen.fill(BACKGROUND)
            #输入框
            inp_en = pygame.Rect(120, 25, 440, 32)
            pygame.draw.rect(screen, [0, 0, 0], inp_en, 2)
            #搜索按钮
            searcht = pygame.Rect(570, 20, 140, 32)
            draw_text("搜索", font, BLACK, 585, 25)
            #返回按钮
            fanhui = pygame.Rect(425, 435, 140, 32)
            draw_text("返回", font, BLACK, 460, 440)
            pygame.display.update()
            # 在输入框中显示输入的文本
            draw_text(input_text, font, BLACK, 122, 20)
            searcht.clamp_ip(searcht_copy)
            pygame.display.update()  # 更新屏幕显示
        if search_t:
            #----------------------------------------------------------------------------------#
            if play_music:
                draw_text(trans, font, BLUE, 270, 60)
                draw_text("记住了？", font, BLUE, 230, 160)
                jzl = pygame.Rect(195, 155, 140, 32)
                draw_text("没记住？", font, BLUE, 430, 160)
                mjz = pygame.Rect(395, 155, 140, 32)
                pygame.display.update()
            else:
                createRequest(input_text)
                print("正在播放音频...3s")
                time.sleep(3)
                try:
                    pygame.mixer.music.load(sys.argv[0].split("/main.py")[0]+"/media.mp3")  # 加载音乐  
                    pygame.mixer.music.set_volume(1)# 设置音量大小0~1的浮点数
                    pygame.mixer.music.play() # 播放音频
                except:
                    pass
                play_music = True
            #----------------------------------------------------------------------------------#
        if jianji:
            xdianji = 122
            clear_screen()
            nolist = decode_read(read("nojizhu.pc3"))
            for i in nolist:
                draw_text(i, font, BLACK, xdianji, 20)
                xdianji += 40
            draw_text("返回", font, BLACK, 460, 440)
            fanhui = pygame.Rect(425, 435, 100, 32)
        if fanhuii:
            back()
            pygame.display.update()
        pygame.display.update()

if __name__ == "__main__":
    main()
