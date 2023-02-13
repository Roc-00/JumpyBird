import cv2

WINDOW_HEIGHT = 720 - 50  # 减去地面
WINDOW_WIDTH = 1280


class Bird:
    PIC_BIRD_ROW = 140  # 图片的row 35
    PIC_BIRD_COL = 100  # 图片的col 25

    bird_list = []
    mask_list = []

    start_x = WINDOW_WIDTH // 2  # (start_x, start_y)左上角
    start_y = WINDOW_HEIGHT // 2
    end_x = start_x + PIC_BIRD_ROW   # (end_x, end_y)右下角
    end_y = start_y + PIC_BIRD_COL

    center_x = 0  # 鸟的中心
    center_y = 0

    bird_posture = 0  # 鸟当前是第几个动作，（0，1，2）

    padding_col = 0  # 内边距
    padding_row = 0

    def __init__(self, pic_bird_row, pic_bird_col):
        self.PIC_BIRD_ROW = pic_bird_row
        self.PIC_BIRD_COL = pic_bird_col
        self.padding_row = pic_bird_row // 2
        self.padding_col = pic_bird_row // 2
        for i in range(3):
            # 导入bird的图片，并调整大小
            temp = cv2.imread('./assets/pic/bird_' + str(i) + '.png')
            temp = cv2.resize(temp, (self.PIC_BIRD_ROW, self.PIC_BIRD_COL))
            self.bird_list.append(temp)

            # 将bird转为灰度图
            temp = cv2.cvtColor(temp, cv2.COLOR_BGR2GRAY)
            # 创建掩码
            ret, temp_mask = cv2.threshold(temp, 1, 255, cv2.THRESH_BINARY_INV)
            self.mask_list.append(temp_mask)

    def refresh(self, x, y):
        self.bird_posture = (self.bird_posture + 1) % 2  # 每次刷新位置姿态都变

        if self.padding_row <= x <= WINDOW_WIDTH - self.padding_row and \
                self.padding_col <= y <= WINDOW_HEIGHT - self.padding_col:
            self.center_x = x
            self.center_y = y
            self.start_x = x - self.padding_row
            self.end_x = self.start_x + self.PIC_BIRD_ROW
            self.start_y = y - self.padding_col
            self.end_y = self.start_y + self.PIC_BIRD_COL

    def draw_bird(self, img):
        # 1、找出鸟所在位置
        roi = img[self.start_y:self.end_y, self.start_x:self.end_x]
        # 2、挖空,三通道的‘与’操作
        temp = cv2.bitwise_and(roi, roi, mask=self.mask_list[self.bird_posture])
        # 3、叠加
        dst = cv2.add(temp, self.bird_list[self.bird_posture])
        # 4、放入原图
        img[self.start_y:self.end_y, self.start_x:self.end_x] = dst

    # 检测有没有碰撞或得分
    def detect_crash_point(self, pipes):
        pass

