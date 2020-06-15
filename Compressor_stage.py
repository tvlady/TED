#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import sympy
import velocity_triangle_plotter as vtp
import free_vortex as fv


def compressor_stage(gamma, R_air, config, Area_in, r_const, N_rpm, Cz, alpha1, deHaller, Tt_in, alpha3, df_r, df_s, Pt_in, m_dot, Re_r, Re_s, V_trinangles,n_stage,turbo_type, units, w_r, w_s, free_vortex_input):
    
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
        r_tip_in=float(abs((temp[0])))
        r_m_in=float(abs((temp[2])))
        r_hub_in=float(abs((temp[1])))
        
    elif config == "HUB":
        r_hub_in=r_const;
        r_tip_in=math.sqrt(Area_in/math.pi + r_hub_in**2);
        r_m_in=math.sqrt((r_tip_in**2+r_hub_in**2)/2);


    h_t_ratio_in = r_hub_in/r_tip_in
    h_blade_r = r_tip_in-r_hub_in
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

    degree_reaction=.5-Cz/U_bladespeed*(math.tan(math.radians(beta2))+math.tan(math.radians(alpha1)))/2;







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
    
    
    P3=pt3*(T3/T_o2)**(gamma/(gamma-1));
    rho_e=P3/(T3*R_air)*1000;
    A_exit=(m_dot)/(rho_e*Cz);
    
    dynamic_visc_1=dynamic_visc(T1);
    rho_1=p1/(T1*R_air)*1000;
    b_r=Re_r/(Cz/math.cos(math.radians(beta1))*rho_1)*dynamic_visc_1;
    s_r=b_r/solidity_r;
    num_blades_r=2*math.pi*r_m_in/s_r;
    num_blades_r=math.ceil(num_blades_r);

    
    
    rho_2=p2/(T2*R_air)*1000;
    
    A_middle=(m_dot)/(rho_2*Cz);

    if config == "TIP":
        r_hub_2=math.sqrt(r_const**2-A_middle/math.pi);
        r_tip_2=r_const;
        r_m_2=math.sqrt((r_tip_2**2+r_hub_2**2)/2); 
        
    elif config == "MEAN":
        
        x, y, z = sympy.symbols('x y z')
        equ1 = sympy.Eq(z-r_const, 0)
        equ2 = sympy.Eq(sympy.root((x**2+y**2)/2,2)-z, 0)
        equ3 = sympy.Eq((x**2-y**2)*math.pi-A_middle, 0) 
        sol =  sympy.solve((equ1, equ2, equ3),(x, y,z))
        temp=sol[0]
        r_tip_2=float(abs(temp[0]))
        r_m_2=float(abs(temp[2]))
        r_hub_2=float(abs(temp[1]))
        
    elif config == "HUB":
        r_hub_2=r_const;
        r_tip_2=math.sqrt(A_middle/math.pi + r_hub_2**2);
        r_m_2=math.sqrt((r_tip_2**2+r_hub_2**2)/2);
    
    
    if config == "TIP":
        r_hub_3=math.sqrt(r_const**2-A_exit/math.pi);
        r_tip_3=r_const;
        r_m_3=math.sqrt((r_tip_2**2+r_hub_2**2)/2); 
        
    elif config == "MEAN":
        
        x, y, z = sympy.symbols('x y z')
        equ1 = sympy.Eq(z-r_const, 0)
        equ2 = sympy.Eq(sympy.root((x**2+y**2)/2,2)-z, 0)
        equ3 = sympy.Eq((x**2-y**2)*math.pi-A_exit, 0) 
        sol =  sympy.solve((equ1, equ2, equ3),(x, y,z))
        temp=sol[0]
        r_tip_3=float(abs(temp[0]))
        r_m_3=float(abs(temp[2]))
        r_hub_3=float(abs(temp[1]))
        
    elif config == "HUB":
        r_hub_3=r_const;
        r_tip_3=math.sqrt(A_exit/math.pi + r_hub_2**2);
        r_m_3=math.sqrt((r_tip_2**2+r_hub_2**2)/2);
    
    h_blade_s=r_tip_2-r_hub_2;
    
    dynamic_visc_2=dynamic_visc(T2);
    b_s=Re_s/(Cz/math.cos(math.radians(alpha2))*rho_2)*dynamic_visc_2;
    s_s=b_s/solidity_s;
    num_blades_s=math.ceil(2*math.pi*r_m_2/s_s);
    
    bz_r=b_r*math.cos(math.radians((beta1+beta2)/2));
    bz_s=b_s*math.cos(math.radians((alpha2+alpha3)/2));
    
    AR_r=h_blade_r/b_r;
    AR_s=h_blade_s/b_s; 
        
    camber_r_old=-25;
    camber_s_old=25;
    
    indicdence_Rotor_stator=2;
    chi_1=indicdence_Rotor_stator+beta1;
    chi_2s=alpha2-indicdence_Rotor_stator;
    
    
    for i in range(0, 10):
        deviation_rotor=.25*camber_r_old/(solidity_r)**(1/2);
        deviation_stator=.25*camber_s_old/(solidity_s)**(1/2);
        chi_2r=beta2-deviation_rotor;
        chi_3=alpha3-deviation_stator;
        camber_r=chi_1-chi_2r;
        camber_s=chi_2s-chi_3;
        camber_r_old=camber_r;
        camber_s_old=camber_s;
        
        
    if V_trinangles == "YES":
        vtp.velocity_triangle_plotter(alpha1, beta1, U_bladespeed, Cz, n_stage, 1, "Mean",turbo_type, units)
        vtp.velocity_triangle_plotter(alpha2, beta2, U_bladespeed, Cz, n_stage, 2, "Mean",turbo_type, units)

    if free_vortex_input == "YES":
        fv.free_vortex_calcs(r_m_in, r_hub_in,r_tip_in, flow_coeff, loading_coeff, N_rpm, alpha1, alpha2, Cz, n_stage, turbo_type, units)
 

    return r_tip_in, r_m_in, r_hub_in, h_t_ratio_in, flow_coeff, loading_coeff, MN1, MN1rel, MN_2, MN_2_rel, solidity_r, solidity_s, n_st, PR_st, num_blades_r, num_blades_s, AR_r, AR_s, A_exit, pt3, T_o3,degree_reaction, r_tip_2, r_m_2, r_hub_2, r_tip_3, r_m_3, r_hub_3, bz_r, bz_s

def dynamic_visc(Temp):
      return 0.000001458*Temp**(3/2)/(Temp+110.4);



    