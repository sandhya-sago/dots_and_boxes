import sys
import os
import jsonpickle
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), 'dots_and_boxes')))
from flask import (Flask, render_template, jsonify, request, redirect, session)
from dots_and_boxes_game import dots_and_boxes_game

# create instance of Flask app
app = Flask(__name__)
#To keep track of the sessions. Need to use json pickle decode and encode
#because e need to save an object
app.config['SECRET_KEY'] = os.urandom(24)

num_dots = 5
grid_range = range(50,50*num_dots+1,50)
grid = [(x,y) for x in grid_range for y in grid_range]
print("grid_range: ", grid_range)

def html_scores():
    '''Generate html string to show current scores'''
    ds_game = jsonpickle.decode(session['ds_game']) 
    return "Scores<br>" + "<br>".join([p+" : "+str(s) for p, s in ds_game.get_scores().items()])

def html_player():
    '''Generate html string to show current player'''
    ds_game = jsonpickle.decode(session['ds_game']) 
    return "<h3>Player : " + ds_game.get_current_player() + "</h3><hr>"
    
@app.route("/")
def index():
    '''Main page, initialize a game to be played'''
    session['ds_game'] = jsonpickle.encode(dots_and_boxes_game(grid_range))
    return render_template("index.html", player_text={})

# create route that renders index.html template
@app.route("/players", methods=["GET", "POST"])
def send():
    '''Got names for players, Start a new game with the playerrs'''
    if request.method == "POST":
        playerA = request.form["playerA"].strip() or "A"
        playerB = request.form["playerB"].strip() or "B" 
        session['ds_game'] = jsonpickle.encode(dots_and_boxes_game(grid_range, playerA, playerB))
        #return jsonify({"player":html_player(), "scores" : html_scores()})
        return render_template("index.html", player_text={"player":html_player(), "scores" : html_scores()})
    else:
        return render_template("index.html", player_text={})

@app.route("/play/<position>")
def play(position):
    '''Got a click, so figure out the line to play, scores, whose turn it is, 
    and see if game ended'''
    list_position = [float(p) for p in position.split(",")]
    #print("Click at : ", list_position)
    ds_game = jsonpickle.decode(session['ds_game']) 
    line = ds_game.click(list_position)
    session['ds_game'] = jsonpickle.encode(ds_game)
    return_dict = {"line":line, "scores":html_scores(),"player":html_player(),
    "squares_player":"","centers":"","winner":""}
    return_dict["squares_player"] = ds_game.get_square_player()
    return_dict["centers"] = ds_game.get_mark_square()
    return_dict["winner"] = ds_game.find_winner()
    #print("Got back :", return_dict)
    return jsonify(return_dict)

@app.route("/show/<position>")
def show(position):
    '''To flash the line to be played upon mouse hover, not updating game state'''
    list_position = [float(p) for p in position.split(",")]
    line = jsonpickle.decode(session['ds_game']).get_end_points(list_position)
    return_dict = {"line":line}
    return jsonify(return_dict)

if __name__ == "__main__":
    app.run(debug=True)