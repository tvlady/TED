#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 00:04:29 2020

@author: tedvlady
"""

import Compressor_stage

r_tip_in, r_m_in, r_hub_in, h_t_ratio_in, flow_coeff, loading_coeff, mn_1, mn_1rel, mn_2, mn_2rel, solidity_r, solidity_s, n_st, PR_st = Compressor_stage.compressor_stage(1.4, 287, "TIP", 1.11567518800000, 0.624702515673106, 6913, 218.043594140771, 2, .72, 287, 1, .425, .42, 100.047070435332);



print("waow")