# NOTE: Normalization should be done on both the training data AND the test data the same way. 
import numpy as np

def rangenorm(train_x, test_x):
  '''
  Function which performs a feature range normalization:
  Feature range normalization should rescale instances to range from -1 
  (minimum) to +1 (maximum), according to values in the training data. 
  '''

  # Feature range normalization for train_x
  length_train = len(train_x)
  length_test = len(test_x)

  min_vals = train_x.min(0) #Returns list of all minimums per column
  denominator = train_x.max(0) #Returns list of all maximums per column
  min_len = len(min_vals)

  for i in range(min_len):
    denominator[i] = denominator[i]-min_vals[i]

  np.nan_to_num(0)
  for m in range(min_len):
    for n in range(length_train):
      if denominator[m] == 0:
        train_x[n][m] = 0
      else:
        train_x[n][m] = (train_x[n][m] - min_vals[m])/(denominator[m])
        train_x[n][m] = (train_x[n][m]*2) - 1
  

  # Feature range normalization for test_x
  min_vals_test = test_x.min(0) #Returns list of all minimums per column
  denominator_test = test_x.max(0) #Returns list of all maximums per column
  min_len_test = len(min_vals_test)

  for i in range(min_len_test):
    denominator_test[i] = denominator_test[i]-min_vals_test[i]

  for m in range(min_len_test):
    for n in range(length_test):
      if denominator_test[m] == 0:
        test_x[n][m] = 0
      else:
        test_x[n][m] = (test_x[n][m] - min_vals_test[m])/(denominator_test[m])
        test_x[n][m] = (test_x[n][m]*2) - 1

  return train_x, test_x

def varnorm(train_x, test_x):
  '''
  Function which performs a feature variant normalization on data.
  Feature variance normalization rescales instances so they 
  have a standard deviation of 1 in the training data. 
  '''
  length_train = len(train_x)
  length_test = len(test_x)
  mean_vals = np.mean(train_x, axis = 0)
  stdev_vals = np.std(train_x, axis = 0)
  length_mean = len(mean_vals)

  np.nan_to_num(0)
  for m in range(length_mean):
    for n in range(length_train):
      if stdev_vals[m] == 0:
        train_x[n][m] = 0
      else:
        train_x[n][m] = (train_x[n][m] - mean_vals[m])/(stdev_vals[m])

  mean_vals_test = np.mean(test_x, axis = 0)
  stdev_vals_test = np.std(test_x, axis = 0)
  length_mean = len(mean_vals_test)
  for m in range(length_mean):
    for n in range(length_test):
      if stdev_vals_test[m] == 0:
        test_x[n][m] = 0
      else:
        test_x[n][m] = (test_x[n][m] - mean_vals_test[m])/(stdev_vals_test[m])

  return train_x, test_x
          
def exnorm(train_x, test_x):
  '''
  Function which performs example magnitude normalization.
  Example magnitude normalization rescales each example 
  to have a magnitude of 1 (under a Euclidean norm).
  '''

  length_train = len(train_x)
  length_test = len(test_x)
  # print(train_x)

  for i in range(length_train):
    euc_norm = np.linalg.norm(train_x[i])
    train_x[i] = train_x[i]/euc_norm
    # print("magnitude =", np.linalg.norm(train_x[i]))

  for i in range(length_test):
    euc_norm = np.linalg.norm(test_x[i])
    test_x[i] = test_x[i]/euc_norm
    # print("magnitude =", np.linalg.norm(test_x[i]))

  return train_x, test_x

