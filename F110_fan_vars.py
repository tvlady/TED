#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 12:46:39 2020

@author: tedvlady
"""

radius_config="MEAN"     #TIP MEAN or HUB
IGV_config="NO"        #YES or NO
turbo_type="F110_Fan"
free_vortex="YES"
units="ENGLISH"
n_stage=3;
gamma=1.4
R=287.05;
m_dot_in=122.016;
Pt_in=93.286066;
Tt_in=287.55556;
PR_req=3.5;

hub_tip_ratio=0.43;
M_in=0.4;
IGV_exit_angle=10;
last_stage_exit_angle=0;
deHaller_first_stage=.72;
deHaller_last_stage=.72;
diff_factor_rotor_first_stage=.332
diff_factor_rotor_last_stage=.332
diff_factor_stator_first_stage=.49
diff_factor_stator_last_stage=.48
reynolds_rotor_first_stage=6*10**6
reynolds_rotor_last_stage=6*10**6
reynolds_stator_first_stage=1.3*10**6
reynolds_stator_last_stage=1.3*10**6
w_r=0.057
w_s=0.057