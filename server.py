import flask
import numpy as np
import pandas as pd
from solve import findBestAssignment

from flask import Flask, render_template, request, send_from_directory
#from werkzeug import secure_filename
app = Flask(__name__)


@app.route('/')
def upload_html():
	return render_template('app.html')

@app.route('/results', methods = ['GET', 'POST'])
def upload_file():
	if request.method == 'POST':
		f = request.files['file']
		#f.save(secure_filename(f.filename))
		output = process_data(f)

		if output['success']:
			#return '<p>Best team: <b>' + str(output['best_score']) + '</b><p>Team: ' + str(output['best_team']) + '</p>'
			return render_template('report.html',
									best_score=output['best_score'],
									best_team=output['best_team'],
									event_counts=output['event_counts'])
		else:
			return 'Failed: ' + output['reason']

@app.route('/static/<path:path>')
def serve_css(path):
	return send_from_directory('static', path)

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
	solvedTeam = solverResult['best_team']
	print("Solved team: " + str(solvedTeam))
	output['event_counts'] = [0,0,0,0,0,0]
	formattedTeam = []
	print(names)
	for entry in solvedTeam:
		print(entry)
		formattedTeam.append([names[entry[0]], entry[1]])
		for e in entry[1]:
			if e > 0:
				output['event_counts'][e-1] += 1
	print("Formatted team: " + str(formattedTeam))
	output['best_team'] = formattedTeam
	output['df'] = df
	return output

if __name__ == '__main__':
   app.run(debug = True)
