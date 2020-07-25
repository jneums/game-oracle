from flask_restful import reqparse, Resource
import xgboost
import numpy as np
import json


class PredictGame(Resource):
    def __init__(self, model_path='../models/xgb.bin'):

        # setup the parser for getting game arg
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('game', type=str)

        # initialize a model and load the saved weights
        self.model = xgboost.XGBRegressor()
        self.model.load_model(model_path)

    def get(self):
        # parse the args
        args = self.parser.parse_args()

        # extract the 'game' arg and pre-process 
        # to fit the shape the model expects
        game = self.__process_game(args['game'])

        # make prediction
        prediction = self.model.predict(game)

        # return dictionary containing the prediction
        return {'prediction': str(prediction[0])}

    def __process_game(self, game):
        # model expects a 2d np array
        game = np.array(json.loads(game))
        game = np.array([game])
        return game
