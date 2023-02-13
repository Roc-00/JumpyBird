import cv2

WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1280
pic_land = cv2.imread('./assets/pic/land_1400.png')


# 头所在的点当鸟
def bird_by_head(landmarks):
    if landmarks is None:
        return None
    x = int(landmarks.landmark[0].x * WINDOW_WIDTH)
    y = int(landmarks.landmark[0].y * WINDOW_HEIGHT)

    return [x, y]


# 身体所在的点当鸟
def bird_by_body(landmarks):
    # return landmarks[11] 和 [12] 的中间往下 100
    if landmarks is None:
        return None
    x1 = int(landmarks.landmark[11].x * WINDOW_WIDTH)
    y1 = int(landmarks.landmark[11].y * WINDOW_HEIGHT)

    x2 = int(landmarks.landmark[12].x * WINDOW_WIDTH)
    y2 = int(landmarks.landmark[12].y * WINDOW_HEIGHT)

    return [(x1 + x2)//2, (y1 + y2)//2 + 100]


# 画陆地
def draw_land(img, start_pos):
    img[WINDOW_HEIGHT-100:WINDOW_HEIGHT, 0:WINDOW_WIDTH] = pic_land[0:100, start_pos:start_pos + WINDOW_WIDTH]

