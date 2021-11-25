import Config
import FM
import numpy as np
from scipy import sparse
from scipy.sparse.csr import csr_matrix

data1: csr_matrix = sparse.load_npz('{0}.npz'.format(Config.csr_paths[0]))
data2: csr_matrix = sparse.load_npz('{0}.npz'.format(Config.csr_paths[1]))
data3: csr_matrix = sparse.load_npz('{0}.npz'.format(Config.csr_paths[2]))
data4: csr_matrix = sparse.load_npz('{0}.npz'.format(Config.csr_paths[3]))
r, c = data1.shape

Y1 = data1[:, c - 1]
Y2 = data2[:, c - 1]
Y3 = data3[:, c - 1]
Y4 = data4[:, c - 1]

X1 = data1[:, : c - 1]
X2 = data2[:, : c - 1]
X3 = data3[:, : c - 1]
X4 = data4[:, : c - 1]

X = [X1, X2, X3, X4]
Y = [Y1, Y2, Y3, Y4]

m = 0
for w_path, V_path in Config.predict_paths:
    V = np.load('{0}.npy'.format(V_path))
    w = np.load('{0}.npy'.format(w_path))
    predictions = []
    print('Train Fold {0}'.format(m))

    for j in range(len(Config.predict_paths)):
        if m != j:
            print('Test fold {0}'.format(j))
            a = FM.prediction(X[j], w, V)
            b = Y[j]
            print('RMSE', FM.rmse(a, b))
    m += 1
