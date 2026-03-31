import cv2
from camera_utils import open_camera
from apriltag_utils import detect_apriltags
from visualization import draw_info_panel


def main():
    cap = open_camera(0, width=1280, height=720)
    if not cap or not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("실시간 AprilTag 인식 및 정보 표시 (q/ESC로 종료)")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("프레임을 읽을 수 없습니다.")
                break

            tags = detect_apriltags(frame)
            import numpy as np
            import math
            info_list = []
            for tag in tags:
                tag_id = tag.tag_id
                x = y = z = roll = pitch = yaw = None
                if hasattr(tag, 'pose_t') and tag.pose_t is not None:
                    # pose_t: (3, 1) numpy array, 단위: m
                    x = tag.pose_t[0][0]
                    y = tag.pose_t[1][0]
                    z = tag.pose_t[2][0]
                if hasattr(tag, 'pose_R') and tag.pose_R is not None:
                    # pose_R: (3, 3) numpy array
                    R = tag.pose_R
                    # 회전 행렬 -> roll, pitch, yaw (ZYX 순서)
                    sy = math.sqrt(R[0,0] * R[0,0] + R[1,0] * R[1,0])
                    singular = sy < 1e-6
                    if not singular:
                        roll = math.atan2(R[2,1], R[2,2]) * 180 / math.pi
                        pitch = math.atan2(-R[2,0], sy) * 180 / math.pi
                        yaw = math.atan2(R[1,0], R[0,0]) * 180 / math.pi
                    else:
                        roll = math.atan2(-R[1,2], R[1,1]) * 180 / math.pi
                        pitch = math.atan2(-R[2,0], sy) * 180 / math.pi
                        yaw = 0
                info = {
                    'id': tag_id,
                    'x': x,
                    'y': y,
                    'z': z,
                    'roll': roll,
                    'pitch': pitch,
                    'yaw': yaw,
                    'corners': tag.corners if hasattr(tag, 'corners') else None,
                    'center': tag.center if hasattr(tag, 'center') else None
                }
                info_list.append(info)

            output = draw_info_panel(frame, info_list)
            cv2.imshow("AprilTag Detection", output)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
