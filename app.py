import sys
import os
sys.path.append( os.path.abspath(os.path.join(os.path.dirname(__file__), 'dots_and_boxes')))
from flask import (Flask, render_template, jsonify, request, redirect, session)
from dots_and_boxes_game import dots_and_boxes_game

# create instance of Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

num_dots = 5
grid_range = range(50,50*num_dots+1,50)
grid = [(x,y) for x in grid_range for y in grid_range]
print("grid_range: ", grid_range)

def html_scores():
    return "Scores<br>" + "<br>".join([p+" : "+str(s) for p, s in session['ds_game'].get_scores().items()])

def html_player():
    return "<h3>Player : " + session['ds_game'].get_current_player() + "</h3><hr>"
    
@app.route("/")
def index():
    session['ds_game'] = dots_and_boxes_game(grid_range)
    return render_template("index.html", player_text={})

# create route that renders index.html template
@app.route("/players", methods=["GET", "POST"])
def send():
    global ds_game
    if request.method == "POST":
        playerA = request.form["playerA"].strip() or "A"
        playerB = request.form["playerB"].strip() or "B" 
        session['ds_game'] = dots_and_boxes_game(grid_range, playerA, playerB)
        #return jsonify({"player":html_player(), "scores" : html_scores()})
        return render_template("index.html", player_text={"player":html_player(), "scores" : html_scores()})
    else:
        return render_template("index.html", player_text={})

@app.route("/game")
def game():
    return render_template("index.html")

@app.route("/play/<position>")
def play(position):
    # print("Play at posi
    # tion : ", position)
    list_position = [float(p) for p in position.split(",")]
    #print("Click at : ", list_position)
    line = session['ds_game'].click(list_position)
    return_dict = {"line":line, "scores":html_scores(),"player":html_player(),
    "squares_player":"","centers":"","winner":""}
    return_dict["squares_player"] = session['ds_game'].get_square_player()
    return_dict["centers"] = session['ds_game'].get_mark_square()
    return_dict["winner"] = session['ds_game'].find_winner()
    #print("Got back :", return_dict)
    return jsonify(return_dict)

@app.route("/show/<position>")
def show(position):
    # print("Play at posi
    # tion : ", position)
    list_position = [float(p) for p in position.split(",")]
    #print("Hover at : ", list_position)
    line = session['ds_game'].get_end_points(list_position)
    return_dict = {"line":line}
    #print("Got back for hover :", return_dict)
    return jsonify(return_dict)

if __name__ == "__main__":
    app.run(debug=True)