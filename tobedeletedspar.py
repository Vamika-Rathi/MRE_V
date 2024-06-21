#!/usr/bin/env python1
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 14:39:12 2024

@author: cvr6133
"""
import numpy as np
import scipy.sparse as sp



def alpha_jn(j, n):
      if n == 0:
          alpha   = 0.0
      elif j == 0:
          alpha   = 4.0 / 3.0
      elif j != n:
          alpha   = ((j - 1.0)**1.5 + (j + 1.0)**1.5 - 2.0 * j**1.5) * 4.0 / 3.0
      else:
          alpha   = ((n - 1.0)**1.5 - n**1.5 + np.sqrt(n)*3.0/2.0) * 4.0/3.0
      return alpha

def alpha_v(N):
    AlphaSubst_v = np.array([])
    for j in range(0, N+1):
        AlphaSubst_v = np.append(AlphaSubst_v,
                                 alpha_jn(j+1, N+1) - alpha_jn(j, N))
    return AlphaSubst_v

def calc_alpha_mat(N):
    for nn in range(0, N-1):
        if nn == 0:
            alpha_mat = sp.csr_matrix(alpha_v(nn), shape=(1, N))
        else:
            alpha_v1 = sp.csr_matrix(alpha_v(nn), shape=(1, N))
            alpha_mat = sp.vstack([alpha_mat, alpha_v1])
    return alpha_mat

R = 0.75
S = 0.3 
h = 0.001
xi = R*np.sqrt(3*h/(np.pi*S))
w1 = 0
w2 = 0
x = 1
y = 0
t_fin = 10
omega = 1

w1_h = 0
w2_h = 0
x_h = 1
y_h = 0

W1_history = [w1_h]
W2_history = [w2_h]
X_history = [x_h]
Y_history = [y_h]

W1 = [w1]
W2 = [w2]
X = [x]
Y = [y]

t_range = np.arange(0, t_fin, h)
N = len(t_range)
for n in range(0, N+1):
    
    
    G1 = ((R-1)*(omega*x_h) - w2_h)*(-omega) - (R/S)*w1_h
    G2 = ((R-1)*(-omega*y_h) - w1_h)*(omega) - (R/S)*w2_h
    
    sum_alpha1  =     np.dot(calc_alpha_mat(n).toarray()[n, :n+1], W1_history)
            
    sum_alpha2  =     np.dot(calc_alpha_mat(n).toarray()[n, :n+1], W2_history)
    
    x_h = x_h + h*(w1_h + (-omega*y_h))
    y_h = y_h + h*(w2_h + (omega*x_h))
    
    X_history.append(x_h)
    Y_history.append(y_h)
    
    w1_h = (w1_h + h*G1 - xi*sum_alpha1)/(1+xi*4/3)
    w2_h = (w2_h + h*G2 - xi*sum_alpha2)/(1+xi*4/3)
    
    W1_history.append(w1_h)
    W2_history.append(w2_h)

print()