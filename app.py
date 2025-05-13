from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Sample flashcard data - in a real app, this would come from a database
flashcards = [
    # Greetings and Common Phrases
    {"irish": "Dia duit", "english": "Hello", "category": "Greetings", "type": "word"},
    {"irish": "Slán", "english": "Goodbye", "category": "Greetings", "type": "word"},
    {"irish": "Go raibh maith agat", "english": "Thank you", "category": "Common phrases", "type": "word"},
    {"irish": "Le do thoil", "english": "Please", "category": "Common phrases", "type": "word"},
    {"irish": "Tá fáilte romhat", "english": "You're welcome", "category": "Common phrases", "type": "word"},
    {"irish": "Gabh mo leithscéal", "english": "Excuse me", "category": "Common phrases", "type": "word"},
    {"irish": "Tá brón orm", "english": "I'm sorry", "category": "Common phrases", "type": "word"},
    {"irish": "Cén t-ainm atá ort?", "english": "What is your name?", "category": "Common phrases", "type": "word"},
    {"irish": "Is mise...", "english": "I am...", "category": "Common phrases", "type": "word"},
    
    # Basic Expressions
    {"irish": "Is maith liom", "english": "I like", "category": "Basic Expressions", "type": "word"},
    {"irish": "Is breá liom", "english": "I love", "category": "Basic Expressions", "type": "word"},
    {"irish": "Ní maith liom", "english": "I don't like", "category": "Basic Expressions", "type": "word"},
    {"irish": "Is fuath liom", "english": "I hate", "category": "Basic Expressions", "type": "word"},
    {"irish": "Tá mé", "english": "I am", "category": "Basic Expressions", "type": "word"},
    {"irish": "Níl mé", "english": "I am not", "category": "Basic Expressions", "type": "word"},
    {"irish": "Tá sé", "english": "He/It is", "category": "Basic Expressions", "type": "word"},
    {"irish": "Tá sí", "english": "She/It is", "category": "Basic Expressions", "type": "word"},
    
    # Shapes
    {"irish": "Cearnóg", "english": "Square", "category": "Shapes", "type": "word"},
    {"irish": "Ciorcal", "english": "Circle", "category": "Shapes", "type": "word"},
    {"irish": "Triantán", "english": "Triangle", "category": "Shapes", "type": "word"},
    {"irish": "Dronuilleog", "english": "Rectangle", "category": "Shapes", "type": "word"},
    
    # Days of the Week
    {"irish": "Dé Luain", "english": "Monday", "category": "Days", "type": "word"},
    {"irish": "Dé Máirt", "english": "Tuesday", "category": "Days", "type": "word"},
    {"irish": "Dé Céadaoin", "english": "Wednesday", "category": "Days", "type": "word"},
    {"irish": "Déardaoin", "english": "Thursday", "category": "Days", "type": "word"},
    {"irish": "Dé hAoine", "english": "Friday", "category": "Days", "type": "word"},
    {"irish": "Dé Sathairn", "english": "Saturday", "category": "Days", "type": "word"},
    {"irish": "Dé Domhnaigh", "english": "Sunday", "category": "Days", "type": "word"},
    
    # Months
    {"irish": "Eanáir", "english": "January", "category": "Months", "type": "word"},
    {"irish": "Feabhra", "english": "February", "category": "Months", "type": "word"},
    {"irish": "Márta", "english": "March", "category": "Months", "type": "word"},
    {"irish": "Aibreán", "english": "April", "category": "Months", "type": "word"},
    {"irish": "Bealtaine", "english": "May", "category": "Months", "type": "word"},
    {"irish": "Meitheamh", "english": "June", "category": "Months", "type": "word"},
    {"irish": "Iúil", "english": "July", "category": "Months", "type": "word"},
    {"irish": "Lúnasa", "english": "August", "category": "Months", "type": "word"},
    {"irish": "Meán Fómhair", "english": "September", "category": "Months", "type": "word"},
    {"irish": "Deireadh Fómhair", "english": "October", "category": "Months", "type": "word"},
    {"irish": "Samhain", "english": "November", "category": "Months", "type": "word"},
    {"irish": "Nollaig", "english": "December", "category": "Months", "type": "word"},
    
    # Seasons
    {"irish": "Earrach", "english": "Spring", "category": "Seasons", "type": "word"},
    {"irish": "Samhradh", "english": "Summer", "category": "Seasons", "type": "word"},
    {"irish": "Fómhar", "english": "Autumn", "category": "Seasons", "type": "word"},
    {"irish": "Geimhreadh", "english": "Winter", "category": "Seasons", "type": "word"},
    
    # Holidays
    {"irish": "Nollaig", "english": "Christmas", "category": "Holidays", "type": "word"},
    {"irish": "Lá Fhéile Pádraig", "english": "St. Patrick's Day", "category": "Holidays", "type": "word"},
    {"irish": "Oíche Shamhna", "english": "Halloween", "category": "Holidays", "type": "word"},
    {"irish": "Lá Caille", "english": "New Year's Day", "category": "Holidays", "type": "word"},
    {"irish": "Lá Breithe", "english": "Birthday", "category": "Personal Holidays", "type": "word"},
    {"irish": "Lá na Máithreacha", "english": "Mother's Day", "category": "Personal Holidays", "type": "word"},
    {"irish": "Lá na nAithreacha", "english": "Father's Day", "category": "Personal Holidays", "type": "word"},
    
    # Day-to-day Sentences
    {"irish": "Cá bhfuil an leithreas?", "english": "Where is the toilet?", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "Cé mhéad atá air?", "english": "How much does it cost?", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "An bhfuil Béarla agat?", "english": "Do you speak English?", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "Níl mé ag tuiscint", "english": "I don't understand", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "Tá mé ag foghlaim Gaeilge", "english": "I am learning Irish", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "Cén t-am é?", "english": "What time is it?", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "Cá bhfuil an stáisiún traenach?", "english": "Where is the train station?", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "Ba mhaith liom caife, le do thoil", "english": "I would like a coffee, please", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "An féidir leat cabhrú liom?", "english": "Can you help me?", "category": "Useful Sentences", "type": "sentence"},
    {"irish": "Tá mé go maith, go raibh maith agat", "english": "I am fine, thank you", "category": "Useful Sentences", "type": "sentence"},
    
    # Restaurant Sentences
    {"irish": "Ba mhaith liom bord a chur in áirithe", "english": "I would like to reserve a table", "category": "Restaurant Phrases", "type": "sentence"},
    {"irish": "An biachlar, le do thoil", "english": "The menu, please", "category": "Restaurant Phrases", "type": "sentence"},
    {"irish": "Tá ocras orm", "english": "I am hungry", "category": "Restaurant Phrases", "type": "sentence"},
    {"irish": "Tá tart orm", "english": "I am thirsty", "category": "Restaurant Phrases", "type": "sentence"},
    {"irish": "An bille, le do thoil", "english": "The bill, please", "category": "Restaurant Phrases", "type": "sentence"},
    {"irish": "Bhí an béile go hálainn", "english": "The meal was delicious", "category": "Restaurant Phrases", "type": "sentence"},
    
    # Travel Sentences
    {"irish": "Cá bhfuil an t-óstán?", "english": "Where is the hotel?", "category": "Travel Phrases", "type": "sentence"},
    {"irish": "Cá bhfuil an aerfort?", "english": "Where is the airport?", "category": "Travel Phrases", "type": "sentence"},
    {"irish": "Cén treo go dtí an lár?", "english": "Which way to the center?", "category": "Travel Phrases", "type": "sentence"},
    {"irish": "Tá mé caillte", "english": "I am lost", "category": "Travel Phrases", "type": "sentence"},
    {"irish": "Cén bus a théann go dtí...?", "english": "Which bus goes to...?", "category": "Travel Phrases", "type": "sentence"},
    {"irish": "Cé mhéad a chosnaíonn ticéad?", "english": "How much does a ticket cost?", "category": "Travel Phrases", "type": "sentence"},
    
    # Emergency Sentences
    {"irish": "Cabhair!", "english": "Help!", "category": "Emergency Phrases", "type": "sentence"},
    {"irish": "Tá gá le dochtúir", "english": "A doctor is needed", "category": "Emergency Phrases", "type": "sentence"},
    {"irish": "Glaoigh ar otharcharr", "english": "Call an ambulance", "category": "Emergency Phrases", "type": "sentence"},
    {"irish": "Tá mé tinn", "english": "I am sick", "category": "Emergency Phrases", "type": "sentence"},
    {"irish": "Cá bhfuil an cógaslann is gaire?", "english": "Where is the nearest pharmacy?", "category": "Emergency Phrases", "type": "sentence"}
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
