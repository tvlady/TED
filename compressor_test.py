#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:04:29 2020

@author: tedvlady
"""

import Compressor_stage
import flowpath_plotter as fp
import fan_vars as vars
import math
import numpy
import xlsxwriter


An_in = vars.m_dot_in*math.sqrt(vars.Tt_in)/(vars.Pt_in*1000*(vars.M_in*math.sqrt(vars.gamma/(vars.R))*(1+(vars.gamma-1)/2*vars.M_in**2)**(-1*(vars.gamma+1)/(2*(vars.gamma-1)))))
Tin=vars.Tt_in/(1+(vars.gamma-1)/2*vars.M_in**2);
a_in=math.sqrt(vars.gamma*vars.R*Tin);
Cz=a_in*vars.M_in*math.cos(math.radians(vars.IGV_exit_angle));
if vars.radius_config == "TIP":
    r_const=math.sqrt(An_in/(math.pi*(1-vars.hub_tip_ratio**2)));
elif vars.radius_config == "MEAN":
    temp1=math.sqrt(An_in/(math.pi*(1-vars.hub_tip_ratio**2)));
    temp2=temp1*vars.hub_tip_ratio;
    r_const=math.sqrt((temp1**2+temp2**2)/2);
elif vars.radius_config == "HUB":
    temp=math.sqrt(An_in/(math.pi*(1-vars.hub_tip_ratio**2)));
    r_const=temp*vars.hub_tip_ratio;


alpha_matrix=numpy.linspace(vars.IGV_exit_angle, vars.last_stage_exit_angle, vars.n_stage+1);
dH_matrix=numpy.linspace(vars.deHaller_first_stage, vars.deHaller_last_stage, vars.n_stage);
df_r_matrix=numpy.linspace(vars.diff_factor_rotor_first_stage, vars.diff_factor_rotor_last_stage, vars.n_stage);
df_s_matrix=numpy.linspace(vars.diff_factor_stator_first_stage, vars.diff_factor_stator_last_stage, vars.n_stage);
reynolds_r_matrix=numpy.linspace(vars.reynolds_rotor_first_stage, vars.reynolds_rotor_last_stage, vars.n_stage);
reynolds_s_matrix=numpy.linspace(vars.reynolds_stator_first_stage, vars.reynolds_stator_last_stage, vars.n_stage);




T_temp=vars.Tt_in
P_temp=vars.Pt_in
A_temp=An_in
PR_total=1;
rpm_min=2000
rpm_max=20000
rpm=0;
i=0;
while(abs(vars.PR_req-PR_total)>.001):
    i=i+1
    rpm=(rpm_max+rpm_min)/2
    
    PR_total=.99;
    T_temp=vars.Tt_in
    P_temp=vars.Pt_in
    A_temp=An_in
    for x in range(vars.n_stage):
        _, _, _, _, _, _, _, _, _, _, _, _, _, PR_st, _, _, _, _, A_exit, pt3, T_o3,_, _, _, _, _, _, _, _, _  = Compressor_stage.compressor_stage(vars.gamma, vars.R, vars.radius_config, A_temp, r_const, rpm, Cz, alpha_matrix[x], dH_matrix[x], T_temp, alpha_matrix[x+1], df_r_matrix[x], df_s_matrix[x], P_temp, vars.m_dot_in, reynolds_r_matrix[x], reynolds_s_matrix[x], "NO", x+1,vars.turbo_type, vars.units, vars.w_r, vars.w_s, "NO");
        PR_total=PR_st*PR_total;
        T_temp=T_o3
        P_temp=pt3
        A_temp=A_exit
      
        
    if(PR_total-vars.PR_req<0):    
        rpm_min=rpm
    else:
        rpm_max=rpm
        
    print('iteration ' + str(i))
    print(str(rpm))
    print(str(PR_total))

T_temp=vars.Tt_in
P_temp=vars.Pt_in
A_temp=An_in
PR_total=1;
out = []
flowpath_out=[]
for x in range(vars.n_stage):
    r_tip_in, r_m_in, r_hub_in, h_t_ratio_in, flow_coeff, loading_coeff, MN1, MN1rel, MN_2, MN_2_rel, solidity_r, solidity_s, n_st, PR_st, num_blades_r, num_blades_s, AR_r, AR_s, A_exit, pt3, T_o3,degree_reaction, r_tip_2, r_m_2, r_hub_2, r_tip_3, r_m_3, r_hub_3, bz_r, bz_s = Compressor_stage.compressor_stage(vars.gamma, vars.R, vars.radius_config, A_temp, r_const, rpm, Cz, alpha_matrix[x], dH_matrix[x], T_temp, alpha_matrix[x+1], df_r_matrix[x], df_s_matrix[x], P_temp, vars.m_dot_in, reynolds_r_matrix[x], reynolds_s_matrix[x], "YES",x+1,vars.turbo_type, vars.units, vars.w_r, vars.w_s, vars.free_vortex);
    out.append([PR_st, n_st, flow_coeff, loading_coeff,degree_reaction,dH_matrix[x], MN1rel, solidity_r, solidity_s, df_r_matrix[x], df_s_matrix[x],h_t_ratio_in, r_tip_in, r_m_in, r_hub_in,num_blades_r, num_blades_s, AR_r, AR_s ])
    flowpath_out.append([r_tip_in, r_m_in, r_hub_in, bz_r, .8])
    flowpath_out.append([r_tip_2, r_m_2, r_hub_2, bz_s, 1])
    PR_total=PR_st*PR_total;
    T_temp=T_o3
    P_temp=pt3
    A_temp=A_exit
    
flowpath_out.append([r_tip_3, r_m_3, r_hub_3,0,0])

out=numpy.array(out)
flowpath_out=numpy.array(flowpath_out)



fp.flowpath_plotter(flowpath_out, vars.IGV_config, vars.turbo_type, vars.units)


labels=['PR_st', 'eff_st', 'flow_coeff', 'loading_coeff','Reaction','dehaller', 'MN1rel', 'solidity_r', 'solidity_s', 'diffusion_factor_r','diffusion_factor_s', 'h_t_ratio_in', 'r_tip_in', 'r_m_in', 'r_hub_in','num_blades_r', 'num_blades_s', 'AR_r', 'AR_s']

workbook = xlsxwriter.Workbook('out.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write_row(0, 0, labels)

col = 0

for row, data in enumerate(out):
    worksheet.write_row(row+1, col, data)

workbook.close()

