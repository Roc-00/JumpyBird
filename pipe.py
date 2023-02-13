import cv2
import random

pic_pipe_down = cv2.imread('./assets/pic/pipe_down_600_100.png')
pic_pipe_top = cv2.imread('./assets/pic/pipe_top_600_100.png')

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

vertical_whole_size = WINDOW_HEIGHT - 100  # 上下管道+空白的总长


class Pipe:
    can_get_point = True  # 这个管道能否得分，得过分的不会再得分
    distance_between_pipes = 160  # 上下管道之间的空隙
    top_pipe_len = 0  # 上管道的长度，一旦生成，不可更改，同时下管道的长度也确定
    down_pipe_len = 0  # 下管道的长度

    top_pipe = None  # 用[x1,y1,x2,y2]
    down_pipe = None  # 同上

    refresh_index = 1280  # 到最左端以后刷新的位置

    def __init__(self, img_start_pos, top_pipe_len, distance_between_pipes, refresh_index):
        self.refresh_index = refresh_index
        self.distance_between_pipes = distance_between_pipes
        self.top_pipe_len = top_pipe_len
        self.down_pipe_len = vertical_whole_size - top_pipe_len - distance_between_pipes

        self.top_pipe = [img_start_pos, 0, img_start_pos + 100, top_pipe_len]
        self.down_pipe = [img_start_pos, top_pipe_len + distance_between_pipes,
                          img_start_pos + 100, vertical_whole_size]

    def refresh(self, speed):
        temp = self.top_pipe[0] - speed

        if temp <= -100:
            temp = self.refresh_index
            self.top_pipe_len = random.randint(60, vertical_whole_size - 60 - self.distance_between_pipes)
            self.down_pipe_len = vertical_whole_size - self.top_pipe_len - self.distance_between_pipes

        top_pipe = [temp, 0, temp + 100, self.top_pipe_len]
        down_pipe = [temp, self.top_pipe_len + self.distance_between_pipes,
                          temp + 100, vertical_whole_size]

        self.top_pipe = top_pipe
        self.down_pipe = down_pipe

    def draw(self, img):
        start_index = self.top_pipe[0]
        if start_index >= WINDOW_WIDTH:
            return
        elif start_index >= WINDOW_WIDTH - 100:
            len = WINDOW_WIDTH - start_index
            # 上管道
            img[0:self.top_pipe_len, start_index:WINDOW_WIDTH] = pic_pipe_top[600 - self.top_pipe_len:600, 0:len]
            # 下管道
            img[self.down_pipe[1]:vertical_whole_size, start_index:WINDOW_WIDTH] = pic_pipe_down[0:self.down_pipe_len, 0:len]
        elif start_index >= 0:
            # 上管道
            img[0:self.top_pipe_len, start_index:start_index+100] = pic_pipe_top[600 - self.top_pipe_len:600, 0:100]
            # 下管道
            img[self.down_pipe[1]:vertical_whole_size, start_index:start_index+100] = pic_pipe_down[0:self.down_pipe_len, 0:100]
        else:
            end = self.top_pipe[2]
            # 上管道
            img[0:self.top_pipe_len, 0:end] = pic_pipe_top[600 - self.top_pipe_len:600, 100 - end:100]
            # 下管道
            img[self.down_pipe[1]:vertical_whole_size, 0:end] = pic_pipe_down[0:self.down_pipe_len, 100-end:100]


class PipeManager:
    exist_pipes = []  # 管道
    speed = 6  # 管道移动的速度

    horizontal_interval = WINDOW_WIDTH  # 水平间隔，两条pipe之间的距离
    vertical_interval = 150  # 垂直间隔，上下管道之间的间隔

    def __init__(self, num, horizontal_interval, vertical_interval, speed):
        temp_pipes = []
        start_pos = WINDOW_WIDTH
        self.horizontal_interval = horizontal_interval
        self.vertical_interval = vertical_interval
        self.speed = speed

        refresh_index = num*(horizontal_interval+100) - 100  # 管道刷新的位置，最后一根管道的位置
        for i in range(num):
            top_pipe_len = random.randint(60, vertical_whole_size - 60 - vertical_interval)
            temp_pipes.append(Pipe(start_pos, top_pipe_len, vertical_interval, refresh_index))
            start_pos += horizontal_interval + 100

        self.exist_pipes = temp_pipes

    def refresh(self):
        for pipe in self.exist_pipes:
            pipe.refresh(self.speed)

    def draw_pipes(self, img):
        for pipe in self.exist_pipes:
            pipe.draw(img)