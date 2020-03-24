#=============================Imports==============================#

import numpy as np
from extract import *
from normalize import *
# import ui as u
#==================================================================#

#Initialize train_y in case no training occurs
train_y = np.zeros(289)
train_y[0:240] = -1
train_y[241:288] = 1
#=============================KNN Model============================#

# Distance between instances x1 and x2
def dist(x1, x2):
	dist = np.linalg.norm(x1-x2)
	dist = dist**2
	return dist


def classify(train_x, train_y, k, x):
	'''
	Use distance to determine k nearest x vectors, and then use sum on
	corresponding y values. 

	train_x : list of vectors
	train_y : vector of classifications
	x : vector we use to compare to other vectors within train_x
	'''

	length_train = len(train_x)
	dists = list()

	for i in range(len(train_x)):
		distance = dist(x, train_x[i])
		dists.append(distance)

	index_nearest = np.argpartition(dists, k)[:k]

	classification_sum = 0
	k_near = list()
	for elem in index_nearest:
		classification_sum += train_y[elem]

	if classification_sum >= 0:
		return 1
	elif classification_sum < 0:
		return -1


# Function to compare results of classify with expected outcome to compute accuracy
def runTest(test_x, test_y, train_x, train_y, k):
	correct = 0
	for (x,y) in zip(test_x, test_y):
		if classify(train_x, train_y, k, x) == y: # Compare call to classify with test_y
			correct += 1
	acc = float(correct)/len(test_x)
	return acc

#==================================================================#



#=========================Perceptron Model=========================#

# Learn weights using the perceptron algorithm
def train_perceptron(train_x, train_y, maxiter=100):
  # Initialize weight vector and bias
  '''
  Check whether or not a point is correctly classified
  If it is: 
    Do nothing
  If it is not: 
    Figure out which weight (wi) is affected it most and adjust by accordingly.


  '''
  numvars = len(train_x[0])
  numex = len(train_x)
  w = np.array([0.0] * numvars)
  b = 0.0

  for m in range(maxiter):
    for i in range(numex-1):
      a = np.dot(w, train_x[i]) + b #Compute activation

      a = a * train_y[i]
      # print(a)
      if a <= 0: # There is something wrong, we need to update. 

        # Iterate through w, add the product of xj and yj
        for j in range(numvars):
          update = np.dot(train_y[i], train_x[i][j])
          w[j] = w[j] + update

        b = b + train_y[i] # Update the bias
        
      # Else: No update needed (correct prediction)

  # print((w,b))
  return (w,b)

def predict_perceptron(model, x):
  (w,b) = model

  a = 0
  for i in range(len(x)):
    a += w[i]*x[i]

  a += b
  return a


#==================================================================#

# ============================Single Email============================
def predict_single(model, default, single):
	k = 6
	vec = extract_single(single, default)
	storage_matrix = read_matrix(default)

	#Run single knn
	if model == 1:
		prediction = classify(storage_matrix, train_y, k, vec)
	#Run single perceptron
	elif model == 2:
		(wa, ba) = read_wb(default)
		prediction = predict_perceptron( (wa,ba), vec)
		if prediction < 0:
			prediction = -1
		else:
			prediction = 1

	return prediction

#==================================================================#

#=================================Model============================#
# Type of model (1 = KNN, 2 = Perceptron), directory of training, directory of testing,
# Total numbers of files, total numbers of ham, single entry to be scanned
def model(model, default, training, testing, tot, ham):
	# File Paths for default datasets and file values
	if default:
		training = "./data/lingspam_public/bare/part7"
		testing = "./data/lingspam_public/bare/part10"
		tot = 289
		ham = 241


	# =============== Feature Extraction ==============
	# # Read data from training
	final_words_train = count_words(training)
	train_x = extract_features(training, final_words_train)
	
	# Read data from testing
	final_words_test = count_words(testing)
	test_x = extract_features(testing, final_words_test)

	store_dict(final_words_train, default) #Store the feature matrix in usrdata.txt
	store_matrix(train_x, default) # Store the feature matrix in usrmatrix.txt

	# Creating our labels, 1 indicates spam, -1 indicates ham
	train_y = np.zeros(tot)
	train_y[0:(ham-1)] = -1
	train_y[ham:(tot-1)] = 1

	# Creating our labels, 1 indicates spam, -1 indicates ham
	test_y = np.zeros(tot)
	test_y[0:(ham-1)] = -1
	test_y[ham:(tot-1)] = 1


	# ==================== Storage =============== =====
	#Store the feature matrix in data.txt if its the default dataset
	# and usrdata.txt if its the users inputed datasets
	store_dict(final_words_train, default) 
	new_words = read_dict(default)

	# Store the feature matrix in matrix.txt if default else usrmatrix.txt
	store_matrix(train_x, default) 
	new_matrix = read_matrix(default)

	# =================================================
		


	if model == 1:
		#===============================KNN==================================
		k = 15
		acc = runTest(test_x, test_y, train_x, train_y, k)
		return acc
		#====================================================================

	elif model == 2:

		#============================Perceptron==============================
		(w,b) = train_perceptron(train_x, train_y, 100)
		store_w(w, default)
		store_b(b, default)

		correct = 0
		for (x,y) in zip(test_x, test_y):
			activation = predict_perceptron( (w,b), x)
			if activation * y > 0:
				correct += 1
		acc = float(correct)/len(test_y)
		return acc

		#====================================================================


	else:
		print("Not a valid model (1 for KNN, 2 for Perceptron).")
		return -1,-1

#==================================================================#














