import sys 
import numpy as np

matrixFile = sys.argv[1]
n = int(sys.argv[2]) #number of rows. users 
m = int(sys.argv[3]) #number of columns. products
f = int(sys.argv[4]) #number of dimensions/factors 
k = int(sys.argv[5]) #number of iterations 

def calcRSME(matU, matV):
	matMprime = np.dot(matU, matV) 			#M' is UV multiplied
	matInt = np.subtract(matrix, matMprime) #intermediary matrix 
	rows, cols = np.where(matrix == 0) #finding where there are 0s in the original matrix
	for i in range(0, len(rows)):
		matInt[rows[i], cols[i]] = 0 #putting 0s back in the intemediary matrix
	totSquaredErr = 0
	for arr in matInt:
		for items in arr:
			totSquaredErr = totSquaredErr + items ** (2)
	nonBlankEntries = (n * m) - len(rows)
	RSME = (float(totSquaredErr)/nonBlankEntries) ** (0.5)
	print "%.4f" % RSME

def calcMatU(matrix, matU, matV):
	denominator = 0
	mySum = 0
	innerCalc = 0
	numerator = 0

	for r in range(0, n):
		for s in range(0, f):
			innerCalc = 0 
			numerator = 0
			denominator = 0
			for j in range(0, m):
				if matrix[r][j] != 0:
					for k in range(0, f):
						if k != s:
							mySum = mySum + (matU[r][k] * matV[k][j])
					innerCalc = matrix[r][j] - mySum
					numerator = numerator + (matV[s][j] * innerCalc)
					denominator = denominator + matV[s][j] ** (2)
					mySum = 0
				matU[r][s] = float(numerator) / denominator

def calcMatV(matrix, matU, matV):
	denominator = 0
	mySum = 0
	innerCalc = 0
	numerator = 0

	for r in range(0, f):
		for s in range(0, m):
			innerCalc = 0 
			numerator = 0
			denominator = 0
			for i in range(0, n):
				if matrix[i][s] != 0:
					for k in range(0, f):
						if k != r:
							mySum = mySum + (matU[i][k] * matV[k][s])
					innerCalc = matrix[i][s] - mySum
					numerator = numerator + (matU[i][r] * innerCalc)
					denominator = denominator + matU[i][r] ** (2)
					mySum = 0
				matV[r][s] = float(numerator) / denominator


file = open(matrixFile, 'r')
matrix = np.zeros((n,m), dtype=np.int)

for line in file.readlines(): #reading input file and storing into matrix using numpy
	temp = line.strip().split(',')
	row = int(temp[0]) - 1 
	col = int(temp[1]) - 1
	matrix[row, col] = temp[2]
file.close()

matU = np.ones((n, f), dtype=np.float)	#U is of size n x f filled with 1's
matV = np.ones((f, m), dtype=np.float)	#V is of size f x m filled with 1's

for i in range(0, k):
	calcMatU(matrix, matU, matV)
	calcMatV(matrix, matU, matV)
	calcRSME(matU, matV)


   



