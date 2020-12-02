import matplotlib.pyplot as plt
import numpy as np
import time

fig = plt.figure()
ax = fig.add_subplot(111)
line, = plt.plot([], [])

x_lim = 10
y_lim = 10

ax.set_xlim([0, x_lim])
ax.set_ylim([0, y_lim])

X = np.array([])
y = np.array([])

iterations = 500
alpha = 0.01


def onClick(event):
    global X, y, line
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))

    X = np.append(X, event.xdata).reshape(X.shape[0]+1, 1)
    m = X.shape[0]
    X_c = np.copy(X)
    X_c = np.append(np.ones(m).reshape(m, 1), X_c, axis=1)
    y = np.append(y, event.ydata).reshape(y.shape[0]+1, 1)

    theta = np.zeros(X_c.shape[1])

    plt.plot(event.xdata, event.ydata, '.', ms=10, color='blue')
    fig.canvas.draw()

    if (X.size > 1):
        for i in range(0, iterations):
            theta = gradientDescentStep(X_c, y, theta)
            print(theta)
            #y = b + ax
            b = theta[0]
            a = theta[1]
            line.set_data([0, x_lim], [b, b+x_lim*a])
            fig.canvas.draw() 
            plt.pause(.0001)
    else:
        pass

def gradientDescentStep(X, y, theta):
    m = X.shape[0]
    theta = theta - (alpha/m)*sum(np.dot(np.dot(X, theta)-y, X))

    return theta

cid = fig.canvas.mpl_connect('button_press_event', onClick)
plt.show()