from flask import request, redirect, url_for
from flask_restful import Resource
import pandas as pd

class AssistantFeedback(Resource):
    def post(self):
        try:
            # Get user input from the form
            user_input = int(request.form['user_input'])

            # Read the CSV file into a DataFrame
            df = pd.read_csv('responses.csv')

            # Get the index of the last row
            last_row_index = df.index[-1]

            # Update the value in the DataFrame
            df.loc[last_row_index, 'feedback'] = user_input

            # Write the updated DataFrame back to the CSV file
            df.to_csv('responses.csv', index=False)

            return {
                'success': True, 
                'message': 'Feedback submitted successfully'
                }

        except Exception as e:
            return {
                'success': False,
                'message': str(e)
                }