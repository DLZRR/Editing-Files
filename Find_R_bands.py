import numpy as np
import scipy.io
import matplotlib.pyplot as plt

array = np.zeros((225-33, 34))

filter_wavelengths = [3595, 4640, 6122, 6440, 16620, 35075, 44366, 56281, 75892, 232096, 684448, 1525902, 2428218, 3408914, 4822548, 11991798] # Effective wavelengths from filter website 610 and 20cm need to be added (16500 is h, taken from wikipedia), 119917898 needs to be replaced with a better effective wavelength


SDSS = scipy.io.readsav('MULTIWAVE_allfluxes_final.sav')

threshold = 100
#print SDSS['fr'][0]
#print SDSS.keys()

#key_names = ['f3', 'f4', 'f5', 'f8', 'f160', 'f70', 'df610', 'df20cm', 'smam', 'zs', 'df350', 'df250', 'dfu', 'dfr', 'epoch', 'dfh', 'f24', 'dfg', 'fr', 'f610', 'df160', 'fu', 'df70', 'rmag', 'f350', 'fg', 'fh', 'mips', 'f500', 'df8', 'df500', 'df5', 'df4', 'f250', 'df3', 'f20cm', 'df24', 'dsmam', 'ew7']

key_names = ['fu', 'dfu', 'fg', 'dfg', 'fr', 'dfr', 'fh', 'dfh', 'f3', 'df3', 'f4', 'df4', 'f5', 'df5', 'f8', 'df8', 'f24', 'df24', 'f70', 'df70', 'f160', 'df160', 'f250', 'df250', 'f350', 'df350', 'f500', 'df500', 'smam', 'dsmam'] # Have not added h band yet drmag does not actually exist, just to make sure program does not whine about this

array = np.zeros((len(SDSS['fg'])+1, len(key_names)+2))

#print SDSS['fu'][0]

#SDSS['fu'] *= 1e-3
#SDSS['dfu'] *= 1e-3
#SDSS['fg'] *= 1e-3
#SDSS['dfg'] *= 1e-3
#SDSS['fr'] *= 1e-3
#SDSS['dfr'] *= 1e-3
#SDSS['fh'] *= 1e-3
#SDSS['dfh'] *= 1e-3 
SDSS['f3'] *= 1e-3
SDSS['df3'] *= 1e-3
SDSS['f4'] *= 1e-3
SDSS['df4'] *= 1e-3
SDSS['f5'] *= 1e-3
SDSS['df5'] *= 1e-3
SDSS['f8'] *= 1e-3
SDSS['df8'] *= 1e-3 


for i in range(0, len(SDSS['fg']), 1): #len(SDSS['fg'])

    array[i+1][0] = SDSS['mips'][i]
    
    array[i+1][1] = SDSS['zs'][i]
    #print SDSS['mips'][i]
    #print

    for j in range(2, 10, 2):

        #print j

        #print SDSS[key_names[j-2]][i]
        
        
        if SDSS[key_names[j-2]][i] == 0.:

            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        elif SDSS[key_names[j-2]][i] > threshold:

            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

            
        elif SDSS[key_names[j-2]][i] < 1.e-9:
            
            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        else:

            array[i+1][j] = SDSS[key_names[j-2]][i] 
            array[i+1][j+1] = SDSS[key_names[j-2]][i]/10.
            
            #array[i+1][8]

            #print array[i+1][j]

    #print array[i+1][j]

    for j in range(10, len(key_names) + 2, 2):

        #print j

        if SDSS[key_names[j-2]][i] == 0. and SDSS[key_names[j-1]][i] == 0.:

            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        elif SDSS[key_names[j-1]][i] > threshold and SDSS[key_names[j-2]][i] > threshold:

            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        elif SDSS[key_names[j-2]][i] > threshold and SDSS[key_names[j-1]][i] == 0.:

            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        elif SDSS[key_names[j-1]][i] > threshold:

            array[i+1][j] = SDSS[key_names[j-1]][i]
            array[i+1][j+1] = SDSS[key_names[j-1]][i] / 10.
            
        elif SDSS[key_names[j-2]][i] < 1.e-8 and SDSS[key_names[j-1]][i] < 1.e-9:
            
            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        else:

            array[i+1][j] = SDSS[key_names[j-2]][i] 
            array[i+1][j+1] = SDSS[key_names[j-1]][i]
            
            if SDSS[key_names[j-1]][i]/SDSS[key_names[j-2]][i] < 0.1:
            
                array[i+1][j+1] = SDSS[key_names[j-2]][i]/10.
            
    for x in range(2, len(key_names) + 2, 2):
        
                if array[i+1][x] > 1000. or array[i+1][x] < 1.e-7:
            
                    print(array[i+1][x+1])
                    #array[i+1][x] = -99.
                    #print(array[i+1][x])   

print(array[2])
print(len(key_names)+2)
print(np.arange(2,32,2).tolist())

np.savetxt('something_new_new.txt', array)

