import os
import pandas as pd
from matplotlib import pyplot as plt

os.chdir("/Users/Marie/Desktop/DataCrunching/Platereaders/Processing")

print("Hello, and welcome to this data visualisation and comparison program!")
print("Please enter the names of your excel files (remember .xlsx suffix).")

# Identify files
file1 = input("File number 1 (30C): ")
file2 = input("File number 2 (42C): ")

# Growth comparison
ask = input("Do you want a background comparison? (y/n): ")

BGgrowth = ""
if ask == "y":
    BGgrowth = input("Which one? MG1655 (m) or WT keio (k)?: ")
else:
    pass

# Read files
file30 = pd.read_excel(file1)
file42 =pd.read_excel(file2)

# Extract and edit names
names = list(file42.columns[2:])
names[0] = "A1 - MG1655"
names[12] = "B1 - KanS keio"
names[24] = "C1 - KanS keio + WT"

# Make x-axis
time = []
hours = 0
minutes = 0.0
for i in range(len(file42)-1):
    time += [hours + minutes]    
    minutes += 0.10
    if minutes == 0.60:
        hours += 1
        minutes = 0.0
time += [hours]

# Adjust figure size
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 30
fig_size[1] = 15
plt.rcParams["figure.figsize"] = fig_size

# Set limits
limit1 = 2
limit2 = 3

print("Plotting graphs. Please wait...")

# Plot graphs
for i in range(96):
    
    fig = plt.subplot(8,12,i+1)
    plt.tight_layout()
    
    if BGgrowth == "m":
        p1 = plt.plot(time, file30.iloc[:,2:3], color = "lightsteelblue")
        p2 = plt.plot(time, file42.iloc[:,2:3], color = "peachpuff")
    elif BGgrowth == "k":
        p1 = plt.plot(time, file30.iloc[:,26:27], color = "lightsteelblue")
        p2 = plt.plot(time, file42.iloc[:,26:27], color = "peachpuff")
    
    p3 = plt.plot(time, file30.iloc[:,limit1:limit2], color = "royalblue")
    p4 = plt.plot(time, file42.iloc[:,limit1:limit2], color = "orangered")
    plt.title(names[i], fontsize = 12)
    plt.ylim([0,0.8])
    plt.xlim([0,time[-1]])

    limit1 += 1
    limit2 += 1

# Adjust legend
if ask == "y":    
    leg = fig.legend((p1[0],p2[0],p3[0],p4[0]),("WT pyrF (30C)", "WT pyrF (42C)", "Mutant (30C)", "Mutant (42C)"), bbox_to_anchor=(-4.9,-0.5), loc="lower right", ncol=4)
else:
    leg = fig.legend((p3[0],p4[0]),("Growth 30C", "Growth 42C"), bbox_to_anchor=(-4.9,-0.5), loc="lower right", ncol=2)
for legobj in leg.legendHandles:
    legobj.set_linewidth(5.0)
 
save = input("Do you want to save the figure? (y/n): ")

if save == "y":
    name = input("Name the file: ")
    plt.savefig(name + ".png")  
else:
    pass

plt.show()