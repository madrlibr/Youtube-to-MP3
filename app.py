from flask import Flask, request, render_template, send_file, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            mp3_filename = os.path.splitext(os.path.basename(filename))[0] + '.mp3'
            mp3_path = os.path.join(DOWNLOAD_FOLDER, mp3_filename)

        # render halaman preview
        return render_template('preview.html', filename=mp3_filename)

    except Exception as e:
        return f"Terjadi error: {str(e)}"

@app.route('/play/<filename>')
def play(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename))

@app.route('/get/<filename>')
def get_file(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)