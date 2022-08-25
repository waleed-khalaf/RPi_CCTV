from asyncio import streams
import cv2


class VideoCamera():

    def __init__(self, stream):
        self.stream = stream
        self.video = cv2.VideoCapture(f"{self.stream}")

    def __del__(self):
        self.video.release()

    def generate_frames(self):
        """ Reads in video stream from RPi camera and generates frames for webpage"""
        while True:

            # read the camera frame
            success, frame = self.video.read()
            if not success:
                break
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
