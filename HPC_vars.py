#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:46:39 2020

@author: tedvlady
"""

radius_config="TIP"     #TIP MEAN or HUB
IGV_config="NO"        #YES or NO
turbo_type="HPC"
units="ENGLISH"
n_stage=6;
gamma=1.35
R=287;
m_dot_in=162.198148912000;
Pt_in=578.364806505281;
Tt_in=596.834223263889;
PR_req=8.5;

hub_tip_ratio=0.665;
M_in=.55;
IGV_exit_angle=7;
last_stage_exit_angle=0;
deHaller_first_stage=.72;
deHaller_last_stage=.72;
diff_factor_rotor_first_stage=.425
diff_factor_rotor_last_stage=.425
diff_factor_stator_first_stage=.43
diff_factor_stator_last_stage=.43
reynolds_rotor_first_stage=2.4*10**6
reynolds_rotor_last_stage=2.4*10**6
reynolds_stator_first_stage=1.5*10**6
reynolds_stator_last_stage=1.5*10**6
w_r=0.0377
w_s=0.0377