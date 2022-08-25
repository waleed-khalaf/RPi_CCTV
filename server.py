import os
from flask import Flask, render_template, Response, request
from wtforms import Form, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from camera import VideoCamera

app = Flask(__name__)
app.secret_key = "WaleedIsCool"

STREAM = "tcp://81.135.73.137:8554"
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'
camera = cv2.VideoCapture(STREAM, cv2.CAP_FFMPEG)


class RegistrationFrom(FlaskForm):
    email = StringField(label='Email:', validators=[Email()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label="Log In")


# def generate_frames():
#     """ Reads in video stream from RPi camera and generates frames for webpage"""
#     while True:

#         # read the camera frame
#         success, frame = camera.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# Landing/Home Page
@app.route('/')
def landing_page():
    """ doc-string"""
    return render_template('index.html')


# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ doc-string"""
    reg_form = RegistrationFrom()
    reg_form.validate_on_submit()
    username = reg_form.email.data
    password = reg_form.password.data
    print(username, password)
    return render_template('login.html', form=reg_form)


# Sends video frame by frame to the index.html page to be displayed
@app.route('/video')
def video():
    """ Displays video stream frames from RPi onto the webpage """
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == "__main__":
    app.run(debug=True)
