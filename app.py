from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User, db

import threading


app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_URI'


app = Flask(__name__)

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'




is_signing = False

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:  # Password hashing should be used in production.
            login_user(user)
            return redirect(url_for('index'))  # Redirecting to the dashboard after successful login.
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def index():
    return render_template('index.html')

@app.route('/start_signing', methods=['POST'])
def start_signing():
    global is_signing
    if not is_signing:
        is_signing = True
        thread = threading.Thread(target=signing_logic)
        thread.start()
        return jsonify({'message': 'Started signing process.'})
    else:
        return jsonify({'message': 'Signing process already running.'})

@app.route('/stop_signing', methods=['POST'])
def stop_signing():
    global is_signing
    is_signing = False
    return jsonify({'message': 'Stopped signing process.'})

def signing_logic():
    global is_signing  # to control the while loop and stop it when needed

    from PIL import ImageGrab
    import pyautogui
    import cv2
    import numpy as np
    import time

    while is_signing:  # changed from "True" to "is_signing" to allow for stopping
        try:
            # Capture the whole screen
            screenshot = ImageGrab.grab()

            # Convert the screenshot to a numpy array and then to grayscale
            img = np.array(screenshot)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # Read the template image in grayscale
            template = cv2.imread('metamask.png', 0)

            # Perform template matching
            res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            threshold = 0.8
            loc = np.where(res >= threshold)

            if len(loc[0]) > 0:
                # Rest of the logic...
                # Make sure to place appropriate logic to handle the clicks and updates.
                pass
            else:
                print("Element not found, waiting for 5 seconds before trying again")
                time.sleep(5)
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)


if __name__ == "__main__":
    app.run(debug=True)
