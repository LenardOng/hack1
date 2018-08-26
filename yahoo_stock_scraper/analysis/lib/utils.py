import numpy as np

def dist(x,y):
    z = np.square(np.subtract(x, np.transpose(y)))
    return z


def cov_tut(x, y):
    cov = np.exp(np.multiply((-1. / 2.), dist(x, y)))
    return cov


def cov_matern(x_dat, y_pred, l=1, w=1):
    cov = np.square(l)*np.exp(np.multiply(-1/w, dist(x_dat, y_pred)))
    return cov


def cov_periodic(x_dat, y_pred, rho=100, w=1):
    cov = np.exp(np.multiply(-2/w, np.square(np.sin(np.multiply(np.pi/rho, dist(x_dat, y_pred))))))
    return cov


def cov_combined(x_dat, y_pred):
    cov = cov_periodic(x_dat, y_pred) + cov_matern(x_dat, y_pred)
    return cov


def pred_mu(x_pred, x_dat, y_dat, mu_dat, inv_cov_dat, cov):
    k_s_d = cov(x_pred, x_dat)
    mu_pred = mu_dat + np.matmul(k_s_d, (np.matmul(inv_cov_dat, y_dat)))
    return mu_pred


def pred_var(x_pred, x_dat, inv_cov_dat, cov):
    k_s = cov(x_pred, x_pred)
    k_s_d = cov(x_pred, x_dat)
    k_pred = k_s - np.matmul(k_s_d, np.matmul(inv_cov_dat, np.transpose(k_s_d)))
    return k_pred


def calc_data_cov(x_dat, cov):
    x_arr = np.tile(x_dat, (len(x_dat), 1))
    k = cov(x_arr, x_arr)
    inv_k = np.linalg.inv(k)
    return k, inv_k