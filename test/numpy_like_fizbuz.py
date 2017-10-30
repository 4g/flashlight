##########################################################################
##########################################################################
# Author: Sherin Thomas
# PyTorch Version 0.2
# Program for predicting the next number whether its a
# fiz or buz or fizbuz
# The original post written the idea of fizbuz in neural network:
#       http://joelgrus.com/2016/05/23/fizz-buzz-in-tensorflow/
#
#
#
# incase you haven't played this game, you had the worst childhood,
# but don't worry, here are the rules.
#
# number divisible by 3 is fiz
# number divisible by 5 is buz
# number divisible by both 3 and 5 is fizbuz
# other numbers should be considered as that number itself
###########################################################################
###########################################################################

import torch
from torch.autograd import Variable

from dataset import get_data, decoder, check_fizbuz


input_size = 10
epochs = 2000
batches = 64
lr = 0.01


trX, trY, teX, teY = get_data(input_size)
if torch.cuda.is_available():
    dtype = torch.cuda.FloatTensor
else:
    dtype = torch.FloatTensor
x = Variable(torch.from_numpy(trX).type(dtype), requires_grad=False)
y = Variable(torch.from_numpy(trY).type(dtype), requires_grad=False)

w1 = Variable(torch.randn(10, 100).type(dtype), requires_grad=True)
w2 = Variable(torch.randn(100, 4).type(dtype), requires_grad=True)

b1 = Variable(torch.zeros(1, 100).type(dtype), requires_grad=True)
b2 = Variable(torch.zeros(1, 4).type(dtype), requires_grad=True)

no_of_batches = int(len(trX) / batches)
for epoch in range(epochs):
    for batch in range(no_of_batches):
        start = batch * batches
        end = start + batches
        x_ = x[start:end]
        y_ = y[start:end]

        a2 = x_.matmul(w1)
        a2 = a2.add(b1)
        h2 = a2.sigmoid()

        a3 = h2.matmul(w2)
        a3 = a3.add(b2)
        hyp = a3.sigmoid()

        error = hyp - y_
        output = error.pow(2).sum() / 2.0
        output.backward()

        w1.data -= lr * w1.grad.data
        w2.data -= lr * w2.grad.data
        b1.data -= lr * b1.grad.data
        b2.data -= lr * b2.grad.data
        w1.grad.data.zero_()
        w2.grad.data.zero_()
        b1.grad.data.zero_()
        b2.grad.data.zero_()
    if epoch % 10:
        print(epoch, output.data[0])


# test
x = Variable(torch.from_numpy(teX).type(dtype), volatile=True)
y = Variable(torch.from_numpy(teY).type(dtype), volatile=True)

a2 = x.matmul(w1)
a2 = a2.add(b1)
h2 = a2.sigmoid()

a3 = h2.matmul(w2)
a3 = a3.add(b2)
hyp = a3.sigmoid()
error = hyp - y
output = error.pow(2).sum() / 2.
outli = ['fizbuz', 'buz', 'fiz', 'number']
for i in range(len(teX)):
    num = decoder(teX[i])
    print(
        'Number: {} -- Actual: {} -- Prediction: {}'.format(
            num, check_fizbuz(num), outli[hyp[i].data.max(0)[1][0]]))
print('Test loss: ', output.data[0] / len(x))
accuracy = hyp.data.max(1)[1] == y.data.max(1)[1]
print('accuracy: ', accuracy.sum() / len(accuracy))
