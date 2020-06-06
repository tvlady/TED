#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import sympy

def compressor_stage(gamma, R_air, config, Area_in, r_const, N_rpm, Cz, alpha1, deHaller, Tt_in, alpha3, df_r, df_s, Pt_in):
    
    cp=R_air*(gamma/(gamma-1));
    
    if config == "TIP":
        r_hub_in=math.sqrt(r_const**2-Area_in/math.pi);
        r_tip_in=r_const;
        r_m_in=math.sqrt((r_tip_in**2+r_hub_in**2)/2); 
        
    elif config == "MEAN":
        
        x, y, z = sympy.symbols('x y z')
        equ1 = sympy.Eq(z-r_const, 0)
        equ2 = sympy.Eq(sympy.root((x**2+y**2)/2,2)-z, 0)
        equ3 = sympy.Eq((x**2-y**2)*math.pi-Area_in, 0) 
        sol =  sympy.solve((equ1, equ2, equ3),(x, y,z))
        temp=sol[0]
        r_tip_in=abs(temp[0])
        r_m_in=abs(temp[2])
        r_hub_in=abs(temp[1])
        
    elif config == "HUB":
        r_hub_in=r_const;
        r_tip_in=math.sqrt(Area_in/math.pi + r_hub_in**2);
        r_m_in=math.sqrt((r_tip_in**2+r_hub_in**2)/2);


    h_t_ratio_in = r_hub_in/r_tip_in
    h_blade_rotor = r_tip_in-r_hub_in
    U_bladespeed=r_m_in*N_rpm*math.pi*1/30;
    flow_coeff=Cz/U_bladespeed; 
    
    beta1=math.degrees(math.atan((math.tan(math.radians(alpha1))-1/flow_coeff)));
    x = sympy.symbols('x')
    equ1 = sympy.Eq(sympy.cos(math.radians(beta1)),(deHaller*sympy.cos(x)))
    sol =  sympy.solve((equ1),(x))
    beta2 = math.degrees(min(sol))*-1
    alpha2= math.degrees(math.atan((math.tan(math.radians(beta2))*Cz+U_bladespeed)/Cz));

    d_ctheta_1_2=U_bladespeed+Cz*(math.tan(math.radians(beta2))-math.tan(math.radians(alpha1)));
    loading_coeff=d_ctheta_1_2/U_bladespeed;                  


    T1=Tt_in-(Cz/math.cos(math.radians(alpha1)))**2/(2*cp);
    MN1=Cz/math.cos(math.radians(alpha1))/(gamma*R_air*T1)**(1/2);
    MN1rel=Cz/math.cos(math.atan((math.tan(math.radians(alpha1))*Cz-U_bladespeed)/Cz))/(gamma*R_air*T1)**(1/2);


    T_o2=Tt_in+(Cz/flow_coeff)**2*loading_coeff/cp;
    T2=T_o2-Cz**2/(2*cp*(math.cos(math.radians(alpha2))**2));
    MN_2=Cz/math.cos(math.radians(alpha2))/(gamma*R_air*T2)**(1/2);
    MN_2_rel=(Cz/math.cos(math.radians(beta2)))/math.sqrt(gamma*R_air*T2);

    T3=T_o2-(Cz/math.cos(math.radians(alpha3)))**2/(2*cp);
    T_o3=T_o2

    x = sympy.symbols('x')
    equ1 = sympy.Eq(1-sympy.cos(math.radians(beta1))/sympy.cos(math.radians(beta2))+1/x*sympy.cos(math.radians(beta1))/2*(sympy.tan(math.radians(beta2))-sympy.tan(math.radians(beta1))),df_r);
    sol =  sympy.solve((equ1),(x))
    solidity_r=float(sol[0])

    x = sympy.symbols('x')
    equ1 = sympy.Eq(1-sympy.cos(math.radians(alpha2))/sympy.cos(math.radians(alpha3))+1/x*sympy.cos(math.radians(alpha2))/2*(sympy.tan(math.radians(alpha2))-sympy.tan(math.radians(alpha3))),df_s);
    sol =  sympy.solve((equ1),(x))
    solidity_s=float(sol[0])

    w_r=0.0379;
    w_s=0.0379;
    
    p1=(1+(gamma-1)/2*MN1**2)**(-gamma/(gamma-1))*Pt_in;
    pt1r=(1+(gamma-1)/2*MN1rel**2)**(gamma/(gamma-1))*p1;
    pt2r=pt1r-(pt1r-p1)*w_r;
    p2=(1+(gamma-1)/2*MN_2_rel**2)**(-gamma/(gamma-1))*pt2r;
    pt2=(1+(gamma-1)/2*MN_2**2)**(gamma/(gamma-1))*p2;
    
    pt3=pt2-(pt2-p2)*w_s;
    
    
    
    Po2_Po1=pt2/Pt_in;
    Po3_Po2=pt3/pt2;
    
    
    PR_st=Po3_Po2*Po2_Po1;

    n_st=(PR_st**((gamma-1)/gamma)-1)/(T_o2/Tt_in-1);
   
    return r_tip_in, r_m_in, r_hub_in, h_t_ratio_in, flow_coeff, loading_coeff, MN1, MN1rel, MN_2, MN_2_rel, solidity_r, solidity_s, n_st, PR_st

  
    