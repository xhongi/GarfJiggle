from flask import Flask 
from flask_cors import CORS, cross_origin
from database import Database
from markupsafe import escape
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = Database()

@app.route('/getLeaderboard')
@cross_origin()
def returnLeaderboard():
   return {
      'jigglers': [{'name': userData[0], 'count': userData[1]} for userData in db.select_jiggle_ranking()],
      'garfers': [{'name': userData[0], 'count': userData[1]} for userData in db.select_garf_ranking()]
      }

@app.route('/user/<username>')   
@cross_origin()
def returnUserStats(username):
   user_id = db.get_user_id(escape(username))
   #[0][0] = 1st row of result and then column 1, which is the count
   return {'jiggles': db.get_jiggle_count(user_id)[0][0], 'garfs': db.get_garf_count(user_id)[0][0]}


if __name__ == '__main__':
   app.run()