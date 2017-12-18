#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This is an example implementation of ALS for learning how to use Spark. Please refer to
pyspark.ml.recommendation.ALS for more conventional use.

This example requires numpy (http://www.numpy.org/)
"""
from __future__ import print_function

import sys

import numpy as np
from numpy.random import rand
from numpy import matrix
from pyspark.sql import SparkSession

LAMBDA = 0.01   # regularization
np.random.seed(42)


def rmse(R, ms, us):
    diff = R - ms * us.T
    return np.sqrt(np.sum(np.power(diff, 2)) / (N * M))


def update(i, mat, ratings):
    uu = mat.shape[0]
    ff = mat.shape[1]

    XtX = mat.T * mat
    Xty = mat.T * ratings[i, :].T

    for j in range(ff):
        XtX[j, j] += LAMBDA * uu

    return np.linalg.solve(XtX, Xty)

N = int(sys.argv[2])
M = int(sys.argv[3])
F = int(sys.argv[4]) 

if __name__ == "__main__":

    """
    Usage: als [M] [U] [F] [iterations] [partitions]"
    """

    spark = SparkSession\
        .builder\
        .appName("PythonALS")\
        .getOrCreate()

    sc = spark.sparkContext

    file = open(sys.argv[1], 'r')
    matrixM = np.zeros((N,M), dtype=np.int)

    for line in file.readlines(): #reading input file and storing into matrix using numpy
        temp = line.strip().split(',')
        row = int(temp[0]) - 1 
        col = int(temp[1]) - 1
        matrixM[row, col] = temp[2]
    file.close()

    N = int(sys.argv[2]) #M changed to N
    M = int(sys.argv[3]) #U changed to M
    F = int(sys.argv[4]) 
    ITERATIONS = int(sys.argv[5]) 
    partitions = int(sys.argv[6])
    outputFile = sys.argv[7] 

    R = matrix(rand(N, F)) * matrix(rand(M, F).T)
    R = matrix(matrixM)

    ms = matrix(rand(N, F)) #ms is U
    us = matrix(rand(M, F)) #us is V

    matU = np.ones((N, F), dtype=np.float)  #U is of size n x f filled with 1's
    matV = np.ones((M, F), dtype=np.float)  #V is of size f x m filled with 1's
    
    ms = matrix(matU)
    us = matrix(matV)

    Rb = sc.broadcast(R)
    msb = sc.broadcast(ms)
    usb = sc.broadcast(us)
    
    writing = open(outputFile, 'w')
    for i in range(ITERATIONS):
        ms = sc.parallelize(range(N), partitions) \
               .map(lambda x: update(x, usb.value, Rb.value)) \
               .collect()
        # collect() returns a list, so array ends up being
        # a 3-d array, we take the first 2 dims for the matrix
        ms = matrix(np.array(ms)[:, :, 0])
        msb = sc.broadcast(ms)

        us = sc.parallelize(range(M), partitions) \
               .map(lambda x: update(x, msb.value, Rb.value.T)) \
               .collect()
        us = matrix(np.array(us)[:, :, 0])
        usb = sc.broadcast(us)

        error = rmse(R, ms, us)
        #print("RMSE: %5.4f" % error)
        writing.write("%.4f\n" % error)
    writing.close()
    spark.stop()
