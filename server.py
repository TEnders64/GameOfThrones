from flask import Flask, request, render_template, redirect
from mysqlconnection import MySQLConnector
app = Flask(__name__)

mysql = MySQLConnector(app, 'game_of_thrones')

@app.route('/')
def index():
    return redirect('/characters')

@app.route('/characters')
def characters():
    query = "SELECT characters.id, characters.name, houses.name AS house_name, houses.sigil FROM characters JOIN houses ON characters.house_id = houses.id;"
    all_characters = mysql.query_db(query)
    return render_template('index.html', all_characters=all_characters)

@app.route('/characters/new')
def new_character():
    query = "SELECT * FROM houses"
    all_houses = mysql.query_db(query)
    
    return render_template('new.html', all_houses=all_houses)

@app.route('/characters/create', methods=["POST"])
def create_character():
    if request.form['new_house']:
        # insert a new house record
        # insert a new character record
        pass
    else:
        query = "INSERT INTO characters (name, house_id, created_at, updated_at) VALUES (:name, :house_id, NOW(), NOW())"
        data = {
            'name': request.form['character_name'],
            'house_id': request.form['house']
        }
        mysql.query_db(query,data)
    
    return redirect('/characters')

@app.route('/characters/<id>/show')
def show_character(id):
    query = "SELECT * FROM characters WHERE id = :id"
    data = { 'id': id }
    character = mysql.query_db(query,data)
    if len(character) > 0:
        return render_template('show.html', character=character[0])
    else:
        return redirect('/characters')
    
app.run(debug=True)