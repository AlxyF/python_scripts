import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111)
line, = plt.plot([], [])

x_lim = 10
y_lim = 10

ax.set_xlim([0, x_lim])
ax.set_ylim([0, y_lim])

X = np.array([])
y = np.array([])

def onClick(event):
    global X, y, line
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))

    X = np.append(X, event.xdata).reshape(X.shape[0]+1,1)
    m = X.shape[0]
    X_c = np.copy(X)
    X_c = np.append(np.ones(m).reshape(m,1),X_c, axis=1)
    y = np.append(y, event.ydata).reshape(y.shape[0]+1,1)
    
    if (X.size > 1):
        theta = normalEqn(X_c,y)
        print(theta)
        #y = b + ax
        b = theta[0][0]
        a = theta[1][0]
        line.set_data([0,x_lim], [b, b+x_lim*a])
    else:
        pass

    plt.plot(event.xdata, event.ydata, '.', ms=10, color='blue')
    fig.canvas.draw()
    
def normalEqn(X, y):
    theta = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X),X)),np.transpose(X)),y)
    return theta


cid = fig.canvas.mpl_connect('button_press_event', onClick)
plt.show()