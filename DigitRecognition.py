import numpy as np
import pandas as pd

data = pd.read_csv('train.csv')
data.head()

data = np.array(data)
m, n = data.shape
np.random.shuffle(data) # shuffle before splitting into dev and training sets

dataDev = data[0:1000].T
yDev = dataDev[0]
XDev = dataDev[1:n]
XDev = XDev / 255.

dataTrain = data[1000:m].T
yTrain = dataTrain[0]
XTrain = dataTrain[1:n]
XTrain = XTrain / 255.

def init():
    w1 = np.random.rand(10, 784) - 0.5
    w2 = np.random.rand(10, 10) - 0.5
    b1 = np.random.rand(10, 1) - 0.5
    b2 = np.random.rand(10, 1) - 0.5
    return w1, w2, b1, b2

def RelU(z):
    return np.maximum(z, 0)

def softmax(z):
    a = np.exp(z) / sum(np.exp(z))
    return a
    
def forward(w1, w2, b1, b2, X):
    z1 = w1.dot(X) + b1
    a1 = RelU(z1)
    z2 = w2.dot(a1) + b2
    a2 = softmax(z2)
    return z1, z2, a1, a2

def RelUDerivative(z):
    return z > 0

def oneHot(Y):
    oneHotY = np.zeros((Y.size, Y.max() + 1))
    oneHotY[np.arange(Y.size), Y] = 1
    oneHotY = oneHotY.T
    return oneHotY

def backwardProp(z1, z2, a1, a2, w1, w2, X, Y):
    oneHotY = oneHot(Y)
    dz2 = a2 - oneHotY
    dw2 = 1 / m * dz2.dot(a1.T)
    db2 = 1 / m * np.sum(dz2)
    dz1 = w2.T.dot(dz2) * RelUDerivative(z1)
    dw1 = 1 / m * dz1.dot(X.T)
    db1 = 1 / m * np.sum(dz1)
    return dw1, dw2, db1, db2

def updateParams(w1, b1, w2, b2, dw1, db1, dw2, db2, learningRate):
    w1 -= learningRate * dw1
    w2 -= learningRate * dw2  
    b1 -= learningRate * db1    
    b2 -= learningRate * db2    

    return w1, w2, b1, b2

def Predictions(a2):
    return np.argmax(a2, 0)

def Accuracy(predictions, Y):
    print(predictions, Y)
    return np.sum(predictions == Y) / Y.size

def gradientDescent(X, Y, learningRate, iterations):
    w1, w2, b1, b2 = init()
    for i in range(iterations):
        z1, z2, a1, a2 = forward(w1, w2, b1, b2, X)
        dw1, dw2, db1, db2 = backwardProp(z1, z2, a1, a2, w1, w2, X, Y)
        w1, w2, b1, b2 = updateParams(w1, b1, w2, b2, dw1, db1, dw2, db2, learningRate)
        if i % 50 == 0:
            print("Iteration: ", i)
            predictions = Predictions(a2)
            print(Accuracy(predictions, Y))
    return w1, w2, b1, b2

w1, w2, b1, b2 = gradientDescent(XTrain, yTrain, 0.10, 250)
