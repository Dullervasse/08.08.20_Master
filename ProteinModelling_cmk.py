import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

# Initiating test
print("Hello, and welcome to this FoldX data processing program! :)")
print("This is the test for cmk.")

# set working directory to folder with FoldX output files
os.chdir("/Users/Marie/Desktop/DataCrunching/cmk")

# Import and clean up files
files = os.listdir()
i = 0
while i < len(files):
    if files[i][0:9] != "energies_":
        del(files[i])
    else:
        i += 1

# Identify and save position number for each file
numberList = []
for i in range(0, len(files)):
    number = re.search(r"\D(\d+)\D", files[i])
    numberList.append(number.group(1))
    
# Create pair lists with file and position number
PairList =[]
PositionTable = []
for i in range(0,len(files)):
    PairList.append([files[i],int(numberList[i])])
  
# Sort pair lists
PairList.sort(key = lambda x: x[1])
  
# Prepare data tables  
EnergyTable = []
LabelTable = []

# Lists for sorting mutations into three categories
MutSta = []
MutDes = []
MutNeu = []

# Processing of each file
for i in range(0,len(PairList)):
    
    # Identify and save position
    position = PairList[i][1]
    PositionTable.append(position)

    # Import table with energy reads, set index
    energies = pd.read_csv(PairList[i][0], header = None, delimiter = r"\s+")

    # Extract columns with names, clean up, and save
    AAnames = np.array(energies.iloc[:,0])
    AAnames[0] = "WTref"
    for s in range(1, len(AAnames)):
        AAnames[s] = AAnames[s][0:3] + str(position)
    LabelTable.append(AAnames)

    # Extract energies from file
    ddG = np.array(energies.iloc[:,1])

    # Calculating dddG values
    WTbase = float(ddG[0])
    dddG = []
    for r in range(0, len(ddG)):
        dddG.append(WTbase - float(ddG[r]))

    # Add data to table
    EnergyTable.append(dddG)
    
    # Sort mutations into categories
    stable = 0
    destable = 0
    neutral = 0
    for m in range(1, len(dddG)):
        if dddG[m] > 0.5:
            stable += 1
        elif dddG[m] < -0.5:
            destable += 1
        else:
            neutral += 1
    MutSta.append(stable)
    MutDes.append(destable)
    MutNeu.append(neutral)

##### Data visualisation

processing = True
while processing == True:
    
    print("Alright, what would you like to do?")
    print("1: Graph")
    print("2: Position data")
    print("3: Only destabilised")
    print("4: Exit")
    
    func = input("Please answer here (1/2/3/4): ")
    
    # Create bar chart over mutations
    if func == "1":

        n=len(PositionTable)
        st = np.array(MutSta)
        ds = np.array(MutDes)
        ne = np.array(MutNeu)
        ind=np.arange(n)
        width=1
        plt.rcParams["figure.figsize"] = (50,3)

        p1=plt.bar(ind,st,width,color="green")
        p2=plt.bar(ind,ds,width,color="red",bottom=st)
        p3=plt.bar(ind,ne,width,color="blue",bottom=st+ds)

        plt.title("Predicted stabilities of cmk mutants", fontsize = 12)
        plt.xticks(ind+width/2, PositionTable, fontsize = 12, rotation=90)
        plt.yticks(fontsize=12)
        plt.ylim([0,25])
        plt.legend((p1[0], p2[0], p3[0]), ('Stabilising', 'Destabilising', 'Neutral'), loc=2, fontsize=11, ncol=4, framealpha=0, fancybox=True)
        
        # Save figure
        save = input("Do you want to save the figure? (y/n): ")
        
        if save == "y":
            name = input("Name the file: ")
            plt.savefig(name + ".png")  
        else:
            pass

        plt.show()
        
    # Extract ddG data for specific positions
    elif func == "2":
        
        scan = input("Which position?: ")
        
        t = 0
        while PositionTable[t] != int(scan):
            t +=1
            
        for i in range(0, len(LabelTable[t])):
            print(LabelTable[t][i], "\t", round(EnergyTable[t][i],5))
            
        t = 0
    
    # Show only destabilised mutations
    elif func == "3":
    
        n=len(PositionTable)
        ds = np.array(MutDes)
        ind=np.arange(n)
        width=1
        plt.rcParams["figure.figsize"] = (50,3)

        p2=plt.bar(ind,ds,width,color="red")

        plt.title("Predicted stabilities of cmk mutants", fontsize = 12)
        plt.xticks(ind+width/2, PositionTable, fontsize = 12, rotation=90)
        plt.yticks(fontsize=12)
        plt.ylim([0,25])
        plt.savefig("cmk_destabilised", transparent = True, )
        
        save = input("Do you want to save the figure? (y/n): ")
        
        # Save figure
        if save == "y":
            name = input("Name the file: ")
            plt.savefig(name + ".png")  
        else:
            pass

        plt.show()
    
    # End script
    elif func == "4":
        processing = False
        
print("Goodbye!")
            
            



