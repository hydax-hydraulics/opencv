from flask import Flask, render_template, request, jsonify, Response
import cv2

application = Flask(__name__)
video = cv2.imread('static/baby.jpg')


@application.route('/')
def index():
    return render_template("index.html")


def gen(video):
    while True:

        frame_gray = cv2.cvtColor(video, cv2.COLOR_BGR2GRAY)
        edges1 = cv2.Canny(frame_gray, 100, 40)
        ret, jpeg = cv2.imencode('.jpg', edges1)

        frame = jpeg.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@application.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    application.run()