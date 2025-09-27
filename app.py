from flask import Flask, request, jsonify, render_template
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = "images"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Empty filename"}), 400

    # Save locally
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Git add + commit + push
    subprocess.run(["git", "add", filepath])
    subprocess.run(["git", "commit", "-m", f"Add {file.filename}"])
    subprocess.run(["git", "push"])

    url = f"https://USERNAME.github.io/REPO/images/{file.filename}"
    return jsonify({"url": url})
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
