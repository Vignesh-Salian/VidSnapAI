from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp4', 'mov', 'avi', 'mkv', 'webm'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ── VidSnapAI Routes ──────────────────────

@app.route("/")
def home():
    """Landing page with hero, features, and trending snaps."""
    return render_template("index.html")

@app.route("/studio",methods=["GET","POST"])
def studio():
    myid=uuid.uuid1()
    if request.method=="POST":
        print(request.files.keys())
        rec_id=request.form.get("uuid")
        desc=request.form.get("text")
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], str(rec_id))
        os.makedirs(upload_path, exist_ok=True)
        
        #capture the description and save it to a file
        with open(os.path.join(upload_path, "desc.txt"), "w", encoding="utf-8") as f:
            f.write(desc if desc else "")
            
        input_files=[]
        for key,value in request.files.items():
            print(key,value)
            #upload the  file
            file=request.files[key]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_path, filename))
                input_files.append(file.filename)

        with open(os.path.join(upload_path, "input.txt"), "w", encoding="utf-8") as f:
            for fl in input_files:
                f.write(f"file '{fl}'\nduration 1\n")
    return render_template("create.html", myid=myid)

@app.route("/snaps")
def snaps():
    os.makedirs("static/reels", exist_ok=True)
    reels=os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels=reels)

if __name__ == "__main__":
    app.run(debug=True)