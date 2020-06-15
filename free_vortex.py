#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 19:41:12 2020

@author: tedvlady
"""
import numpy
import matplotlib.pyplot as plt
import math

def free_vortex_calcs(r_m, r_hub_rotor,r_tip_rotor, flow_coeff, loading_coeff, N_rpm, alpha1, alpha2, Cz, n_stage, turbo_type, units):

    r_vector=numpy.array(numpy.linspace(r_hub_rotor,r_tip_rotor,100));
    c_theta1=Cz*math.tan(math.radians(alpha1));
    c_theta2=Cz*math.tan(math.radians(alpha2));
    
    flow_matrix=[]
    loading_matrix=[]
    wheel_speed_matrix=[]
    alpha1_matrix=[]
    beta1_matrix=[]
    alpha2_matrix=[]
    beta2_matrix=[]
    turning=[]
    reaction_matrix=[]
    
    for i in range(len(r_vector)):
        flow_matrix.append(flow_coeff*r_m/(r_vector[i]))
        loading_matrix.append(loading_coeff*(r_m/(r_vector[i]))**2)
        wheel_speed_matrix.append(r_vector[i]*N_rpm*math.pi*1/30)
        alpha1_matrix.append(math.degrees(math.atan((c_theta1/Cz*r_m/(r_vector[i])))));
        beta1_matrix.append(math.degrees(math.atan((c_theta1*r_m/(r_vector[i])-wheel_speed_matrix[i])/Cz)));
        alpha2_matrix.append(math.degrees(math.atan((c_theta2/Cz*r_m/(r_vector[i])))));
        beta2_matrix.append(math.degrees(math.atan((c_theta2*r_m/(r_vector[i])-wheel_speed_matrix[i])/Cz)));
        turning.append(abs(beta1_matrix[i]-beta2_matrix[i]));
        reaction_matrix.append(.5-Cz/wheel_speed_matrix[i]*(math.tan(math.radians(beta2_matrix[i]))+math.tan(math.radians(alpha1_matrix[i])))/2);

    plt.figure()
    plt.plot(flow_matrix,r_vector*39.3701,loading_matrix,r_vector*39.3701, reaction_matrix, r_vector*39.3701 )
    plt.xlabel('Parameter value')
    plt.ylabel('blade radius (in)')
    plt.legend(['flow coefficent', 'loading coefficent', 'degree reaction']);
    
    plt.figure()
    plt.plot(beta1_matrix,r_vector*39.3701 ,beta2_matrix,r_vector*39.3701, turning,r_vector*39.3701)
    plt.ylabel('blade radius (in)')
    plt.xlabel('Angle (deg)')
    plt.legend(['beta1', 'beta2', 'turning']);
   
    
    