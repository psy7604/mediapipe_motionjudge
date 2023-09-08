import cv2
import mediapipe as mp
import numpy as np
import face_recognition
import math
import dlib


# 计算身体各个关节夹角
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radius = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radius * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# 情绪判断函数
def motionJudge(angle_shoulder_nose, angle_leftBigArm, angle_rightBigArm,
                angle_leftForearm, angle_rightForearm, angle_leftLap,
                angle_rightLap, angle_leftKnee, angle_rightKnee,pointLeftDistance, pointRightDistance):
    if angle_shoulder_nose > 120.0 or max(pointLeftDistance, pointRightDistance) < 10:
        return 'Sleep'       # 鼻肩夹角大于120度且闭眼，判断为‘睡觉’

    if (angle_leftBigArm < 150.0 and angle_rightBigArm < 150.0) and (70.0 < angle_leftForearm < 110.0 and 70.0 < angle_rightForearm < 110.0):
        return 'Capitulate'   # 大臂打直，小臂趋于90度，判断为‘投降’

    if (70.0 < angle_leftLap < 130.0 and angle_leftKnee > 140.0) or (70.0 < angle_rightLap < 130.0 and angle_rightKnee > 140.0):
        return 'Let u out'      #踢腿，判断为‘让你滚’

    if(40.0, 40.0, 70.0, 70.0) < (angle_leftBigArm, angle_rightBigArm, angle_leftForearm, angle_rightForearm) < (90.0, 90.0, 110.0, 110.0):
        return 'Angry'       # 双手叉腰，判断为‘生气’

    else:
        return 'Nothing'

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 视频源
cap = cv2.VideoCapture(0)

# 初始化情绪
motion = None

# 建立mediapipe实例
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()

        # 将图片渲染为RGB模式
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False

        # 姿态检测
        results = pose.process(image)

        # 将图片重新渲染为BGR模式
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # 提取关节点（landmarks）
        try:
            landmarks = results.pose_landmarks.landmark
            ldmarks = face_recognition.face_landmarks(frame)
            # for lndmark in mp_pose.PoseLandmark:
            #     print(lndmark)


            # 获取关节点的坐标
            nose = [landmarks[mp_pose.PoseLandmark.NOSE.value].x,
                        landmarks[mp_pose.PoseLandmark.NOSE.value].y]
            left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
            right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
            right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
            left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
            left_knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
            left_ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
            right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value].y]
            right_knee = [landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
            right_ankle = [landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].x,
                        landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]

            #判断眼睛是否闭上
            leftEye = ldmarks[0]['left_eye']
            top_point_left = leftEye[1]
            top_point_right = leftEye[2]
            bottom_point_left = leftEye[-1]
            bottom_point_right = leftEye[-2]
            pointLeftDistance = math.sqrt(math.pow(top_point_left[0] - bottom_point_left[0], 2) + math.pow(
                top_point_left[1] - bottom_point_left[1], 2))
            pointRightDistance = math.sqrt(math.pow(top_point_left[0] - bottom_point_left[0], 2) + math.pow(
                top_point_left[1] - bottom_point_left[1], 2))

            # 计算夹角
            angle_shoulder_nose = calculate_angle(left_shoulder, nose, right_shoulder)
            angle_leftBigArm = calculate_angle(left_hip, left_shoulder, left_elbow)
            angle_rightBigArm = calculate_angle(right_hip, right_shoulder, right_elbow)
            angle_leftForearm = calculate_angle(left_shoulder, left_elbow, left_wrist)
            angle_rightForearm = calculate_angle(right_shoulder, right_elbow, right_wrist)
            angle_leftLap = calculate_angle(left_shoulder, left_hip, left_knee)
            angle_rightLap = calculate_angle(right_shoulder, right_hip, right_knee)
            angle_leftKnee = calculate_angle(left_hip, left_knee, left_ankle)
            angle_rightKnee = calculate_angle(right_hip, right_knee, right_ankle)

            # 情绪判断
            motion = motionJudge(angle_shoulder_nose, angle_leftBigArm, angle_rightBigArm,
                angle_leftForearm, angle_rightForearm, angle_leftLap,
                angle_rightLap, angle_leftKnee, angle_rightKnee,pointLeftDistance, pointRightDistance)

        except:
            pass


        # 绘制文字显示区
        cv2.rectangle(image, (0, 0), (350, 73), (255, 255, 255), -1)

        # 文字内容显示
        cv2.putText(image, 'Motion:', (15, 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
        cv2.putText(image, str(motion), (10, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 2, cv2.LINE_AA)




        # 记录、绘出检测内容
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(105, 92, 73), thickness=2, circle_radius=2),
                                  mp_drawing.DrawingSpec(color=(61, 3, 44), thickness=2, circle_radius=2)
                                  )


        cv2.namedWindow('Mediapipe Feed', 0)
        cv2.resizeWindow("Mediapipe Feed", 1200, 900)
        cv2.moveWindow("Mediapipe Feed", 200, 50)
        cv2.imshow('Mediapipe Feed', image)

        if cv2.waitKey(10) and 0xFF == ord('q'):
            break

if __name__ == "__main__":
    cap.release()
    cv2.destroyAllWindows()