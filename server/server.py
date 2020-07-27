# import required libraries
from flask import Flask
from flask_restful import Api
from PredictGame import PredictGame
from ListGames import ListGames

# instantiate flask server
app = Flask(__name__)
api = Api(app)


# Setup the Api resource routing here
# Route the URL to the resource
api.add_resource(PredictGame, '/game')
api.add_resource(ListGames, '/games')

if __name__ == '__main__':
    app.run(debug=True)
