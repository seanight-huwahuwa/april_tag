import cv2

def open_camera(camera_id=0, width=640, height=480):
    """
    카메라를 열고 해상도를 설정합니다.
    Args:
        camera_id (int): 사용할 카메라 번호 (기본값 0)
        width (int): 프레임 가로 해상도
        height (int): 프레임 세로 해상도
    Returns:
        cap (cv2.VideoCapture): 카메라 객체
    """
    cap = cv2.VideoCapture(camera_id)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if not cap.isOpened():
        raise RuntimeError(f"카메라({camera_id})를 열 수 없습니다.")
    return cap

def read_frame(cap):
    """
    카메라에서 프레임을 읽어옵니다.
    Args:
        cap (cv2.VideoCapture): 카메라 객체
    Returns:
        frame (np.ndarray): 읽어온 프레임
    """
    ret, frame = cap.read()
    if not ret:
        raise RuntimeError("프레임을 읽을 수 없습니다.")
    return frame

def release_camera(cap):
    """
    카메라를 해제합니다.
    Args:
        cap (cv2.VideoCapture): 카메라 객체
    """
    cap.release()

def main():
    # 1280x720 해상도로 카메라 열기
    cap = open_camera(0, width=1280, height=720)
    window_name = "Camera (press q or ESC to quit)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    try:
        cv2.startWindowThread()
    except Exception:
        pass

    if not cap.isOpened():
        print("카메라를 열 수 없습니다.")
        return

    print("카메라가 열렸습니다. 영상 창에서 q 또는 ESC를 누르면 종료합니다.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("프레임을 읽을 수 없습니다.")
            break

        cv2.imshow(window_name, frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # q 또는 ESC
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
