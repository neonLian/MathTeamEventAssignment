import flask
import numpy as np
import pandas as pd
from solve import findBestAssignment

from flask import Flask, render_template, request
#from werkzeug import secure_filename
app = Flask(__name__)

@app.route('/upload')
def upload_html():
	return render_template('app.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		#f.save(secure_filename(f.filename))
		output = process_data(f)

		if output['success']:
			return 'Best team: ' + str(output['best_score'])
		else:
			return 'Failed: ' + output['reason']

def process_data(file):

	output = {'success': False, 'reason': 'Unknown', 'best_score': 0, 'best_team': [], 'df': None}

	df = pd.read_csv(file)

	# Identify the important columns
	name_col = None
	event_cols = [None,None,None,None,None,None]
	for colname in df.columns:
		if "NAME" in colname.upper():
			name_col = colname
		for e in range(1, 6+1):
			if str(e) in colname:
				event_cols[e-1] = colname
	if name_col is None or None in event_cols:
		output['success'] = False
		output['reason'] = 'Could not find necessary column'
		return output

	# Split dataframe into names and scores
	scores_df = df[event_cols]
	scores_df.fillna(0, inplace=True)
	scores_arr = scores_df.to_numpy().astype(int)

	names = df[name_col]

	# Send information to solver program
	solverResult = findBestAssignment(scores_arr)
	output['success'] = True
	output['best_score'] = solverResult['best_score']
	output['best_team'] = solverResult['best_team']
	output['df'] = df
	return output

if __name__ == '__main__':
   app.run(debug = True)
