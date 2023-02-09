import sys
import cv2
import mediapipe as mp

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800

BIRD_PATH = './assets/sprites/redbird-midflap.png'

bird_img = cv2.imread(BIRD_PATH)
# 获取屏幕，参数是摄像头的序号，window摄像头的序号默认是0,mac是1
if 'win' in sys.platform:
    cap = cv2.VideoCapture(0)
else:
    cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)  # 设置摄像头图像宽度
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)  # 设置摄像头图像高度

# mediapipe的处理pose的方法
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False,  # 静态图片还是连续视频帧
                    model_complexity=1,  # 选择识别的模型，0,1,2;0是最快，但是不准确
                    smooth_landmarks=True,
                    enable_segmentation=True,
                    min_detection_confidence=0.5,  # 置信度
                    min_tracking_confidence=0.5)  # 置信度
mp_drawing = mp.solutions.drawing_utils  # mediapipe提供的画图方法

while cap.isOpened():
    # 获取画面
    success, img = cap.read()
    if success:
        img = cv2.flip(img, 1)  # 摄像头是和人对立的，将图像左右调换回来正常显示。
        # BGR-->RGB
        img_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 将RGB图像输入模型
        result = pose.process(img_RGB)

        # 可视化
        mp_drawing.draw_landmarks(img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow('mu_window', img)

    if cv2.waitKey(1) == ord('q'):  # 按q结束
        break


# 完成所有操作后，释放捕获器
cap.release()
cv2.destroyAllWindows()