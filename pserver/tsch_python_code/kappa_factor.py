#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os,sys,  getopt, getpass
import os.path, time

import numpy as np

def kappa_factor(trace_x, trace_y):
  kappa = 0.0

  if len(trace_x)  != len(trace_y):
      M=np.min(len(trace_x), len(trace_y))
      trace_x = trace_x[1:M]
      trace_y = trace_y[1:M]

  trace_xy = np.multiply(trace_x, trace_y)

  Px = np.mean(trace_x)
  Py = np.mean(trace_y)
  Pxy= np.mean(trace_xy)


  sigma_x = np.sqrt(Px*(1-Px))
  sigma_y = np.sqrt(Py*(1-Py))
   
  rho_txy = 0.0
  rho_max = 0.0
  rho_min = 0.0

  if sigma_x*sigma_y != 0:
        rho_txy = (Pxy -Px*Py)/np.sqrt(sigma_x*sigma_y)
        rho_max = (np.min(Px, Py) - Px*Py)/np.sqrt(sigma_x*sigma_y)

        if np.add(Px, Py) <= 1:
            rho_min = (-1.0*(Px * Py))/np.sqrt(sigma_x*sigma_y)
        else:
            rho_min = (Px + Py - 1.0 - Px*Py)/np.sqrt(sigma_x*sigma_y)

  else:
      rho_txy = 0

  if rho_txy > 0:
      kappa = 1.0*rho_txy/rho_max
  elif rho_txy < 0:
      kappa = -1.0*(rho_txy/rho_min)

  return kappa


def kappa_factor_frequency(data, no_channels):

    n_chs = no_channels
    kappa      = np.zeros((1, no_channels-1))
    prob_xy    = np.zeros((1, no_channels-1))
    prob_xy_ctr= np.zeros((1, no_channels-1), int)
    prob_ch    = np.zeros((1, no_channels))
    sigma_ch   = np.zeros((1, no_channels))

    ch_mat = np.resize(data, (len(data)/no_channels + len(data)%no_channels, no_channels)).T
    #ch_mat = ch_mat.T

    #compute the probabilities per channel    
    for idx in range(0, len(ch_mat)):
        prob_ch[0][idx] = np.mean(ch_mat[idx])
        sigma_ch[0][idx]= np.sqrt(prob_ch[0][idx]*(1.0-prob_ch[0][idx]))
        #for n in range(idx+1, len(ch_mat)):
            #kappa[0][idx]= kappa_factor(ch_mat[idx], ch_mat[n])

    #return kappa[0]
    #compute the cross probabilities event counter:
    lenPxy = len(prob_xy_ctr[0])
    for n in range(0, len(data)-1):
        if int(data[n]) == 1 and  int(data[n+1]) == 1:
            prob_xy_ctr[0][n%lenPxy] = prob_xy_ctr[0][n%lenPxy] + 1
    
    #compute the corss probability: pxy
    for n in range(0, len(prob_xy_ctr)):
        prob_xy[0][n] = float(prob_xy_ctr[0][n])/(len(data)/no_channels)
        #prob_xy[0][n] = float(prob_xy_ctr[0][n])/(len(data))


    for n in range(0, len(prob_xy)):
        pxy = prob_xy[0][n]
        px  = prob_ch[0][n]
        py  = prob_ch[0][n+1]
        sigma_xy = sigma_ch[0][n]*sigma_ch[0][n+1]

        if sigma_xy != 0:
            rho_xy  = (pxy - px*py)/sigma_xy
            rho_max = (np.min(px, py) - px*py)/sigma_xy
            rho_min = 0.0

            if (px + py) <= 1.0:
                rho_min = -1.0*px*py/sigma_xy
            else:
                rho_min = (px+py-1-px*py)/sigma_xy

            if rho_xy >0:
                kappa[0][n] = rho_xy/rho_max
            if rho_xy < 0:
                kappa[0][n] = -1.0*rho_xy/rho_min
            if rho_xy == 0:
                kappa[0][n] = 0.0
        else:
            kappa[0][n] = 0
   
    return kappa[0]