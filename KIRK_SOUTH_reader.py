import numpy as np
import gvar


infrared = np.loadtxt('infraredgoodssouthnew.txt', usecols=[0,2,3,4,5,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]) # 20, 21 PACS 70

#infraredPACS = np.loadtxt('infraredgoodssouthnew.txt', usecols=[0,20,21]) # 20, 21 PACS 70

optical = np.loadtxt('KIRKWITHGOODS.txt', skiprows=1, usecols=[0,3,13,14,16,17,19,20,22,23,25,26,28,29,31,32,34,35,37,38,40,41,43,44,46,47,49,50,52,53,55,56,58,59,61,62])

infrarednew = np.loadtxt('infraredgoodssouthnew.txt', usecols=[0,2,3,4,5,6,7,8,9,10,11,12,13]) # 20, 21 PACS 70
array = np.zeros((len(optical)+1, len(optical[0])+len(infrared[0])-1))




for i in range(len(optical)):

    for j in range(len(infrared)):
        
        if optical[i][0] == infrared[j][0]:

            #print optical[i][0]

            array[i+1][0] = optical[i][0]
            array[i+1][1] = optical[i][1]
            
            for s in range(2, len(optical[0]), 2):
    
                array[i+1][s] = optical[i][s]
                array[i+1][s+1] = optical[i][s]/10.
                
                #array[i+1][s] = -99.
                #print(s)

            #print('Max s is:', len(optical[0]))

            #array[i+1][len(optical[0])-8] = infrarednew[j][6-1]
            #array[i+1][len(optical[0])-7] = infrarednew[j][7-1]
            #array[i+1][len(optical[0])-7] = infrarednew[j][6-1]/10.
            #array[i+1][len(optical[0])-6] = infrarednew[j][8-1]
            #array[i+1][len(optical[0])-5] = infrarednew[j][9-1]
            #array[i+1][len(optical[0])-7] = infrarednew[j][8-1]/10.
            #array[i+1][len(optical[0])-4] = infrarednew[j][10-1]
            #array[i+1][len(optical[0])-3] = infrarednew[j][11-1]
            #array[i+1][len(optical[0])-7] = infrarednew[j][10-1]/10.
            #array[i+1][len(optical[0])-2] = infrarednew[j][12-1]
            #array[i+1][len(optical[0])-1] = infrarednew[j][13-1]
            #array[i+1][len(optical[0])-7] = infrarednew[j][12-1]/10.

            for t in range(1, len(infrared[0])-12, 2):

                array[i+1][t+len(optical[0])-1] = infrared[j][t]
                array[i+1][t+len(optical[0])] = infrared[j][t+1]
                
                #array[i+1][t+len(optical[0])-1] = -99.
                
                #array[i+1][t+len(optical[0])] = -99.
                
                if infrared[j][t+1]/infrared[j][t] < 0.1:
                    
                    array[i+1][t+len(optical[0])] = infrared[j][t]/10.
                    
                #print t
                #print len(infrared[0])-12
                #print(infrared[0][t])

            #print('Max t is:', len(infrared[0])-12)

            for x in range(len(infrared[0])-12, len(infrared[0]), 2):

                if infrared[j][x] == -99. or infrared[j][x+1] == -99.:
            
                    array[i+1][x+len(optical[0])-1] = -99.
                    array[i+1][x+len(optical[0])] = -99.

                elif infrared[j][x] == 0. and infrared[j][x+1] == 0.:

                    array[i+1][x+len(optical[0])-1] = -99.
                    array[i+1][x+len(optical[0])] = -99.

                else:
    
                    array[i+1][x+len(optical[0])-1] = infrared[j][x] * 1.e3
                    array[i+1][x+len(optical[0])] = infrared[j][x+1] * 1.e3
                    
                    if infrared[j][x+1]/infrared[j][x] < 0.1:
                        
                        array[i+1][x+len(optical[0])] = infrared[j][x] * 1.e3 / 10.
                
            if array[i+1][len(optical[0])-1+len(infrared[0])-14] > 0. and array[i+1][len(optical[0])-1+len(infrared[0])-12] > 0.:
                
                #print optical[i][0]
                #print 111
                #print array[i+1][len(optical[0])-1+len(infrared[0])-10]
                #print array[i+1][len(optical[0])-1+len(infrared[0])-11]
                #print array[i+1][len(optical[0])-1+len(infrared[0])-12]
                #print array[i+1][len(optical[0])-1+len(infrared[0])-13]
                
                x = gvar.gvar(array[i+1][len(optical[0])-1+len(infrared[0])-14], array[i+1][len(optical[0])-1+len(infrared[0])-14+1] )
                y = gvar.gvar(array[i+1][len(optical[0])-1+len(infrared[0])-14+2], array[i+1][len(optical[0])-1+len(infrared[0])-14+3] )

                z = (x + y) / 2.

                array[i+1][len(optical[0])-1+len(infrared[0])-14] = z.mean
                array[i+1][len(optical[0])-1+len(infrared[0])-14+1] = z.sdev
                
                #array[i+1][len(optical[0])-1+len(infrared[0])-14] = (array[i+1][len(optical[0])-1+len(infrared[0])-14] + array[i+1][len(optical[0])-1+len(infrared[0])-14+2]) / 2.
                #array[i+1][len(optical[0])-1+len(infrared[0])-14+1] = array[i+1][len(optical[0])-1+len(infrared[0])-14] / 8.
                #print array[i+1][len(optical[0])-1+len(infrared[0])-14]  max(array[i+1][len(optical[0])-1+len(infrared[0])-14+1]-)
                #array[i+1][len(optical[0])-1+len(infrared[0])-12+1] = (array[i+1][len(optical[0])-1+len(infrared[0])-12+1] + array[i+1][len(optical[0])-1+len(infrared[0])-12+2+1]) / 2.
                
                array[i+1][len(optical[0])-1+len(infrared[0])-14+2] = -99.
                array[i+1][len(optical[0])-1+len(infrared[0])-14+2+1] = -99.
                
                #print len(infrared[0])-12

            #print(infrared[j][x+1])

print(array[1])
#print(len(array[1]))
#print(np.arange(2, 54, 2).tolist())
#print(np.arange(3, 54, 2).tolist())

np.savetxt('KIRKSGOODS_70.txt', array)
