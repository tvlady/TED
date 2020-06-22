import math
import matplotlib.pyplot as plt
import numpy as np

def bladeplotter(V1,t_c_max, Vtheta1,Vtheta2,s, c, stagger, turbo_type, stage):
    stagger=stagger*-1;
    x_c_NACA=[0,0.005,0.0075,0.0125,0.025,0.05,0.075,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5,0.55,0.6,0.65,0.7,0.75,0.8,0.85,0.9,0.95,1];
    t_c_NACA=[0,0.772,0.932,1.4,1.8,2.177,2.641,3.04,3.666,4.143,4.503,4.76,4.924,4.966,4.963,4.812,4.53,4.146,3.682,3.146,2.584,1.987,1.385,0.81,0.306,0];
    x_c_NACA=np.array(x_c_NACA)
    t_c_NACA=np.array(t_c_NACA)
    
    circuation=abs((-Vtheta1+Vtheta2)*s);
    Cl_star=2*circuation/(V1*c);
    
    
    x_c=np.arange(0.001, .999, .001)
    t_c_NACA_adj=t_c_NACA*t_c_max*c/max(t_c_NACA);
    t=np.interp(x_c,x_c_NACA,t_c_NACA_adj)*c;
    
    y_camber_c=[]
    v_angle=[]
    camber_x=[]
    camber_y=[]
    x_top=[]
    y_top=[]
    x_bot=[]
    y_bot=[]
    for i in range(len(x_c)):
        y_camber_c.append(-Cl_star/(4*math.pi)*((1-x_c[i])*math.log(1-x_c[i])+x_c[i]*math.log(x_c[i])))
        v_angle.append(math.atan(Cl_star/(4*math.pi)*math.log((1-x_c[i])/x_c[i])))
    
        x_top.append(39.9*(x_c[i]*c-t[i]/2*math.sin(v_angle[i])));
        y_top.append(39.9*(y_camber_c[i]*c+t[i]/2*math.cos(v_angle[i])));
        
        x_bot.append(39.9*(x_c[i]*c+t[i]/2*math.sin(v_angle[i])));
        y_bot.append(39.9*(y_camber_c[i]*c-t[i]/2*math.cos(v_angle[i])));
    
        a_rad=((stagger*math.pi)/180); 
        R, THETA = cart2pol(x_top[i],y_top[i]); 
        THETA=THETA+a_rad; 
        temp1,temp2 = pol2cart(R, THETA); 
        x_top[i]=temp1
        y_top[i]=temp2
        R, THETA = cart2pol(x_bot[i],y_bot[i])
        THETA=THETA+a_rad
        temp1,temp2 = pol2cart(R, THETA); 
        x_bot[i]=temp1
        y_bot[i]=temp2
        camber_x.append((x_top[i]+x_bot[i])/2)
        camber_y.append((y_top[i]+y_bot[i])/2)
        
    y_camber_c=np.array(y_camber_c)
    v_angle=np.array(v_angle)
    camber_x=np.array(camber_x)
    camber_y=np.array(camber_y)
    x_top=np.array(x_top)
    y_top=np.array(y_top)
    x_bot=np.array(x_bot)
    y_bot=np.array(y_bot)
        
    flow_in=math.atan((camber_y[25]-camber_y[2])/(camber_x[25]-camber_x[2]))
    flow_out=math.atan((camber_y[len(camber_y)-1]-camber_y[len(camber_y)-25])/(camber_x[len(camber_y)-1]-camber_x[len(camber_y)-25]))
    turning=(flow_in-flow_out)*180/math.pi


    plt.figure()
    plt.plot(x_top,y_top, 'k',x_bot,y_bot,'k', linewidth=.5)
    plt.savefig('results/'+turbo_type+'/'+ str(stage) +'_blade_drawing' +'.png', dpi=300)


def cart2pol(x, y):
    R = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return(R, theta)

def pol2cart(R, theta):
    x = R * np.cos(theta)
    y = R * np.sin(theta)
    return(x, y)