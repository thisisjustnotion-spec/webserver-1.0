import subprocess

# Node.js 기본 설치 경로 기준
node_exe = r"C:\Program Files\nodejs\node.exe"
npm_cli = r"C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js"

# node.exe로 npm-cli.js 직접 실행
try:
    subprocess.run(["pip", "install", "python-socketio", "opencv-python", "numpy", "ultralytics"])
    print("✅ pip install python-socketio opencv-python numpy ultralytics 완료")
    subprocess.run([node_exe, npm_cli, "init", "-y"], check=True)
    print("✅ npm init -y 완료")
    subprocess.run([node_exe, npm_cli, "install", "express", "socket.io"])
    print("✅ npm install 완료")
except Exception as e:
    print("❌ 실행 에러:", e)
