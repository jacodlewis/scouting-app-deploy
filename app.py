from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import requests 
import base64
import io

app = Flask(__name__)
app.secret_key = "secret"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(days=5)

db = SQLAlchemy(app)
class Data(db.Model):
    _id = db.Column(db.Integer, primary_key=True)
    team = db.Column(db.Integer)
    match_number = db.Column(db.Integer)
    team_note = db.Column(db.String(250))

    def __init__(self, team, match_number, team_note):
        self.team = team
        self.match_number = match_number
        self.team_note = team_note

teamsearch = None 
matchsearch = None

@app.route("/")
def home():
    return render_template("stats.html")

@app.route("/teamscore/", methods=["POST", "GET"])
def teamScore():
    if request.method == "POST":
        team = request.form["team"]
        match_number = request.form["match_number"]
        team_note = request.form["team_note"]
        match_Data = Data(team=team, match_number=match_number, team_note=team_note)
        db.session.add(match_Data)
        db.session.commit()
        return redirect(url_for("stats"))

    return render_template("score.html")

@app.route("/stats/", methods=["POST", "GET"])
def stats():
    if request.method == "POST":
        if "match_id" in request.form:
            match_id = request.form["match_id"]
            Data.query.filter_by(_id=match_id).delete()
            db.session.commit()
        elif "teamsearch" in request.form:
            global teamsearch
            teamsearch = request.form["teamsearch"]
            return redirect(url_for("teampage", team=teamsearch))
        elif "matchsearch" in request.form:
            global matchsearch
            matchsearch = request.form["matchsearch"]
            return redirect(url_for("matchpage", match=matchsearch))
    return render_template("stats.html", stats=Data.query.all())

@app.route("/stats/team_page/", methods=["POST", "GET"])
def teampage():
    if request.method == "POST":
        if "match_id" in request.form:
            match_id = request.form["match_id"]
            Data.query.filter_by(_id=match_id).delete()
            db.session.commit()
        elif "teamsearch" in request.form:
            global teamsearch
            teamsearch = request.form["teamsearch"]
            return redirect(url_for("teampage", team=teamsearch))
        elif "matchsearch" in request.form:
            global matchsearch
            matchsearch = request.form["matchsearch"]
            return redirect(url_for("matchpage", match=matchsearch))
    return render_template("teampage.html", stats=Data.query.filter_by(team=teamsearch))
    
@app.route("/stats/match_page/", methods=["POST", "GET"])
def matchpage():
    if request.method == "POST":
        if "match_id" in request.form:
            match_id = request.form["match_id"]
            Data.query.filter_by(_id=match_id).delete()
            db.session.commit()
        elif "teamsearch" in request.form:
            global teamsearch
            teamsearch = request.form["teamsearch"]
            return redirect(url_for("teampage", team=teamsearch))
        elif "matchsearch" in request.form:
            global matchsearch
            matchsearch = request.form["matchsearch"]
            return redirect(url_for("matchpage", match=matchsearch))
    return render_template("matchpage.html", stats=Data.query.filter_by(match_number=matchsearch))

@app.errorhandler(405)
def method_not_allowed(e):
    return render_template("405.html"), 405

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)