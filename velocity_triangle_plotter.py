#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:00:42 2020

@author: tedvlady
"""
import math
import matplotlib.pyplot as plt

def velocity_triangle_plotter(alpha, beta, U, Cz, n_stage, station, location, turbo_type, units):
    station=str(station)
    n_stage=str(n_stage)
    if(units=="ENGLISH"):
        Cz=Cz*3.28084
        U=U*3.28084
    c=Cz/math.cos(math.radians(alpha));
    w=Cz/math.cos(math.radians(beta));    
    c_theta=Cz*math.tan(math.radians(alpha));
    plt.figure()
    plt.plot([0, Cz],[0, -Cz*math.tan(math.radians(alpha))], [0, Cz],[0, -Cz*math.tan(math.radians(beta))], [0, Cz],[0, 0],':' ,[Cz, Cz],[-Cz*math.tan(math.radians(alpha)), -Cz*math.tan(math.radians(beta))]);
    plt.axis([0,500,-500,500])
    plt.legend(['$C_{'+ station +'}$: '+ str(round(c))+' m/s @ $ α_{'+ station +'} $ = '+ str(round(alpha))+'°', r'$W_{'+ station +'}$: '+ str(round(w))+ r'm/s @ $ \beta_{'+ station +'} $ = '+ str(round(beta))+'°', r"$C_{z}$: "+ str(round(Cz))+ 'm/s', r"$U$: "+ str(round(U))+ 'm/s'], prop={'size': 6})
    plt.title(turbo_type+ ' Stage '+n_stage+', Station '+ station +', '+ location+ ' Velocity Triangle')
    
    if(units=="ENGLISH"):
        plt.ylabel('Angular Velocity (ft/s)')
        plt.xlabel('Axial Velocity (ft/s)')
        plt.axis([0,1500,-2000,2000])
        plt.legend(['$C_{'+ station +'}$: '+ str(round(c))+' ft/s @ $ α_{'+ station +'} $ = '+ str(round(alpha))+'°', r'$W_{'+ station +'}$: '+ str(round(w))+ r'ft/s @ $ \beta_{'+ station +'} $ = '+ str(round(beta))+'°', r"$C_{z}$: "+ str(round(Cz))+ 'ft/s', r"$U$: "+ str(round(U))+ 'ft/s'], prop={'size': 6})
    else:
        plt.ylabel('Angular Velocity (m/s)')
        plt.xlabel('Axial Velocity (m/s)')
        plt.axis([0,500,-600,600])
        plt.legend(['$C_{'+ station +'}$: '+ str(round(c))+' m/s @ $ α_{'+ station +'} $ = '+ str(round(alpha))+'°', r'$W_{'+ station +'}$: '+ str(round(w))+ r'm/s @ $ \beta_{'+ station +'} $ = '+ str(round(beta))+'°', r"$C_{z}$: "+ str(round(Cz))+ 'm/s', r"$U$: "+ str(round(U))+ 'm/s'], prop={'size': 6})
    plt.savefig('results/'+turbo_type+'/'+'stage_' +n_stage+'_station_'+ station +'_'+ location +'.png', dpi=300)