#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# =============================================================================
# Parses NPSS map file and plots Compressor map
# by Ted Vlady - adapted from Jeff Schutte's MATLAB Map plotter code
# Requires a NPSS Compressor Map file
# User must manually go into map file and input the "key words"
# Option included to scale the maps


####INPUT DEFINTION####
# path - path to NPSS map file
# Wc_var - in the Wc Table what is the Wc variable named? Examples are WcMap, WcorrMap, FLOW, etc
# eff_var - in the eff Table what is the eff variable named? Examples are effMap, effAdiabMap, EFF, etc
# PR_var - in the PR Table what is the PR variable named? Examples are PRmap, PratioMap, PR, etc
# alpha_var - in all of the Tables what is the alpha variable named? Examples are alphaMap, ALPHA, etc

####MORE NOTES####
#its important to define these correctly or the parser won't be able to identify where the data is
#the current design of the code ignores the effect of variable IGVs and only plots the first alpha setting


#there are a few issues that I could  not resolve
#  -Adding the conts speed line labels throws off the automatic figure sizing, I tried to add my own but it needs some adjustment


#  I am sure there are more issues and improvments to be made. If you ever improve the code please email me an update: tedvladi@gmail.com
# =============================================================================




import re
import numpy
import math
import matplotlib.pyplot as plt


####INPUTS#####
cmp_type = "LPC"
path="LPC.map"
Nc_var="SPED"
Wc_var="FLOW"
eff_var="EFF"
PR_var="PR"
alpha_var="ALPHA"

Wc_scaler=5
eff_scaler=1
PR_scaler=1
Nc_scaler=1


####CODE####
TB_Wc="FALSE"
Wc_on=0;
eff_on=0;
PR_on=0;
bracket_on="TRUE";
Nc_array=[]
Wc_array=[]
eff_array=[]
PR_array=[]
temp=""


f = open(path,"r" ,encoding="utf8", errors='ignore')
TB_eff="FALSE"

for x in f:
    line=x
    if "Table TB_Wc" in line:
        while(Wc_on<2):        
            line=f.readline()
            if alpha_var in line:
                Wc_on=Wc_on+1;
            elif Nc_var in line:
                Nc_temp=line
                Nc_temp=Nc_temp.split("=")[1]
                Nc_temp=Nc_temp.split("}")[0]
                Nc_temp=Nc_temp.replace('\t'," ")
                " ".join(Nc_temp.split())
                Nc_temp=re.findall('\d*\.?\d+',Nc_temp)
                Nc_temp=[float(i) for i in Nc_temp]
                Nc_array.append(Nc_temp)
            elif Wc_var in line:
                while(bracket_on=="TRUE"):
                    if "}" in line:
                        bracket_on="FALSE";
                        temp=temp+line
                        line=f.readline()
                    else:
                        temp=temp+line;
                        line=f.readline()
                        
                bracket_on="TRUE"
                temp=temp.split("{")[1]
                temp=temp.split("}")[0]
                temp=temp.replace('\n'," ")
                temp=temp.replace('\t'," ")
                temp=temp.replace(','," ")
                " ".join(temp.split())
                temp=re.findall('\d*\.?\d+',temp)
                temp=[float(i) for i in temp]
                Wc_array.append(temp)
                temp=""
    if "Table TB_eff" in line:
        while(eff_on<2):        
            line=f.readline()
            if alpha_var in line:
                eff_on=eff_on+1;
            elif eff_var in line:
                while(bracket_on=="TRUE"):
                    if "}" in line:
                        bracket_on="FALSE";
                        temp=temp+line
                        line=f.readline()
                    else:
                        temp=temp+line;
                        line=f.readline()
                        
                bracket_on="TRUE"
                temp=temp.split("{")[1]
                temp=temp.split("}")[0]
                temp=temp.replace('\n'," ")
                temp=temp.replace('\t'," ")
                temp=temp.replace(','," ")
                " ".join(temp.split())
                temp=re.findall('\d*\.?\d+',temp)
                temp=[float(i) for i in temp]
                eff_array.append(temp)
                temp=""
    if "Table TB_PR" in line:
        while(PR_on<2):        
            line=f.readline()
            if alpha_var in line:
                PR_on=PR_on+1;
            elif PR_var in line:
                while(bracket_on=="TRUE"):
                    if "}" in line:
                        bracket_on="FALSE";
                        temp=temp+line
                        line=f.readline()
                    else:
                        temp=temp+line;
                        line=f.readline()
                        
                bracket_on="TRUE"
                temp=temp.split("{")[1]
                temp=temp.split("}")[0]
                temp=temp.replace('\n'," ")
                temp=temp.replace('\t'," ")
                temp=temp.replace(','," ")
                " ".join(temp.split())
                temp=re.findall('\d*\.?\d+',temp)
                temp=[float(i) for i in temp]
                PR_array.append(temp)
                temp=""

f.close()
eff_array_plt=numpy.array(eff_array)*eff_scaler
PR_array_plt=(numpy.array(PR_array)-1)*PR_scaler+1
Wc_array_plt=numpy.array(Wc_array)*Wc_scaler
Nc_array_plt=numpy.array(Nc_array)*Nc_scaler

Nc_labels=(Nc_array_plt*100)-.0001      #this deals with the silly python round() issues


if(len(eff_array_plt)>0):
    plt.plot(Wc_array_plt[:,0],PR_array_plt[:,0], 'r');
    for i in range(len(Wc_array)):
        plt.plot(Wc_array_plt[i,:],PR_array_plt[i,:], 'b');
        
    for j in range(len(Wc_array_plt[:,0])):
        plt.annotate(str(math.ceil(Nc_labels[j,0])),(Wc_array_plt[j,0],PR_array_plt[j,0]), textcoords="offset points", xytext=(0,10), ha='center' )
    contours=plt.contour(Wc_array_plt,PR_array_plt,eff_array_plt, zorder=3)
    plt.clabel(contours, inline=False, fontsize=8, colors="k")
    plt.xlabel("Wc")
    plt.ylabel("PR")
    
    plt.xlim([min(min((Wc_array)))*Wc_scaler*.80,max(max((Wc_array)))*Wc_scaler*1.1])
    plt.ylim([1,((max(max((PR_array)))-1)*PR_scaler+1)*1.1])
    plt.savefig(cmp_type+".jpg", dpi=300)
