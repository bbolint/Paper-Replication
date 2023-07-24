import numpy as np
import pandas as pd

df = pd.read_csv('wikipedia_edges.csv') #reading the .csv file from a local location. 

#CREATE TUPLES FROM NODE A TO B AND VICE VERSA FOR ALL EDGES AB
df['onward'] = df[['from', 'to']].apply(tuple, axis=1)
df['backward'] = df[['to', 'from']].apply(tuple, axis=1)

#Find the overlap between onward and backward arrays. The overlap will give the array of all bidirectional edges
intersect, ind_a, ind_b = np.intersect1d(df['onward'], df['backward'], return_indices=True)

""" intersect gives the list of bidirectional edges
ind_a gives the indices of onward overlapping edges
ind_b gives the indices of backward overlapping edges """

Ppp, Ppn, Pnp, Pnn = (0 for x in range(4))

err = 0 #Initializing a variable to find all discrepencies such as non 1 or -1 sign and same timestamp for both direction edges

""" The idea for finding probabilities is the following:
    
    If multiplication of the signs is 1, that means both edges are of same sign. In which case, we just check sign of one, and assign it to P(p|p) (Ppp) or P(n|n) (Pnn) respectively
    
    If the multiplication of the signs is -1, then we check the sign of the edge that was formed earlier. Based on this we assign it to either P(p|n) (Ppn) or P(n|p) (Pnp).
    
    Since, we are iterating thorugh the whole list, we count each edge twice. Hence to get the actual numbers, we finally divide all the counters by 2. """

for i in range(len(intersect)): #iterate through all bidirectional edges
    
    #Find indices of the bidirected edges in the original dataframe
    k1 = df.index[df['backward'] == intersect[i]].tolist()[0]
    k2 = df.index[df['onward'] == intersect[i]].tolist()[0]

    #Check for discrepencies
    if((df['timestamp'][k1] == df['timestamp'][k2]) or (df['sign'][k1]!= 1 and df['sign'][k1]!= -1) or (df['sign'][k2]!= 1 and df['sign'][k2]!= -1) ):
        print(df['sign'][k1],df['sign'][k2])
        print(df['timestamp'][k1],df['timestamp'][k2])
        err+=1

    else:
        if(df['sign'][k1]*df['sign'][k2] == 1):
            if(df['sign'][k1]==1):
                Ppp+=1
            elif(df['sign'][k2]==-1):
                Pnn+=1
        
        else:
            if(df['timestamp'][k1] < df['timestamp'][k2]):
                if(df['sign'][k1]==1):
                    Pnp+=1
                else:
                    Ppn+=1
            elif(df['timestamp'][k1] > df['timestamp'][k2]):
                if(df['sign'][k1]==1):
                    Ppn+=1
                else:
                    Pnp+=1
    # print(str(i)+' is done.')

P_tot = Ppp+Pnp #total edges with first one positive
N_tot = Pnn+Ppn #total edges with first one negative

#Write the results into a textfile
file = open("Recipro_stat.txt", "w")
file.write('Wikipedia \n\n')
file.write('P(p|p)= '+str(Ppp)+', fraction= '+str(Ppp/(P_tot))+'\n')
file.write('P(n|p)= '+str(Pnp)+', fraction= '+str(Pnp/(P_tot))+'\n')
file.write('P(p|n)= '+str(Ppn)+', fraction= '+str(Ppn/(N_tot))+'\n')
file.write('P(n|n)= '+str(Pnn)+', fraction= '+str(Pnn/(N_tot))+'\n')

file.write('Total Edges='+str((P_tot+N_tot)/2)+'\n')
file.write('Discrepencies/Errors = '+str(err/2)+'\n')

file.close()

############# END OF CODE ##############################