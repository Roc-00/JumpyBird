import cv2
import mediapipe as mp
import sys
import utils
import bird
import pipe

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PIC_BIRD_ROW = 140  # 鸟的图片的row
PIC_BIRD_COL = 100  # 鸟的图片的col

DISTANCE_BETWEEN_PIPES = 160  # 管道之间的距离


class Game:
    bird = None
    pipes = None
    cap = None  # 摄像头
    pose = None  # mediapipe加工人体姿态的模型

    game_state = 1  # 游戏状态 0:准备; 1:进行中 2:结束
    detect_time = 0  # 检测人体符合要求的开始时间
    prior_flag = False  # 上一帧检测是否符合要求
    game_point = 0  # 游戏得分
    speed = 10  # 图片移动速度

    pipe_num = 10
    pipe_interval = 300

    def __init__(self):
        # 实例化一只鸟
        self.bird = bird.Bird(PIC_BIRD_ROW, PIC_BIRD_COL)

        # 实例化管道
        self.pipes = pipe.PipeManager(self.pipe_num, self.pipe_interval, 150, self.speed)

        # 获取屏幕，参数是摄像头的序号，window摄像头的序号默认是0,mac是1
        if 'win' in sys.platform:
            self.cap = cv2.VideoCapture(0)
        else:
            self.cap = cv2.VideoCapture(1)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)  # 设置摄像头图像宽度
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)  # 设置摄像头图像高度

        # mediapipe的处理pose的方法
        mp_pose = mp.solutions.pose
        self.pose = mp_pose.Pose(static_image_mode=False,  # 静态图片还是连续视频帧
                                 model_complexity=1,  # 选择识别的模型，0,1,2;0是最快，但是不准确
                                 smooth_landmarks=True,
                                 enable_segmentation=True,
                                 min_detection_confidence=0.5,  # 置信度
                                 min_tracking_confidence=0.5)  # 置信度

    def game_stater(self):
        land_pos = 0  # 地面图片的坐标
        while self.cap.isOpened():
            # 获取画面
            success, frame = self.cap.read()
            if success:
                # 摄像头是和人对立的，将图像左右调换回来正常显示。
                frame = cv2.flip(frame, 1)
                temp_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 将RGB图像输入模型
                result = self.pose.process(temp_frame)
                landmarks = result.pose_landmarks

                # 无论哪种游戏状态都先画地面
                utils.draw_land(frame, land_pos)
                land_pos = (land_pos + self.speed) % 120

                if self.game_state == 0:
                    bird_pos = utils.bird_by_head(landmarks)  # 通过头部得到鸟的当前xy
                    # bird_pos = utils.bird_by_body(landmarks)  # 通过身体得到鸟的当前xy
                    if bird_pos is not None:
                        self.bird.refresh(bird_pos[0], bird_pos[1])  # 刷新鸟的当前位置
                    self.bird.draw_bird(frame)  # 画鸟
                elif self.game_state == 1:
                    bird_pos = utils.bird_by_head(landmarks)  # 得到鸟的当前xy
                    # bird_pos = utils.bird_by_body(landmarks)  # 通过身体得到鸟的当前xy
                    if bird_pos is not None:
                        self.bird.refresh(bird_pos[0], bird_pos[1])  # 刷新鸟的当前位置
                    self.bird.draw_bird(frame)  # 画鸟

                    self.pipes.refresh()
                    self.pipes.draw_pipes(frame)
                else:
                    pass

                # 展示画面
                cv2.imshow('Jumpy Bird', frame)

            if cv2.waitKey(1) == ord('q') or cv2.waitKey(1) == ord('Q'):
                break

        # 完成所有操作后，释放捕获器
        self.cap.release()
        cv2.destroyAllWindows()