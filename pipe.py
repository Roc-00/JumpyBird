from queue import Queue
import cv2


pic_pipe_down = cv2.imread('./assets/pic/pipe_down_600_100.png')
pic_pipe_top = cv2.imread('./assets/pic/pipe_top_600_100.png')


class Pipe:
    whole_size = 620  # 上下管道+空白的总长
    can_get_point = True  # 这个管道能否得分，得过分的不会再得分
    distance_between_pipes = 160  # 上下管道之间的空隙
    top_pipe_len = 0  # 上管道的长度，一旦生成，不可更改，同时下管道的长度也确定
    down_pipe_len = 0  # 下管道的长度

    img_start_pos = 0  # img中管道水平的起始坐标，即管道最左上角的位置
    img_end_pos = 100  # img中管道水平最右上角的位置

    def __init__(self, img_start_pos, top_pipe_len, distance_between_pipes, whole_size):
        self.whole_size = whole_size
        self.distance_between_pipes = distance_between_pipes
        self.top_pipe_len = top_pipe_len
        self.down_pipe_len = whole_size - top_pipe_len - distance_between_pipes
        self.refresh(img_start_pos)

    def refresh(self, img_start_pos):
        self.img_start_pos = img_start_pos
        img_end_pos = img_start_pos + 100
        # TODO： 刷新pipe的位置


class PipeManager:
    exist_pipe = None

    def load(self):
        self.exist_pipe = Queue()  # 用队列存放已经生成的管道