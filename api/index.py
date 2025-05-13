from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='../templates')

# Sample flashcard data - in a real app, this would come from a database
flashcards = [
    # Greetings and Common Phrases
    {"irish": "Dia duit", "english": "Hello", "category": "Greetings"},
    {"irish": "Slán", "english": "Goodbye", "category": "Greetings"},
    {"irish": "Go raibh maith agat", "english": "Thank you", "category": "Common phrases"},
    {"irish": "Le do thoil", "english": "Please", "category": "Common phrases"},
    
    # Basic Expressions
    {"irish": "Is maith liom", "english": "I like", "category": "Expressions"},
    {"irish": "Is breá liom", "english": "I love", "category": "Expressions"},
    {"irish": "Ní maith liom", "english": "I don't like", "category": "Expressions"},
    {"irish": "Is fuath liom", "english": "I hate", "category": "Expressions"},
    
    # Shapes
    {"irish": "Cearnóg", "english": "Square", "category": "Shapes"},
    {"irish": "Ciorcal", "english": "Circle", "category": "Shapes"},
    {"irish": "Triantán", "english": "Triangle", "category": "Shapes"},
    {"irish": "Dronuilleog", "english": "Rectangle", "category": "Shapes"},
    
    # Days of the Week
    {"irish": "Dé Luain", "english": "Monday", "category": "Days"},
    {"irish": "Dé Máirt", "english": "Tuesday", "category": "Days"},
    {"irish": "Dé Céadaoin", "english": "Wednesday", "category": "Days"},
    {"irish": "Déardaoin", "english": "Thursday", "category": "Days"},
    {"irish": "Dé hAoine", "english": "Friday", "category": "Days"},
    {"irish": "Dé Sathairn", "english": "Saturday", "category": "Days"},
    {"irish": "Dé Domhnaigh", "english": "Sunday", "category": "Days"},
    
    # Months
    {"irish": "Eanáir", "english": "January", "category": "Months"},
    {"irish": "Feabhra", "english": "February", "category": "Months"},
    {"irish": "Márta", "english": "March", "category": "Months"},
    {"irish": "Aibreán", "english": "April", "category": "Months"},
    {"irish": "Bealtaine", "english": "May", "category": "Months"},
    {"irish": "Meitheamh", "english": "June", "category": "Months"},
    {"irish": "Iúil", "english": "July", "category": "Months"},
    {"irish": "Lúnasa", "english": "August", "category": "Months"},
    {"irish": "Meán Fómhair", "english": "September", "category": "Months"},
    {"irish": "Deireadh Fómhair", "english": "October", "category": "Months"},
    {"irish": "Samhain", "english": "November", "category": "Months"},
    {"irish": "Nollaig", "english": "December", "category": "Months"},
    
    # Seasons
    {"irish": "Earrach", "english": "Spring", "category": "Seasons"},
    {"irish": "Samhradh", "english": "Summer", "category": "Seasons"},
    {"irish": "Fómhar", "english": "Autumn", "category": "Seasons"},
    {"irish": "Geimhreadh", "english": "Winter", "category": "Seasons"},
    
    # Holidays
    {"irish": "Nollaig", "english": "Christmas", "category": "Holidays"},
    {"irish": "Lá Fhéile Pádraig", "english": "St. Patrick's Day", "category": "Holidays"},
    {"irish": "Oíche Shamhna", "english": "Halloween", "category": "Holidays"},
    {"irish": "Lá Caille", "english": "New Year's Day", "category": "Holidays"},
    {"irish": "Lá Breithe", "english": "Birthday", "category": "Personal Holidays"},
    {"irish": "Lá na Máithreacha", "english": "Mother's Day", "category": "Personal Holidays"},
    {"irish": "Lá na nAithreacha", "english": "Father's Day", "category": "Personal Holidays"}
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

# This is for Vercel serverless deployment
app.debug = False
