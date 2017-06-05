def plate_read(*args):
    with open('raw.csv','r') as file_input: #read the full data
        raw_data = file_input.read()

    cycles= ['Cycles'+x for x in raw_data.split('Cycle')] #split the raw_data by cicle
    experiment = cycles[0] #create the experiment ID
    #print cycles
    try:#corrects data processing by windows
        cycles_new = cycles[:-1] + [cycles[-1].split('\r\n\r\nRaw')[0]]+['Cycles 1 (0.0 h)\r\nRaw'+cycles[-1].split('\r\n\r\nRaw')[1]] #processed list for last entry which does not contain cycle header
    except:
        cycles_new = cycles[:-1] + [cycles[-1].split('\n\nRaw')[0]]+['Cycles 1 (0.0 h)\nRaw'+cycles[-1].split('\n\nRaw')[1]] #processed list for last entry which does not contain cycle header
    cycles_split  = []
    cycles_header = []
    for cycle in cycles_new[1:]: #this will split every cycle into matrix of 8x12 with str values of OD
        try: #corrects data processing by windows
            cycles_split.append([x[2:].split(',') for x in cycle.split('\r\n\r\n')[1].split()][1:])
            cycles_header.append(''.join([x for x in cycle.split('\r\n\r\n')[0]]))
        except:
            cycles_split.append([x[2:].split(',') for x in cycle.split('\n\n')[1].split()][1:])
            cycles_header.append(''.join([x for x in cycle.split('\n\n')[0]]))
    # create reversed list of entries
    cycles_split  = cycles_split [::-1]
    cycles_header = cycles_header[::-1]

    return experiment,cycles_header, cycles_split

def well_read(*args):
    exp, header, cycle  = plate_read()
    well_data           = []
    time                = ['Time']
    every_well          = []

    for i in range(8): #creates a list of possibilities for experiment matrix
        for j in range(12):
            every_well.append([i,j])

    for i in header: # extract time in minutes from cycle header
        time.append(str(round(60*(float(i.split()[2][1:])),2)))


    for row,column in every_well:
        ltn = list('ABCDEFGH')
        well_str = ltn[row]+str(column+1) # create a string with human readable well position
        well = [well_str]
        for i in cycle: # extract the well info from every cycle
            well.append(i[row][column])
        well_data.append(well)
    out = [time]+well_data # writes the full matrix of data and times
    import csv

    with open('text.csv', 'w') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerows(zip(*out)) # writes the file in csv with time, data and human readable wells
    print "\n\nProcessing data from SPECTROStar plate reader. \nThe running experiment is described as:\n\n "
    print exp

well_read()
