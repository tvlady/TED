#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:02:28 2020

@author: tedvlady
"""
import numpy
import matplotlib.pyplot as plt




def flowpath_plotter(plot_matrix, IGV_config, turbo_type,units):
    Tip_matrix=plot_matrix[:,0];
    Mean_matrix=plot_matrix[:,1];
    hub_matrix=plot_matrix[:,2];
    Bz_matrix=plot_matrix[:,3];
    TR_matrix=plot_matrix[:,4];
    length_matrix=numpy.zeros([1,len(Tip_matrix)]);
    
    if(units=="ENGLISH"):
        Tip_matrix=Tip_matrix*39.3701
        Mean_matrix=Mean_matrix*39.3701
        hub_matrix=hub_matrix*39.3701
        Bz_matrix=Bz_matrix*39.3701
    
    
    for i in range(1,len(Bz_matrix)):
        length_matrix[0,i]=length_matrix[0,i-1]+Bz_matrix[i-1]*1.25;
    
    length_matrix=numpy.transpose(length_matrix)
    length_matrix=numpy.array(length_matrix)
    length_matrix=length_matrix[:,0]
    
    plt.figure()
    plt.plot(length_matrix,Tip_matrix, 'k',length_matrix,Mean_matrix,'--r' ,length_matrix,hub_matrix,'k')
    
    for i in range(0,len(length_matrix)-1):
        mid_len=(length_matrix[i]+length_matrix[i+1])/2;
        bottom_blade_len=Bz_matrix[i]/(1-(1-TR_matrix[i])/2);
        top_blade_len=bottom_blade_len*TR_matrix[i];
        bottom_l_hub=numpy.interp(mid_len-bottom_blade_len/2,[length_matrix[i],length_matrix[i+1]], [hub_matrix[i],hub_matrix[i+1]]);
        bottom_r_hub=numpy.interp(mid_len+bottom_blade_len/2,[length_matrix[i],length_matrix[i+1]], [hub_matrix[i],hub_matrix[i+1]]);
        top_l_hub=numpy.interp(mid_len-top_blade_len/2, [length_matrix[i],length_matrix[i+1]], [Tip_matrix[i],Tip_matrix[i+1]]);
        top_r_hub=numpy.interp(mid_len+top_blade_len/2,[length_matrix[i],length_matrix[i+1]], [Tip_matrix[i],Tip_matrix[i+1]]);
        plt.plot([mid_len-bottom_blade_len/2, mid_len-top_blade_len/2],[bottom_l_hub, top_l_hub],'k',[mid_len+bottom_blade_len/2, mid_len+top_blade_len/2], [bottom_r_hub, top_r_hub], 'k')
        
        
        bottom_l_m_hub=numpy.interp(mid_len-top_blade_len/2,[length_matrix[i],length_matrix[i+1]], [hub_matrix[i],hub_matrix[i+1]]);
        bottom_r_m_hub=numpy.interp(mid_len+top_blade_len/2,[length_matrix[i],length_matrix[i+1]], [hub_matrix[i],hub_matrix[i+1]]);
        x = [mid_len-bottom_blade_len/2, mid_len-top_blade_len/2, mid_len+top_blade_len/2, mid_len+bottom_blade_len/2]
        y1 = numpy.array([bottom_l_hub,bottom_l_m_hub,bottom_r_m_hub, bottom_r_hub])
        y2 = numpy.array([bottom_l_hub, top_l_hub, top_r_hub, bottom_r_hub])
        
        if(IGV_config=="YES"):
            if (i % 2) == 0:
                plt.fill_between(x, y1, y2, facecolor='grey', alpha=1)
            else:
                plt.fill_between(x, y1, y2, facecolor='k', alpha=1)
        else:
            if (i % 2) == 0:
                plt.fill_between(x, y1, y2, facecolor='k', alpha=1)
            else:
                plt.fill_between(x, y1, y2, facecolor='lightgrey', alpha=1)
    
    if(units=="ENGLISH"):
        plt.ylabel('Radial length (in)')
        plt.xlabel('Axial length (in)')
    else:
        plt.ylabel('Radial length (m)')
        plt.xlabel('Axial length (m)')
    plt.title(turbo_type+' flowpath drawing')
    plt.savefig(turbo_type+'_flowpath_drawing'+'.png', dpi=300)
 
        