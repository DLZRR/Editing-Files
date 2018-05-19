import numpy as np
from astropy.io import fits


#garbage_data = np.loadtxt('ALESS_data_improved.txt', usecols = [0, 46, 47, 53, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 114, 115, 116, 117, 118, 119], skiprows = 1) 
# 0 id , 53 z_phot, 60 VIMOS starts, first all fluxes, then errors, except 46, 47  # 60-78 Fluxes # errors 79-98 # 99-104 are SPIRE BANDS, again flux, error, .... etc.
# 114-119 MIPS and PACS BANDS, flux, error, .... etc.

columns_to_use = [61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98]

columns_to_use2 = [46, 47, 114, 115, 116, 117, 118, 119, 99, 100, 101, 102, 103, 104, 30, 31]

hdul = fits.open('sources_aLESS_24jul2012_brightcal_M+S_IRAC_Radio_24+HSO+PACS_zspec.fits')


wavelengths = [3675.1, 3429, 3647, 4589, 5377, 6504, 8635, 9502.7, 12275.1, 12304.9, 12530, 16366.01, 21630.58, 21322.79, 21337.8, 35075.1, 44365.8, 56281.0, 75891.6, 232096.0, 684447.6, 979036.1, 1539451.3, 2428217.6, 3408914.0, 4822547.5, 8700000.0]



#hdul = fits.open(fits_image_filename)

var = hdul[1].data
#print var[1][-2]

no_redshift = []

array = np.zeros((len(var) + 1, len(wavelengths) * 2 + 2))

for i in range(len(var)):

    array[i+1][0] = float(var[i][0][5:]) # This is the ALESS id

    
    if var[i][-2] < 0. or var[i][-2] == 99.:

        if var[i][53] < 0. or var[i][53] == 99.:

            if var[i][54] < 0. or var[i][54] == 99.:

                array[i+1][1] = np.random.randint(1,5) # I should remove the source ideally, but I can print the source names later. Not ideal though
                #print(array[i+1][0])
                no_redshift.append(i+1)
            
            else:

                array[i+1][1] = var[i][54]

        else:
    
            array[i+1][1] = var[i][53]

    else:

        array[i+1][1] = var[i][-2]
    
    t = 0

    for j in range(2, 2 * (len(wavelengths) - 8) + 2, 2):

        if np.isnan(var[i][columns_to_use[t]]) or var[i][columns_to_use[t]] == 0.:
            
            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        elif var[i][columns_to_use[t]] > 100.:

            array[i+1][j] = -99.
            array[i+1][j+1] = -99.

        elif var[i][columns_to_use[t]] == -99.:

            array[i+1][j] = -99.
            array[i+1][j+1] = -99.
            
        elif var[i][columns_to_use[t+19]] == 0.:
            
            array[i+1][j] = 3631. * 10.**(-var[i][columns_to_use[t]]/2.5)
            array[i+1][j+1] = 3631. * 10.**(-var[i][columns_to_use[t]]/2.5) / 10.

        else:

            # The conversion from magnitude AB to flux in Jansky

            array[i+1][j] = 3631. * 10.**(-var[i][columns_to_use[t]]/2.5)
            array[i+1][j+1] = var[i][columns_to_use[t + 19]] * 3631./2.5 * np.log(10.) * 10.**(-var[i][columns_to_use[t]]/2.5)
            
            if array[i+1][j] == 0. or array[i+1][j]>1.:
            
                print(var[i][columns_to_use[t]])
                print(array[i+1][j+1])
                
            if array[i+1][j+1]/array[i+1][j] < 0.1:
            
                array[i+1][j+1] = array[i+1][j]/10.
                
        #if array[i+1][j] > -98. and array[i+1][j] < 1.e-7:
            
        #            print(array[i+1][j])
        #            print(array[i+1][j+1])
            # It may very well be possible that they are in micro Jansky, I will try that here. Not true, quite sure it is magnitude AB
            
            #array[i+1][j] = var[i][columns_to_use[t]] * 1.e-6
            #array[i+1][j+1] = var[i][columns_to_use[t + 19]] * 1.e-6
 
        
        #array[i+1][j+2] = wavelengths[t]

        t += 1

        #print t-1

        #print 'j is', j

    t = 0

    x = 0
    
    for s in range(2 * (len(wavelengths) - 8) + 2, 2 * len(wavelengths) + 2, 2):
        
        if np.isnan(var[i][columns_to_use2[t]]) or (var[i][columns_to_use2[t]] == 0. and var[i][columns_to_use2[t + 1]] == 0.):
        
            array[i+1][s] = -99.
            array[i+1][s+1] = -99.
            
        elif np.isnan(var[i][columns_to_use2[t+1]]):
            
            array[i+1][s] = var[i][columns_to_use2[t]] * 1.e-3
            array[i+1][s+1] = var[i][columns_to_use2[t]] * 1.e-4

        elif var[i][columns_to_use2[t]] == -99.:

            array[i+1][s] = -99.
            array[i+1][s+1] = -99.

        else:

            array[i+1][s] = var[i][columns_to_use2[t]] * 1.e-3
            array[i+1][s+1] = var[i][columns_to_use2[t+1]] * 1.e-3 

            '''
            if x + len(wavelengths) - 8 == 23 or x + len(wavelengths) - 8 == 24 or x + len(wavelengths) - 8 == 25 or x + len(wavelengths) - 8 == 26:

                #print(x + len(wavelengths) - 8)
                array[i+1][s] = var[i][columns_to_use2[t]] * 1.e-3
                array[i+1][s+1] = var[i][columns_to_use2[t+1]] * 1.e-3

            # These values should be in flux Jansky
        
            elif s != 3 * (len(wavelengths) - 8) + 2:

                array[i+1][s] = 3631. * 10.**(-var[i][columns_to_use2[t]]/2.5)
                array[i+1][s+1] = var[i][columns_to_use2[t + 1]] * 3631./2.5 * np.log(10.) * 10.**(-var[i][columns_to_use2[t]]/2.5)

                #print array[2][s+1]

                if array[i+1][s+1] <= 0.:

                    array[i+1][s+1] = array[i+1][s] / 10.

            else:

                array[i+1][s] = var[i][columns_to_use2[t]] * 1.e-3
                array[i+1][s+1] = var[i][columns_to_use2[t+1]] * 1.e-3 
            '''
        
        #array[i+1][s+2] = wavelengths[x + len(wavelengths) - 8]

        #print t
        
        if array[i+1][s+1]/array[i+1][s] < 0.1:
            
            array[i+1][s+1] = array[i+1][s] / 10.
        
        
        x += 1
        t += 2

        #print x + len(wavelengths) - 7

        #print 's is', s

    for x in range(2 * (len(wavelengths) - 8) + 2, 2 * len(wavelengths) + 2, 1):
        
                if array[i+1][x] > -98. and array[i+1][x] < 1.e-7:
            
                    #print(array[i+1][x])
                    print(1)
                    #array[i+1][x] = -99.
                    #print(array[i+1][x])  

#print(array[1])
#print(array[6])
#print len(array[0])
#print np.arange(2, 56, 2).tolist()


#for i in range(0, 2*len(wavelengths), 1):
    
#    print array[len(var)-3][i], " i is ", i

tp = tuple(no_redshift)
array = np.delete(array, tp, axis=0)

    

np.savetxt('ALESS_TRUE_DATA.txt', array)
