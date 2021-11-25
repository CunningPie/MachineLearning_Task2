from typing import Tuple
from scipy.sparse.csr import csr_matrix
import Config
from scipy import sparse
import numpy as np
import time
import os


def mse(y, y_pred):
    l, _ = y.shape
    return np.sum(np.square(y - y_pred)) / l


def rmse(y, y_pred):
    return np.sqrt(mse(y, y_pred))


def r2(y, y_pred):
    return 1 - (np.sum(np.square(y - y_pred))) / (np.sum(np.square(y - y.mean())))


def prediction(X, w, V):
    return X.dot(w) + 0.5 * (np.sum(np.square(X.dot(V)), axis=1).reshape(-1, 1) -
                             np.sum(X.power(2).dot(np.square(V)), axis=1).reshape(-1, 1))


def step(X: csr_matrix, Y: csr_matrix, w: np.ndarray, V: np.ndarray, rate=0.0001) -> Tuple[np.ndarray, np.ndarray]:
    l, _ = X.shape
    XT = X.copy().transpose()

    p = prediction(X, w, V)
    err = Y - p
    w += ((2 * rate) / l) * XT.dot(err)

    precmp = X.dot(V)
    V += ((2 * rate) / l) * (XT.dot(np.multiply(err, precmp)) - np.multiply(V, (XT).power(2).dot(err)))

    return w, V


def gradient_descent(X, y, w, V, rate=1e-2, mse_bound=1.5) -> Tuple[np.ndarray, np.ndarray, float]:
    w_next, v_next = step(X, y, w, V, rate)
    y_pred = prediction(X, w_next, v_next)
    w = w_next
    V = v_next
    MSE = mse(y, y_pred)
    while (MSE > mse_bound):
        w_next, v_next = step(X, y, w, V, rate)
        y_pred = prediction(X, w_next, v_next)
        w = w_next
        V = v_next
        MSE = mse(y, y_pred)
        print(MSE)

    return w, V, mse


m = 0
test_mse = []
for path in Config.csr_paths:
    w_path, V_path = Config.predict_paths[m]
    print(w_path)
    data: csr_matrix = sparse.load_npz('{0}.npz'.format(path))
    r, c = data.shape
    Y: csr_matrix = data[:, c - 1]
    X: csr_matrix = data[:, : c - 1]
    r, c = X.shape
    V: np.ndarray = np.full((c, Config.k), Config.V_default)
    w = np.full((c, 1), Config.V_default)
    start_time = time.time()
    w, V, mse = gradient_descent(X, Y, w, V)
    end_time = time.time()
    print("--- %s seconds ---" % (end_time - start_time))
    test_mse.append(mse)
    print(mse)
    np.save(w_path, w)
    np.save(V_path, V)
    m += 1

with open(os.path.join(Config.predict_dir, 'train_mse.txt'), 'w') as f:
    k = 0
    for i in test_mse:
        f.write('Dataset {0} {1}'.format(k, i))
        k += 1
