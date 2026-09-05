import socketio
import cv2
import base64
import time
import threading
from ultralytics import YOLO

# Socket.IO 클라이언트 생성
sio = socketio.Client()
image_change_variable = 1

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
    global image_change_variable

    img_path = f'test_image_{image_change_variable}.jpg'
    img = cv2.imread(img_path)
    
    if img is None:
        print(f"❌ {img_path} 파일을 읽을 수 없습니다! 파일이 제대로 업로드됐는지 확인")
        return None
    
    # 이미지 번갈아 바꾸기
    if image_change_variable == 1:
        image_change_variable = 2
    else:
        image_change_variable = 1

    # YOLO 추론 (최적화 옵션 적용)
    results = model(img, imgsz=320, verbose=False, conf=0.25)[0]  # conf=0.25로 낮춰서 더 많은 객체 잡음
    if len(results.boxes) > 0:
        #print("gpio로 1를 출력해서 센서 인식")
        sio.emit('gpio_input', {
                'status': 'triggered',
                'message': '🚨화재 경보🚨',
                'result' : 1,
                'time': time.strftime('%H:%M:%S')
            })
    else:
        sio.emit('gpio_input', {
                'status': 'triggered',
                'message': '🟢 현재 상태: 정상 (화재 미감지)',
                'result' : 0,
                'time': time.strftime('%H:%M:%S')
            })
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
            time.sleep(6)
            continue
            
        sio.emit('image', {
            'image': base64_img,
            'info': 'Real YOLO11n detection result from Python'
        })
        #print(f"📤 YOLO 추론 완료 & 전송 ({time.strftime('%H:%M:%S')})")
        time.sleep(6)  # 2초마다 (Pi에서는 0.5~1초로 줄일 수 있음)

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
        print("🏁 프로그램을 종료합니다.")
