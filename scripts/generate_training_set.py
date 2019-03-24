import matplotlib
matplotlib.use('TkAgg')

import argparse
import matplotlib.pyplot as plt
import numpy as np
import json
import os
import pickle

from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path

def contains_maxima(inputpath):
	with open(inputpath) as f:
	    data = json.load(f)
	    return len(data['maxima']) >= 2

def get_training_and_test_sets(inputdir, picklednamespath, outputpath):
	json_paths = None

	# Read it from the cache if provided
	if picklednamespath is None or not os.path.isfile(picklednamespath):
		json_paths = [
			pth.absolute() for pth in Path(inputdir).iterdir() if pth.suffix == '.json' and contains_maxima(pth.absolute())
		]

		if picklednamespath is not None:
			pickle.dump(json_paths, open(picklednamespath, 'wb'))
			print("Wrote filenames to %s" % picklednamespath)

	else:
		json_paths = pickle.load(open(picklednamespath, 'rb'))

	output = []

	for json_path in json_paths:
		with open(json_path) as f:
			data = json.load(f)
			for i in range(len(data['maxima']) - 1):
				first_maxima = data['maxima'][i]
				second_maxima = data['maxima'][i + 1]

				output.append({
					'id': data['_id'],
					'name': data['name'],
					'gender': data['gender'],
					'first_maximum_index': i,
					'first_maximum_year': data['maxima'][i]['year'],
					'second_maximum_year': data['maxima'][i + 1]['year'],
					'input_maximum_percentage': data['maxima'][i]['percent'],
					'next_maximum_percentage': data['maxima'][i + 1]['percent'],
					'next_maximum_time': data['maxima'][i + 1]['year'] - data['maxima'][i]['year']
				})

	train, test = train_test_split(output)

	pickle.dump({
		'train': train,
		'test': test
	}, open(outputpath, 'wb'))
	print("Wrote test/training sets to %s. Training has %s samples and test has %s samples." % (outputpath, len(train), len(test)))


parser = argparse.ArgumentParser(description='Train a model to predict the next maximum of a name.')
parser.add_argument('--json', default=None, help='Path to the directory containing the JSON file.')
# This option is used to remove the overhead of scanning every json file every time
parser.add_argument('--names', default=None, help='Path to the pickled list of json filenames to use.')
parser.add_argument('--output', default=None, required=True, help='Path to the output path to store the training/test set pickle file')

args = parser.parse_args()

get_training_and_test_sets(args.json, args.names, args.output)

