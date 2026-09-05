const express = require('express');
const { createServer } = require('http');
const { Server } = require('socket.io');
const path = require('path'); 

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { 
    cors: { origin: "*" },
    transports: ['websocket', 'polling']
});

// PWA 및 정적 파일(manifest.json, sw.js) 접근 허용
app.use(express.static(path.join(__dirname, 'frontend')));

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'frontend/index.html'));
});

io.on('connection', (socket) => {
    console.log('✅ 클라이언트 연결됨');

    socket.on('image', (data) => {
        if (data && data.image) {
            io.emit('image', data); 
        }
    });

    socket.on('gpio_input', (data) => {
        io.emit('gpio_input', data);
    });
});

httpServer.listen(3000, () => {
    console.log('🚀 서버 시작: http://localhost:3000');
});
