from flask import Flask, render_template, request, redirect, send_file, flash
from werkzeug.utils import secure_filename
import os
import subprocess
from datetime import datetime

app = Flask(__name__)

app.secret_key = "abhinav@METIS"

today = datetime.now()
folder_name = today.strftime("%b-%d-%Y-%H-%M-%S")
uploads_dir = os.path.join(app.instance_path, 'uploads', folder_name)
os.makedirs(uploads_dir, exist_ok=True)

@app.route("/")
def uploader():
    if folder_name in os.listdir('static/'):
        path = 'static/'+folder_name
        uploads = sorted(os.listdir(path))
        uploads = [folder_name+"/" + file for file in uploads]
        return render_template("index.html", uploads=uploads)
    else:
        return render_template('index.html')

@app.route("/upload", methods=["POST", "GET"])
def upload():
    if request.method == "POST":
        files = request.files.getlist('files[]')
        for f in files:
            filename = secure_filename(f.filename)
            f.save(os.path.join(uploads_dir, filename))
        flash('File(s) successfully uploaded')
    return detect()

@app.route("/detect")
def detect():
    subprocess.run("ls")
    subprocess.run(['python3', 'detect.py', '--weights', 'best.pt', '--source', uploads_dir, '--img', '640',
                    '--conf', '0.5', '--project', 'static', '--name', folder_name, '--save-txt','--device','0'])
    return redirect("/")

@app.route('/return-files', methods=['GET'])
def return_file():
    folder = (os.listdir("runs/detect/"))[-1]
    filename = (os.listdir(f"runs/detect/{folder}/"))[-1]
    path = f"runs/detect/{folder}/{filename}"
    try:
        return send_file(path)
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)
