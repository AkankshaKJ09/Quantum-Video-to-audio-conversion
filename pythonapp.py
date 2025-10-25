import os
from tempfile import NamedTemporaryFile
from flask import Flask, request, send_file, make_response
from moviepy.editor import VideoFileClip
from pydub import AudioSegment
from qiskit import QuantumCircuit, Aer, execute

app = Flask(__name__, static_folder='static')

ALLOWED_EXT = ('.mp4', '.mov', '.mkv', '.avi')

def quantum_audio_params():
    qc = QuantumCircuit(2,2)
    qc.h([0,1])
    qc.cx(0,1)
    qc.measure([0,1],[0,1])
    backend = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend=backend, shots=1).result().get_counts()
    bits = list(result.keys())[0]
    gain = 2 if bits[0]=='1' else -2
    mapping = {
        '00': {'mp3_bitrate':'64k', 'wav_samplerate':22050},
        '01': {'mp3_bitrate':'96k', 'wav_samplerate':32000},
        '10': {'mp3_bitrate':'160k','wav_samplerate':44100},
        '11': {'mp3_bitrate':'320k','wav_samplerate':48000},
    }
    params = mapping.get(bits, mapping['00'])
    params['gain'] = gain
    params['bits'] = bits
    return params

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'video' not in request.files:
        return 'No video uploaded', 400
    file = request.files['video']
    fmt = request.form.get('format','mp3').lower()
    if fmt not in ('mp3','wav'):
        return 'Unsupported output format', 400
    if not file.filename.lower().endswith(ALLOWED_EXT):
        return 'Unsupported input video format', 400

    tmp_vid = NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1])
    file.save(tmp_vid.name)

    clip = VideoFileClip(tmp_vid.name)
    tmp_wav = NamedTemporaryFile(delete=False, suffix='.wav')
    clip.audio.write_audiofile(tmp_wav.name, verbose=False, logger=None)
    clip.close()

    audio = AudioSegment.from_wav(tmp_wav.name)
    params = quantum_audio_params()
    audio = audio + params['gain']

    tmp_out = NamedTemporaryFile(delete=False, suffix='.'+fmt)
    if fmt=='wav':
        audio2 = audio.set_frame_rate(params['wav_samplerate'])
        audio2.export(tmp_out.name, format='wav')
    else:
        audio.export(tmp_out.name, format='mp3', bitrate=params['mp3_bitrate'])

    os.remove(tmp_vid.name)
    os.remove(tmp_wav.name)

    resp = make_response(send_file(tmp_out.name, mimetype=f'audio/{fmt}', as_attachment=True, download_name=f'converted_audio.{fmt}'))
    resp.headers['X-Quantum-Info'] = f"bits={params['bits']}; gain_db={params['gain']}"
    return resp

if __name__=='__main__':
    app.run(host='0.0.0.0', port=5000)
