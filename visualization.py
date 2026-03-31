import cv2
import numpy as np


def draw_info_panel(frame, tag_infos, panel_height=100):
    """
    영상 아래에 태그 정보를 표시하는 패널을 추가하여 반환합니다.
    tag_infos: 리스트, 각 태그에 대해 (id, 거리, 각도 등) 튜플/딕셔너리
    panel_height: 정보 패널의 높이 (픽셀)
    """
    h, w = frame.shape[:2]
    # 패널 배경(흰색)
    panel = np.ones((panel_height, w, 3), dtype=np.uint8) * 255

    # 글씨 스타일
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    font_color = (0, 0, 0)
    thickness = 2
    y0 = 30
    dy = 30

    # 태그 경계선 오버레이 (info에 corners가 있으면)
    overlay = frame.copy()
    for info in tag_infos:
        if isinstance(info, dict) and 'corners' in info:
            corners = info['corners']
            for i in range(4):
                pt1 = tuple(map(int, corners[i]))
                pt2 = tuple(map(int, corners[(i+1)%4]))
                cv2.line(overlay, pt1, pt2, (0,255,0), 2)
            # 중심점
            if 'center' in info:
                cX, cY = map(int, info['center'])
                cv2.circle(overlay, (cX, cY), 5, (0,0,255), -1)

    # 태그 정보 출력
    for i, info in enumerate(tag_infos):
        if isinstance(info, dict):
            tag_id = info.get('id', '?')
            x = info.get('x', '?')
            y_pos = info.get('y', '?')
            z = info.get('z', '?')
            roll = info.get('roll', '?')
            pitch = info.get('pitch', '?')
            yaw = info.get('yaw', '?')
        else:
            tag_id = info[0] if len(info) > 0 else '?'
            x = info[1] if len(info) > 1 else '?'
            y_pos = info[2] if len(info) > 2 else '?'
            z = info[3] if len(info) > 3 else '?'
            roll = info[4] if len(info) > 4 else '?'
            pitch = info[5] if len(info) > 5 else '?'
            yaw = info[6] if len(info) > 6 else '?'

        # 안전하게 float 포맷 적용
        def fmt(val, unit, prec=2):
            try:
                return f"{float(val):.{prec}f}{unit}"
            except (ValueError, TypeError):
                return "N/A"
        x_str = fmt(x, 'm')
        y_str = fmt(y_pos, 'm')
        z_str = fmt(z, 'm')
        roll_str = fmt(roll, '°', 1)
        pitch_str = fmt(pitch, '°', 1)
        yaw_str = fmt(yaw, '°', 1)

        text = f"ID: {tag_id}  X: {x_str}  Y: {y_str}  Z: {z_str}  Roll: {roll_str.replace('°', ' deg')}  Pitch: {pitch_str.replace('°', ' deg')}  Yaw: {yaw_str.replace('°', ' deg')}"
        y_draw = y0 + i * dy
        cv2.putText(panel, text, (10, y_draw), font, font_scale, font_color, thickness, cv2.LINE_AA)

    # 영상과 패널을 아래로 이어붙임
    combined = np.vstack((overlay, panel))
    return combined

# 테스트용 메인
if __name__ == "__main__":
    # 임시 영상 생성
    frame = np.zeros((720, 1280, 3), dtype=np.uint8)
    tag_infos = [
        {'id': 1, 'distance': 1.23, 'angle': 15.2},
        {'id': 2, 'distance': 2.34, 'angle': -7.8},
    ]
    out = draw_info_panel(frame, tag_infos)
    cv2.imshow("Test Info Panel", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
