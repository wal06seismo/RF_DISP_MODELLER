###########33
## Tkinter
import tkinter
from tkinter import Menu, filedialog, PhotoImage 
import tkFileDialog
import tkMessageBox
import tkSimpleDialog

##################
## OS stuff
import os
from shutil import copyfile

################
## Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as  NavigationToolbar2Tk
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.widgets import MultiCursor, Cursor
from matplotlib.patches import Polygon
import numpy as np

#####################
### user defined liberaries
import Modify_model
import Make_CPS_model 
import interpolate_lib
import prep_model



#### clear up
## setting up the input file
path=os.getcwd()
#os.system("rm -f updated_model ")
#os.system("rm -f temp* tmp* ")
rf='./PS49_stack.xy'
import prep_model
vel='./vel.inp'
vp_vs='./vp_vs.inp'
disp='./200_SURF96.inp'
data=np.loadtxt(vel)
step=len(data)
#X,Y = interpolate_lib.interpolate_1D(data[:,1],data[:,0],20)
#X=np.flip(X,axis=0)
#Y=np.flip(Y,axis=0)
#to_save = np.column_stack((Y,X))
'''
np.savetxt('updated_model_vs', data) 
vel = './updated_model_vs'
step=len(data)
data=np.loadtxt(vp_vs)
X,Y = interpolate_lib.interpolate_1D(data[:,1],data[:,0],step)
X=np.flip(X,axis=0)
Y=np.flip(Y,axis=0)
to_save = np.column_stack((Y,X))
np.savetxt('updated_model_vp_vs', to_save) 
vp_vs = './updated_model_vp_vs'
'''
#copyfile(path+vel,path+'/updated_model')
#vel = './updated_model'
################3
## Tkinter Functions
def hello():
    print "hello!"

def on_key_press(event):
    print("you pressed {}".format(event.key))
    key_press_handler(event, canvas, toolbar)

def _quit():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def _modify_model():
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate

def load_LitMod_model(vel,vp_vs):
    
    '''
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    vel = root.filename
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    vp_vs = root.filename
    '''
    prep_model.prep_model_litmod('post_processing_output.dat',200)
    data=np.loadtxt(vel)
    step=len(data)
    y=data[:,1]
    x=data[:,0]
    
    y=np.append(y,y[-1])
    y=np.append(y,y[0])
    
    x=np.append(x,0)
    x=np.append(x,0)
    to_save = np.column_stack((x,y))
    np.savetxt('updated_model_vs', to_save) 
    vel = 'updated_model_vs'
    step=len(data)
    data=np.loadtxt(vp_vs)
    Y,X = interpolate_lib.interpolate_1D(data[:,1],data[:,0],step)
    X=np.flip(X,axis=0)
    Y=np.flip(Y,axis=0)
    Y=np.append(Y,Y[-1])
    Y=np.append(Y,Y[0])
    X=np.append(X,0)
    X=np.append(X,0)
    to_save = np.column_stack((X,Y))
    np.savetxt('updated_model_vp_vs', to_save) 
    vp_vs = 'updated_model_vp_vs'

def load_rf():
    global rf
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    rf = root.filename
    return rf
def load_vel():
    global vel
    #os.system('rm -f updated_model')
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    vel = root.filename
    data=np.loadtxt(vel)
    step=len(data)
    y=data[:,1]
    x=data[:,0]
    
    y=np.append(y,y[-1])
    y=np.append(y,y[0])
    
    x=np.append(x,0)
    x=np.append(x,0)
    to_save = np.column_stack((x,y))
    np.savetxt('updated_model_vs', to_save) 
    vel = 'updated_model_vs'
def load_vp_vs():
    global vel
    #os.system('rm -f updated_model')
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    vp_vs = root.filename
    return vp_vs

def load_disp():
    global disp
    root.filename =  filedialog.askopenfilename(initialdir = path,title = "Select file",filetypes = (("all files","*.*"),("text files","*.txt")))
    disp = root.filename
    return disp

def save():
    os.system("cp updated_model_vs vel-`date +%F_time-%T`.inp.bak ")
    os.system("cp updated_model_vs last_vel.inp")
    os.system("cp updated_model_vp_vs vp_vs-`date +%F_time-%T`.inp.bak ")
    os.system("cp updated_model_vp_vs last_vp_vs.inp")

def save_as(): ### This is not working
    #f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".inp")
    f = tkSimpleDialog.askstring
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    command='cp updated_model_vs '+ str(f)
    os.system(command)

def plot(vel,vp_vs,rf,disp,fig):
    fig.clear()
    ################Vs
    data=np.loadtxt('updated_model_vs')
    y=list(data[:,1])
    x=list(data[:,0])
    poly = Polygon(np.column_stack([x, y]), animated=True)
    ax_vel=fig.add_subplot(141)
    #cursor = MultiCursor(ax_vel, useblit=True, color='black', linewidth=1)
    ax_vel.add_patch(poly)
    ax_vel.set_xlim([min(x),4.2]);  ax_vel.set_ylim([min(y),max(y)]); plt.grid()
    ax_vel.set_xlabel('Vs ($km/s$)');   ax_vel.set_ylabel('Depth ($km$)');    ax_vel.set_title('Shear Wave Velocity')
    p1 = Modify_model.PolygonInteractor(ax_vel, poly,'updated_model_vs',20)
    #canvas.draw()
    ################Vs
    ax_vp_vs = fig.add_subplot(142)
    data_vp_vs=np.loadtxt('updated_model_vp_vs')
    y=list(data_vp_vs[:,1]);x=list(data_vp_vs[:,0])
    poly_vp_vs = Polygon(np.column_stack([x, y]), animated=True)
    #ax_vp_vs.add_patch(poly_vp_vs)
    ax_vp_vs.plot(data_vp_vs[:,0],data_vp_vs[:,1],color='r',label='Synthetic')
    ax_vp_vs.add_patch(poly_vp_vs)#plot(data_vp_vs[:,0],data_vp_vs[:,1],color='r',label='Synthetic')
    p2 = Modify_model.PolygonInteractor(ax_vp_vs, poly_vp_vs,'updated_model_vp_vs',20)
    ax_vp_vs.set_xlim([0,2.0]);ax_vp_vs.set_ylim([min(y),max(y)]); plt.grid(); ax_vp_vs.set_title('Vp Vs Ratio')
    ######## make CPS input file
    #Make_CPS_model
    Make_CPS_model.make()
    #############RF
    # plot observed RF
    ax_rf = fig.add_subplot(143)
    data=np.loadtxt(rf); ax_rf.plot(data[:,1],data[:,0],color='k',label='Observed')
    ##### run and plot RF forward
    os.system("hrftn96 -P -ALP 2.5 -DT 0.1 -D 5. -RAYP 0.07 -M temp_mod  -2 hr  -NSAMP 1500")
    os.system("mv hrftn96.sac temp_mod.2.5.eqr")
    os.system("sac2xy temp_mod.2.5.eqr rf.out")
    data=np.loadtxt('rf.out') 
    ax_rf.plot(data[:,1],data[:,0],color='r',label='Synthetic')
    ax_rf.invert_yaxis()
    ax_rf.set_ylim((20,-5))
    plt.legend(loc='best')
    plt.grid()
    ax_rf.set_xlabel('Amplitude ');    ax_rf.set_ylabel('Time ($s$)');    ax_rf.set_title('P-wave RF')
    ######### Disp
    ### Plot observed disp
    data=np.loadtxt(disp,usecols=(5,6,7))
    ax_disp = fig.add_subplot(144)
    ax_disp.errorbar(data[:,1],data[:,0],xerr=data[:,2],fmt='o',label='Observed')
    ### run and plot disp forward
    os.system("surf96 39")
    os.system("surf96 1 2 6")
    os.system("surf96 27 disp.out")
    data=np.loadtxt('disp.out',usecols=(5,6,7))
    ax_disp.errorbar(data[:,1],data[:,0],xerr=data[:,2],fmt='o',color='r',label='Synthetic')
    plt.legend(loc='best')
    plt.grid()
    ax_disp.invert_yaxis();     ax_disp.set_ylim((max(data[:,0]),min(data[:,0])));    ax_disp.set_xlabel('Velocity ($km/s$)')
    ax_disp.set_ylabel('Period ($s$)');     ax_disp.set_title('Dispersion Curve')
    canvas.draw()
    canvas.mpl_connect("key_press_event", on_key_press)



######################################
### Main App
##### Starting TKinter
root = tkinter.Tk()
root.wm_title("RF DISP Modeller")
#### Embedding matplotib fig in TKiner canvas
#fig = Figure(figsize=(5, 4), dpi=100)
fig= plt.figure()

#### Getting the Cavas for the matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
#### Addig the matplotlib toolbar
toolbar = NavigationToolbar2Tk(canvas, root)
toolbar.update()
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
canvas.draw()

canvas.mpl_connect("key_press_event", on_key_press)





menubar = Menu(root)
## create a pulldown menu to load vel,RF,disp
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Open Velocity file", command=lambda:load_vel())
filemenu.add_command(label="Open Vp_Vs file", command=lambda:load_vp_vs())
filemenu.add_command(label="Open RF file", command=lambda:load_rf())
filemenu.add_command(label="Open Disp file", command=lambda:load_disp())
#filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Open", menu=filemenu)
menubar.add_command(label="Load LitMod Model", command=lambda:load_LitMod_model(vel,vp_vs))
menubar.add_command(label="Save Model", command=lambda:save())
menubar.add_command(label="Run Model", command=lambda:plot(vel,vp_vs,rf,disp,fig))
menubar.add_command(label="Quit", command=_quit)



helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
helpmenu.add_command(label="Help", command=hello)
menubar.add_cascade(label="Help", menu=helpmenu)




# display the menu
root.config(menu=menubar)


####################################################
### This connects the key press events in the matpplotlib


#button1 = tkinter.Button(master=root, text="Quit", command=_quit)
#button2 = tkinter.Button(master=root, text="Modify", command=_modify_model)
#button3 = tkinter.Button(master=root, text="Refresh", command=lambda:plot(vel,rf,disp,fig))



'''
# create more pulldown menus
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Cut", command=hello)
editmenu.add_command(label="Copy", command=hello)
editmenu.add_command(label="Paste", command=hello)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=hello)
'''
#menubar.add_cascade(label="Help", menu=helpmenu)


#button1 = tkinter.Button(master=root, text="Quit", command=_quit)
#button2 = tkinter.Button(master=root, text="Modify", command=_modify_model)
#button3 = tkinter.Button(master=root, text="Refresh", command=lambda:plot(vel,rf,disp,fig))

#button1.pack(side=tkinter.LEFT)
#button2.pack(side=tkinter.RIGHT)
#button3.pack(side=tkinter.RIGHT)

tkinter.mainloop()


# If you put root.destroy() here, it will cause an error if the window is
# closed with the window manager.
