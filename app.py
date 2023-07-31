from flask import Flask, render_template, request, session, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "boggle-secret"

boggle_game = Boggle()

@app.route('/')
def home():
    board = boggle_game.make_board()
    session['board'] = board
    return render_template('home.html', board=board)

@app.route('/check-word', methods=['POST'])
def check_word():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No json received"}), 400

    word = data.get('word')
    if not word:
        return jsonify({"error": "No word in json"}), 400

    word_check = boggle_game.check_valid_word(session['board'], word)
    return jsonify({'result': word_check})

@app.route("/post-score", methods=["POST"])
def post_score():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No json received"}), 400

    score = data.get("score")
    if score is None:
        return jsonify({"error": "No score in json"}), 400

    session["games_played"] = session.get("games_played", 0) + 1
    session["high_score"] = max(session.get("high_score", 0), score)

    return jsonify({"games_played": session["games_played"], "high_score": session["high_score"]})


if __name__ == '__main__':
    app.run(debug=True)

