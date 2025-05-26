from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os
import uuid

app = Flask(__name__)
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            return render_template("index.html", error="Please enter a URL.")
        try:
            yt = YouTube(url)
            stream = yt.streams.get_highest_resolution()
            filename = f"{uuid.uuid4()}.mp4"
            filepath = os.path.join(DOWNLOAD_FOLDER, filename)
            stream.download(output_path=DOWNLOAD_FOLDER, filename=filename)
            return render_template("index.html", download_link=f"/download/{filename}", title=yt.title)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

@app.route("/download/<filename>")
def download(filename):
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
