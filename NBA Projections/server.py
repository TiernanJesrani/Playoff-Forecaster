from flask import Flask, render_template
from main import simulator

app = Flask(__name__, static_folder='/static')

playoff_odds = {}
secondround_odds = {}
thirdround_odds = {}
fourthround_odds = {}
finalist_odds = {}

simulator(playoff_odds, secondround_odds, thirdround_odds, fourthround_odds, finalist_odds)

team_odds = []
for team in playoff_odds:
    team_data = {'team_abbreviation': team}
    team_data['playoff_odds'] = playoff_odds[team] if team in playoff_odds else 0
    team_data['conference_semis'] = secondround_odds[team] if team in secondround_odds else 0
    team_data['conference_finals'] = thirdround_odds[team] if team in thirdround_odds else 0
    team_data['finals'] = fourthround_odds[team] if team in fourthround_odds else 0
    team_data['champs'] = finalist_odds[team] if team in finalist_odds else 0
    
    team_odds.append(team_data)

team_odds = sorted(team_odds, key=lambda x:-x['champs'])


@app.route("/")
def home():
    return render_template("home.html", team_data = team_odds)

if __name__ == "__main__":
    app.run(debug=True)

