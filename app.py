from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Sample flashcard data - in a real app, this would come from a database
flashcards = [
    {"irish": "Dia duit", "english": "Hello", "category": "Greetings"},
    {"irish": "Slán", "english": "Goodbye", "category": "Greetings"},
    {"irish": "Go raibh maith agat", "english": "Thank you", "category": "Common phrases"},
]

scores = {
    "current_streak": 0,
    "best_streak": 0,
    "total_correct": 0,
    "total_attempts": 0
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/flashcards')
def get_flashcards():
    return jsonify(flashcards)

@app.route('/api/score', methods=['GET'])
def get_score():
    return jsonify(scores)

@app.route('/api/score', methods=['POST'])
def update_score():
    data = request.json
    if data.get('correct'):
        scores['current_streak'] += 1
        scores['total_correct'] += 1
        if scores['current_streak'] > scores['best_streak']:
            scores['best_streak'] = scores['current_streak']
    else:
        scores['current_streak'] = 0
    scores['total_attempts'] += 1
    return jsonify(scores)

if __name__ == '__main__':
    app.run(debug=True)
