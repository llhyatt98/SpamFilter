from collections import Counter
import os
import numpy as np

#====================================================================
#========================== FREQUENCY DICT ==========================
#====================================================================

def count_words(directory):
	emails = [os.path.join(directory,file) for file in os.listdir(directory)] 
	track_words = []
	for email in emails:
		with open(email, encoding="latin-1") as email:
			for line in email:
				words = line.split() # Create list of words on a line
				track_words += words # Add each word to total count

	count_words = Counter(track_words) # Count frequency of each word

	# This portion removes unwanted features:
	# meaningless words, non-alphabetic characters...
	words = list(count_words.keys())

	for elem in words:
		if len(elem) == 1 or len(elem) == 2: # Remove stop words.
			del count_words[elem]
		if elem.isalpha() == False: # Remove non-alphabetical words.
			del count_words[elem]

	count_words = count_words.most_common(3000) # Take the most common 3000 words
	
	# print(count_words)
	return count_words

#====================================================================
#=========================== DATA STORAGE ===========================
#====================================================================

def store_matrix(feature_matrix, default):
	# Stores the feature_matrix to the data.txt file
	#Checks which file to store in
	fl = 'storage/matrix.txt'
	if not default:
		fl = 'storage/usrmatrix.txt'

	with open(fl, 'w') as file:
		for row in feature_matrix:
			length = len(row)
			for i in range(length):
				if i == 0:
					file.write(str(row[i]))
				else:
					file.write(' ')
					file.write(str(row[i]))
			file.write("\n")

def store_dict(dictionary, default): # Stores the dictionary inside of data.txt in storage
	#checks which file to store in
	fl = 'storage/data.txt'
	if not default:
		fl = 'storage/usrdata.txt'

	with open(fl, 'w') as file:
		i = 0
		for word,freq in dictionary:
			i += 1
			if i == 3000:
				file.write(str(word))
				break

			file.write(str(word))
			file.write("\n")

def store_w(w, default): # Stores the dictionary inside of data.txt in storage
	#checks which file to store in
	fl = 'storage/weight.txt'
	if not default:
		fl = 'storage/usrweight.txt'
	# f = open(fl,'w') #open a file in write mode
	np.savetxt(fl, w)
	# f.close() #close the file

def store_b(b, default): # Stores the dictionary inside of data.txt in storage
	#checks which file to store in
	fl = 'storage/bias.txt'
	if not default:
		fl = 'storage/usrbias.txt'
	f = open(fl,'w') #open a file in write mode
	f.write(str(b)) #str(b)
	# np.savetxt(fl, dictionary[1])
	f.close() #close the file

def read_matrix(default):
	# Reads the feature_matrix from the data.txt file
	count = 0
	#checks which file to read in
	fl = 'storage/matrix.txt'
	if not default:
		fl = 'storage/usrmatrix.txt'

	file = open(fl, 'r')
	for line in file: # Determine how many emails (rows of matrix) there are
		count += 1

	# print(count)
	features_matrix = np.zeros((count, 3000))

	with open(fl, 'r') as file:
		count = 0
		for row in file:
			i = 0
			test = row.split(" ")
			# print(test)
			for item in test:
				features_matrix[count][i] = float(item)
				i += 1 
			count += 1

	return features_matrix

def read_dict(default):
	#Checks which .txt to open
	fl = 'storage/data.txt'
	if not default:
		fl = 'storage/usrdata.txt'

	with open(fl, 'r') as file:
		words = ['' for i in range(3000)]
		i = 0
		for line in file:
			if i == 2999: # Last line doesn't have a newline
				words[i] = line
				break

			words[i] = line[0:-1]
			i += 1

	return words

 # Reads the weights inside of (usr)weight.txt in storage
def read_wb(default):
	#checks which file to store in
	fl = 'storage/weight.txt'
	fl2 = 'storage/bias.txt'
	if not default:
		fl = 'storage/usrweight.txt'
		fl2 = 'storage/usrbias.txt'

	w = np.loadtxt(fl, float)
	f = open(fl2,'r') #open a file in read mode
	b = f.readline()
	b = float(b)
	f.close() #close the file
	# f.close() #close the file
	return (w,b)


#====================================================================
#==========================FEATURE MATRIX============================
#====================================================================

def extract_features(directory, dictionary):
	'''
	directory: where to find the data
	dictionary: 300 most common words within the directory
	toStore: used for storage, only store the matrix for training (no need to store for testing)
	'''
	files_list = [os.path.join(directory,file) for file in os.listdir(directory)]
	files = sorted(files_list)

	files = files[1:] # Get rid of .DS_Store file at the beginning (after sorted)
	# print(files)

	# Create the matrix to store the features
	features_matrix = np.zeros((len(files), 3000))
	# print(features_matrix)

	docID = 0
	# traceback = [] #This is used to correlate words for the feedback

	for emails in files:
		# print(emails)
		with open(emails, encoding="latin-1") as email:
			for line in email:
				words = line.split() # Create list of words on a line
				for word in words:
					wordID = 0
					for i,d in enumerate(dictionary): # Here i is the index and d is the word
						if d[0] == word: # d[0] is the word, d[1] is the frequency.
							wordID = i
							# traceback[i] = d[0]
							features_matrix[docID, wordID] = 1 # Set the occurrence of that word.
							# features_matrix[docID, wordID] = word.count(word) # Original sets the frequency

			docID += 1 #Increment the index to indicate which email we are at.
	
	return features_matrix

# Function to test a single email against a feature matrix
def extract_single(file, default):

	# Create the matrix to store the features
	# feature_matrix = read_matrix()
	dictionary = read_dict(default)
	
	'''
	Vector specific to the email
	Populate this based on dictionary
	Compare it to the feature matrix. 
	'''
	features_vector = np.zeros(3000)


	with open(file, encoding="latin-1") as email:
		for line in email:
			words = line.split() # Create list of words on a line
			for word in words:
				wordID = 0
				for i,d in enumerate(dictionary): # Here i is the index and d is the word
					if d == word: # d[0] is the word, d[1] is the frequency.
						wordID = i
						features_vector[wordID] = 1 # Set the occurrence of that word.

	# print(features_vector)
	return features_vector # Singular feature vector for email. 


'''
Sources: 

https://www.kdnuggets.com/2017/03/email-spam-filtering-an-implementation-with-python-and-scikit-learn.html

'''















