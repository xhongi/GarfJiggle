from flask import Flask 
from flask_cors import CORS, cross_origin
from ranking_queries import select_jiggle_ranking, select_garf_ranking
app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/getLeaderboard')
@cross_origin()
def returnLeaderboard():
   return [select_garf_ranking(), select_jiggle_ranking()]

if __name__ == '__main__':
   app.run()