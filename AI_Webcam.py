import socketio
import cv2
import base64
import time
import threading
from ultralytics import YOLO

# Socket.IO 클라이언트 생성
sio = socketio.Client()
cap = cv2.VideoCapture(0)

# YOLO 모델 로드 
print("🔄 YOLO11n 모델 로딩 중...")
model = YOLO("best_ncnn_model") 

@sio.event
def connect():
    print("✅ Node.js 서버에 연결 성공!")

@sio.event
def disconnect():
    print("❌ 연결이 끊어졌습니다.")

# YOLO 추론 + 바운딩박스 그린 이미지 생성
def create_yolo_image():
    global cap

    if not cap.isOpened():
        print("❌ 웹캠을 열 수 없습니다. 연결 상태를 확인하세요.")
        return None

    ret, img = cap.read()

    if not ret:
        print("❌ 프레임을 읽어올 수 없습니다.")
        return None

    # YOLO 추론 (최적화 옵션 적용)
    results = model(img, imgsz=320, verbose=False, conf=0.25)[0]  # conf=0.25로 낮춰서 더 많은 객체 잡음
    if len(results.boxes) > 0:
        print("gpio로 1를 출력해서 센서 인식")
    # 바운딩박스 + 라벨 그려진 이미지
    annotated = results.plot()
    
    # JPG → base64
    _, buffer = cv2.imencode('.jpg', annotated)
    return base64.b64encode(buffer).decode('utf-8')

# 이미지 전송 루프 (별도 스레드)
def image_sender():
    while True:
        base64_img = create_yolo_image()
        if base64_img is None:
            time.sleep(2)
            continue
            
        sio.emit('image', {
            'image': base64_img,
            'info': 'Real YOLO11n detection result from Python'
        })
        print(f"📤 YOLO 추론 완료 & 전송 ({time.strftime('%H:%M:%S')})")
        time.sleep(2)  # 2초마다 (Pi에서는 0.5~1초로 줄일 수 있음)

if __name__ == "__main__":
    try:
        sio.connect('http://localhost:3000')
        
        # 이미지 전송 스레드 시작
        threading.Thread(target=image_sender, daemon=True).start()
        
        # 프로그램 유지
        sio.wait()
    except KeyboardInterrupt:
        print("\n🛑 사용자에 의해 프로그램이 중단되었습니다.")
    except Exception as e:
        print("❌ 연결 실패:", e)
    finally:
        if cap.isOpened():
            cap.release()
            print("📷 웹캠 자원이 해제되었습니다.")
        cv2.destroyAllWindows()
        print("🏁 프로그램을 종료합니다.")
