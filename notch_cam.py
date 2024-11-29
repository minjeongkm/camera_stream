from flask import Flask, request, Response
import cv2
import base64
import numpy as np

app = Flask(__name__)
frame = None  # 실시간 프레임 저장

@app.route('/upload', methods=['POST'])
def upload_frame():
    global frame
    data = request.get_json()
    image_data = data['image'].split(',')[1]
    frame = cv2.imdecode(np.frombuffer(base64.b64decode(image_data), np.uint8), cv2.IMREAD_COLOR)
    return '', 204

@app.route('/video_feed')
def video_feed():
    def generate():
        global frame
        while True:
            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.45.62', port=5000)
