"""
YT Drop — Backend para Render.com (grátis para sempre)
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp, os, threading, uuid, tempfile, time

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = tempfile.mkdtemp()
jobs = {}

def fmt_speed(s):
    if not s: return '0 KB/s'
    if s >= 1_000_000: return f'{s/1_000_000:.1f} MB/s'
    return f'{s/1_000:.1f} KB/s'

def make_hook(job_id):
    def hook(d):
        if d['status'] == 'downloading':
            dl  = d.get('downloaded_bytes', 0)
            tot = d.get('total_bytes') or d.get('total_bytes_estimate', 1)
            jobs[job_id].update({
                'status':  'downloading',
                'percent': round(dl / tot * 100, 1),
                'speed':   fmt_speed(d.get('speed', 0)),
                'eta':     d.get('eta', 0),
            })
        elif d['status'] == 'finished':
            jobs[job_id]['status'] = 'processing'
        elif d['status'] == 'error':
            jobs[job_id]['status'] = 'error'
    return hook

@app.route('/api/info', methods=['POST'])
def info():
    url = (request.json or {}).get('url', '').strip()
    if not url:
        return jsonify({'error': 'URL ausente'}), 400
    try:
        with yt_dlp.YoutubeDL({
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 15,
    'extractor_args': {'youtube': {'player_client': ['android']}},
}) as ydl:            meta = ydl.extract_info(url, download=False)
        return jsonify({
            'title':      meta.get('title', 'Sem título'),
            'duration':   meta.get('duration', 0),
            'thumbnail':  meta.get('thumbnail', ''),
            'uploader':   meta.get('uploader', ''),
            'view_count': meta.get('view_count', 0),
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['POST'])
def download():
    body  = request.json or {}
    url   = body.get('url', '').strip()
    fmt   = body.get('format', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best')
    label = body.get('format_label', '')
    if not url:
        return jsonify({'error': 'URL ausente'}), 400

    job_id = str(uuid.uuid4())
    jobs[job_id] = {'status': 'starting', 'percent': 0, 'speed': '—', 'eta': '—'}

    def worker():
        try:
            opts = {
                'format':         fmt,
                'outtmpl':        os.path.join(DOWNLOAD_DIR, f'{job_id}_%(title)s.%(ext)s'),
                'progress_hooks': [make_hook(job_id)],
                'quiet':          True,
                'no_warnings':    True,
                'socket_timeout': 20,
                'retries':        3,
		'extractor_args': {'youtube': {'player_client': ['android']}},
            }
            if 'MP3' in label.upper():
                opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            with yt_dlp.YoutubeDL(opts) as ydl:
                ydl.download([url])

            files = [f for f in os.listdir(DOWNLOAD_DIR) if f.startswith(job_id)]
            if files:
                jobs[job_id].update({'status': 'ready', 'file': files[0], 'percent': 100})
            else:
                jobs[job_id].update({'status': 'error', 'error': 'Arquivo não encontrado'})
        except Exception as e:
            jobs[job_id].update({'status': 'error', 'error': str(e)})

    threading.Thread(target=worker, daemon=True).start()
    return jsonify({'job_id': job_id})

@app.route('/api/progress/<job_id>')
def progress(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job não encontrado'}), 404
    return jsonify(job)

@app.route('/api/file/<job_id>')
def get_file(job_id):
    job = jobs.get(job_id)
    if not job or job.get('status') != 'ready':
        return jsonify({'error': 'Arquivo não pronto'}), 404
    filepath   = os.path.join(DOWNLOAD_DIR, job['file'])
    clean_name = job['file'][len(job_id)+1:]
    def cleanup():
        time.sleep(10)
        try: os.remove(filepath); jobs.pop(job_id, None)
        except: pass
    threading.Thread(target=cleanup, daemon=True).start()
    return send_file(filepath, as_attachment=True, download_name=clean_name)

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f'🚀 YT Drop backend na porta {port}')
    app.run(host='0.0.0.0', port=port, debug=False)
