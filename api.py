from flask import Flask 
from flask_cors import CORS, cross_origin
from database import Database
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = Database()

@app.route('/getLeaderboard')
@cross_origin()
def returnLeaderboard():
   return [db.select_garf_ranking(), db.select_jiggle_ranking()]

if __name__ == '__main__':
   app.run()