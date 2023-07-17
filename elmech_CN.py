#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 15:52:02 2023
# integrazione nel tempo equazioni modello elettro-meccanico
# con equazioni di stato e metodo di Crank Nicolson
# riferimento documento model.pdf
@author: mauriziorepetto
"""

# libraries
# ---------
import numpy as np
import csv
import matplotlib.pyplot as plt
plt.ion()
#
# dati circuito magnetico
mu0=4*np.pi*1e-7
# parametri circuito magnetico
S=10*1e-4 #sezione 10 cm2
N=1000    #numero spire
Rt=1.88  #resistenza avvolgimento
# generatore
V_g=10.0
# parametri circuito meccanico
k_e=10000 #costante elastica molla
m=2 # massa parte mobile
c_v=5e-1 #coefficiente attrito viscoso
# dati  asse temporale
# ipwm=0 => tensione continua V_g
# ipwm=1 => tensione pwm con ampiezza V_g periodo 1/fsw, duty d
ipwm=1
if(ipwm==0):
    t_ini=0.0
    t_fin=1.0
    Nist=1000
    time=np.linspace(t_ini,t_fin,Nist)
    Deltat=time[1]-time[0]
    e_s=V_g*np.ones(Nist)
if(ipwm==1):
    t_ini=0
    fsw=50
    Nper=100
    Nptper=20
    d=0.25
    Nist=Nper*Nptper
    time=np.linspace(t_ini,Nper/fsw,Nist)
    Deltat=time[1]-time[0]
    vpwm=np.zeros(Nist)
    for k in range(Nper):
        for kk in range(Nptper):
            if(kk/Nptper<d):
                vpwm[k*Nptper+kk]=1
            else:
                vpwm[k*Nptper+kk]=0
    e_s=V_g*vpwm
    #
    hf0 = plt.figure()
    q1=plt.plot(time, e_s, '-r')
    plt.xlabel('time, s', fontsize=14)
    plt.ylabel('e_s, m', fontsize=14)
    plt.grid(True)
    plt.title('tensione pwm')
#
#
x=np.zeros((3,Nist))
A=np.zeros((3,3))
B=np.zeros((3,3))
M1=np.zeros((3,3))
M1inv=np.zeros((3,3))
M2=np.zeros((3,3))
u=np.zeros((3,Nist))
xpos=np.zeros(Nist)
#
# initial conditions
x[0,0]=0 #i
x[1,0]=0 #xdot
x[2,0]=0 #fe
#
xpos[0]=2e-2 #posizione iniziale traferro
G=N**2*mu0*S
# array di lavoro
xdum=np.zeros(3)
xnew=np.zeros(3)
fdum=np.zeros(3)
fnew=np.zeros(3)
#
chk=np.zeros(Nist)
xmin=1e-4 #minima x
#
for itime in range(1,Nist):
    # calcolo matrice A
    A[0,0]=G/2/xpos[itime-1]
    A[1,1]=m
    A[2,2]=1/k_e
#    A[1,1]=1
#    A[2,2]=1
    # calcolo matrice B
    B[0,0]=Rt
    B[0,1]=-G*x[0,itime-1]/2/xpos[itime-1]**2
    B[1,0]=G*x[0,itime-1]/2/xpos[itime-1]**2
    B[1,1]=1/c_v
    B[1,2]=-1
    B[2,1]=1
    # calcolo termine noto u
    u[0,itime]=e_s[itime]
    u[1,itime]=0.25*G*x[0,itime-1]**2/xpos[itime-1]**2
    #
 
    #calcolo matrici M1 e M2
    M1=A/Deltat+B/2
    M2=A/Deltat-B/2
    M1inv=np.linalg.inv(M1)
    xdum=x[:,itime-1]
    fdum=0.5*(u[:,itime-1]+u[:,itime])
    xnew=np.matmul(M1inv,np.matmul(M2,xdum)+fdum)
    x[:,itime]=xnew
#    print('xnew',xnew)
    #integra posizione da velocita'
    xpos[itime]=xpos[itime-1]+0.5*(x[1,itime-1]+x[1,itime])*Deltat
#    print('xpos',xpos[itime])
    if(xpos[itime]<xmin):
        break
#
hf1 = plt.figure()
q1=plt.plot(time, xpos, '-r')
plt.xlabel('time, s', fontsize=14)
plt.ylabel('xpos, m', fontsize=14)
plt.grid(True)
plt.title('posizione')
#
hf2 = plt.figure()
q1=plt.plot(time, x[0,:], '-b')
plt.xlabel('time, s', fontsize=14)
plt.ylabel('current, m', fontsize=14)
plt.grid(True)
plt.title('corrente')
#
hf3 = plt.figure()
q1=plt.plot(time, x[1,:], '-g')
plt.xlabel('time, s', fontsize=14)
plt.ylabel('velocita, m/s', fontsize=14)
plt.grid(True)
plt.title('velocita')
#
hf4 = plt.figure()
q1=plt.plot(time, x[2,:], '-c')
plt.xlabel('time, s', fontsize=14)
plt.ylabel('forza molla, N', fontsize=14)
plt.grid(True)
plt.title('forza elastica')
#
# istante finale
print('istante finale')
cur=V_g/Rt
Fm=G/4*cur**2/xpos[Nist-1]**2
Fel=k_e*(0.02-xpos[Nist-1])
print("forza magnetica: ","{:10.4f}".format(Fm), "N") 
print("forza elastica:  ","{:10.4f}".format(Fel), "N") 
#
# write parametric cost to csv file
# --------------------------
with open('elmech_CN.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['time (s)', 'i (A)', 'xdot (m/s)','f_el (N)'])
    for i in range(Nist):
        writer.writerow([time[i],x[0,i],x[1,i],x[2,i]])
   
    



