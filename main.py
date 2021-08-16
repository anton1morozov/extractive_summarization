import fasttext.util

from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from summarizers.single_lang_summarizer import SingleLangSummarizer

app = Flask(__name__)
io = SocketIO(app)

# Loading word2vec
fasttext.util.download_model('en', if_exists='ignore')
ft_en = fasttext.load_model('cc.en.300.bin')

summarizer = SingleLangSummarizer(ft_en)


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/process', methods=['POST'])
def process_http():
    if request.method == 'POST':
        data = request.json
        result = summarizer.summarize(data['text'], data['k'])
        return result


@io.on('text_to_process')
def process(obj):
    result = summarizer.summarize(obj['text'], k=int(obj['k']))
    emit('result', result)


@io.on('connection_established', namespace='/')
def connected():
    print('Connected!')


@io.on('connection_lost')
def disconnect():
    print('Disconnected!')


if __name__ == '__main__':
    io.run(app)
