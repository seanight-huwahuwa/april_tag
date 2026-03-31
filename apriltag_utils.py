import cv2
from pupil_apriltags import Detector

# AprilTag 인식 함수
def detect_apriltags(frame, tag_family="tag36h11", camera_params=None, tag_size=0.1):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = Detector(families=tag_family)
    # 1280x720 해상도 기준 임시 카메라 파라미터 (실제 환경에서는 보정값 사용 권장)
    fx = 1000.0
    fy = 1000.0
    cx = 1280 / 2
    cy = 720 / 2
    camera_params = (fx, fy, cx, cy)
    tags = detector.detect(gray, estimate_tag_pose=True, camera_params=camera_params, tag_size=tag_size)
    return tags

# 테스트 코드
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    print("카메라가 열렸습니다. AprilTag 인식 테스트 중... (q/ESC로 종료)")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break
        tags = detect_apriltags(frame)
        for tag in tags:
            corners = tag.corners.astype(int)
            for i in range(4):
                cv2.line(frame, tuple(corners[i]), tuple(corners[(i+1)%4]), (0,255,0), 2)
            cX, cY = int(tag.center[0]), int(tag.center[1])
            cv2.circle(frame, (cX, cY), 5, (0,0,255), -1)
            cv2.putText(frame, f"id:{tag.tag_id}", (cX-10, cY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2)
        cv2.imshow("AprilTag Detection Test", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
    cap.release()
    cv2.destroyAllWindows()
