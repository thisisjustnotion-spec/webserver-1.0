1. node.js 설치하기 (https://nodejs.org/ko/download)
2. python 설치하기 (https://www.python.org/downloads/release/python-3910/)
3. pip install python-socketio opencv-python numpy ultralytics
4. 해당 github 설치 및 압축 풀기
5. webserver-main 폴더(파일들이 보이는 폴더) 안에서 터미널 열기 (vscode를 사용 중이라면 vscode에서 폴더 열기로 webserver를 선택하고 터미널 열기)
6. npm init -y
7. npm install express socket.io
8. 터미널 총 3개 열기 (웹서버, 인공지능+gpio출력, gpio 입력)
9. node server.js / python AI.py / python gpio_input.py 각각 터미널에 입력하기 (만약에 웹캠으로 돌아가도록 테스트하고 싶으면 AI.py 대신 AI_Webcam.py로 하면 됨. 대신 이건 아직 테스트 못 해봐서 웹캠 연결하고 실제 테스트 필요)
