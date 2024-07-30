from flask import Flask, session, render_template, request, jsonify, redirect, url_for
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

boggle_game = Boggle()

@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    session['score'] = 0
    session['played'] = session.get('played', 0)
    session['high_score'] = session.get('high_score', 0)
    return render_template('index.html', board=board)

@app.route('/check-word')
def check_word():
    word = request.args.get('word')
    board = session['board']
    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/post-score', methods=['POST'])
def post_score():
    score = request.json['score']
    session['played'] = session.get('played', 0) + 1
    session['high_score'] = max(score, session.get('high_score', 0))
    return jsonify({
        'played': session['played'],
        'high_score': session['high_score']
    })

@app.route('/restart')
def restart():
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
