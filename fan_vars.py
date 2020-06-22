#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:46:39 2020

@author: tedvlady
"""

radius_config="TIP"     #TIP MEAN or HUB
IGV_config="NO"        #YES or NO
turbo_type="Fan"
free_vortex="YES"
units="SI"
n_stage=3;
gamma=1.4
R=287.05;
m_dot_in=241.238331586505;
Pt_in=100.047070435332;
Tt_in=286.994223146370;
PR_req=4.44;

hub_tip_ratio=0.3;
M_in=0.670266664480158
IGV_exit_angle=2;
last_stage_exit_angle=0;
deHaller_first_stage=.72;
deHaller_last_stage=.72;
diff_factor_rotor_first_stage=.425
diff_factor_rotor_last_stage=.425
diff_factor_stator_first_stage=.42
diff_factor_stator_last_stage=.42
reynolds_rotor_first_stage=4.4*10**6
reynolds_rotor_last_stage=4.4*10**6
reynolds_stator_first_stage=3.2*10**6
reynolds_stator_last_stage=3.2*10**6
w_r=0.0379
w_s=0.0379