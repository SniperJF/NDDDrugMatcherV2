#This script opens the csv files that Dr. Cummings modified to classify the intervention type and generate text files with each category
#Run as: 
#time python3 csvClassifier.py
#TODO add as command line argument option to run with all tolower or without (case insesitive vs sensitive)

import csv 
#Functions
def writeListToFileSorted(dataToWrite, fdir, fname): #Small function to write to a file a list of sorted items
    sortedData = sorted(dataToWrite)
    f = open(fdir + fname + ".txt", "w")
    for entry in sortedData:
        f.write(entry)
        f.write("\n")
    f.close()

def processFile(fname):
    interventions = []
    with open("input/" + fname + ".csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            if row[0] != '':
                interventions.append([ row[0],row[12] ]) #Case Sensitive Version
                #interventions.append([ row[0].lower(),row[12] ]) #Lower Case Version (case insensitive)
    return interventions[2:] #Skip first 2 rows

#This one reads for table 10 which has multiple interventions in the same line so let's split them up
def processFileWithMult(fname):
    mixedInterventions = processFile(fname)
    separatedInterventions = []
    for entry in mixedInterventions:
        splitEntry = entry[0].split(", ")
        for subEntry in splitEntry:
            separatedInterventions.append([ subEntry,entry[1] ]) #Case Sensitive Version
            #separatedInterventions.append([ subEntry.lower(),entry[1] ]) #Lower Case Version (case insensitive)
    return separatedInterventions



#Globals
keyword_behaviors  = {'bejhav', 'behv', 'berhav', 'behav'}
keyword_biomarkers = {'biom', 'bioom', 'biomark'}
keyword_drugs      = {'dug', 'drg', 'drug'}
keyword_device     = {'device', 'deice'}
keyword_stemcells  = {'stem', 'sem'}
keyword_supplement = {'suppl', 'sduppl'}
keyword_delete     = {'delete'}
keyword_unknown    = {''}

#Function prints out how we did classifying stuff
def printTemetry(interventions):
    intClasses = set()
    for entry in interventions:
            intClasses.add(entry[1]) 
    newIntClasses = set()
    #print("Current Classes:", intClasses)
    print("Classifying into:")
    print("behaviors, biomarkers, drugs, devices, stemcells, supplements, delete,")
    print("and unknown")
    for i in intClasses:
        if (i not in keyword_behaviors     and i not in keyword_biomarkers 
            and i not in keyword_drugs     and i not in keyword_device 
            and i not in keyword_delete    and i not in keyword_unknown
            and i not in keyword_stemcells and i not in keyword_supplement ):
            newIntClasses.add(i)
    if len(newIntClasses) != 0:
        print("\nNew Classes: ",newIntClasses)
    else:
        print("\nAll Classes accounted for!")

#Check for interventions showing up in both classes
def printPartialIntercepts(be,bi,dr,dev,st,su,dele,un):
    classname = ['behaviors','biomarkers','drugs', 'devices', 'stemcells', 'supplements', 'delete list', 'unknown']
    allclasses = []
    allclasses.append(be)   #behaviors
    allclasses.append(bi)   #biomarkers
    allclasses.append(dr)   #drugs
    allclasses.append(dev)  #devices
    allclasses.append(st)   #stem cells
    allclasses.append(su)   #supplements
    allclasses.append(dele) #delete list
    allclasses.append(un)   #unknown
    
    allintercepts = []

    for i in range(0, len(allclasses)-1):
        for j in range(i+1,len(allclasses)):
            curr_intercepts = set.intersection(allclasses[i], allclasses[j])
            if len(curr_intercepts) > 0: #we found some intercepts
                for curr in curr_intercepts:
                    allintercepts.append([curr, classname[i], classname[j]])

    if len(allintercepts) > 0:
        print("Warning! Intercepts found for the following Interventions:")
        for entry in allintercepts:
            print(entry[0]+" "+entry[1]+"/"+entry[2])


#Main
def main():
    #Code 
    biomarkers = set()
    devices    = set()
    behaviors  = set()
    drugs      = set()
    stemcells  = set()
    deleteList = set()
    supplement = set()
    unknown     = set()

    interventions  = processFile("NDDCrossTable9HyperLinked.jlc.060521")
    interventions += processFileWithMult("NDDCrossTable10HyperLinked.jlc")
    interventions += processFile("ManualExtraClasses")

    printTemetry(interventions)

    #Time To Classify
    for i in interventions:
        if i[1] in keyword_behaviors:
            behaviors.add(i[0])
        elif i[1] in keyword_biomarkers:
            biomarkers.add(i[0])
        elif i[1] in keyword_drugs:
            drugs.add(i[0])
        elif i[1] in keyword_device:
            devices.add(i[0])
        elif i[1] in keyword_stemcells:
            stemcells.add(i[0])
        elif i[1] in keyword_supplement:
            supplement.add(i[0])
        elif i[1] in keyword_delete:
            deleteList.add(i[0])
        elif i[1] in keyword_unknown:
            unknown.add(i[0])
        else:
            print("Warning: No Class found for this label: " + i[1])

    #Next find the intercept of all sets to see if something shows up in 2 classes
    printPartialIntercepts(behaviors, biomarkers, drugs, devices, stemcells, supplement, deleteList, unknown)

    #Next write our output files with the classes each intervention belongs to
    writeListToFileSorted(behaviors, "output/", "behaviors-class")
    writeListToFileSorted(biomarkers, "output/", "biomarkers-class")
    writeListToFileSorted(drugs, "output/", "drugs-class")
    writeListToFileSorted(devices, "output/", "devices-class")
    writeListToFileSorted(stemcells, "output/", "stemcells-class")
    writeListToFileSorted(supplement, "output/", "supplement-class")
    writeListToFileSorted(deleteList, "output/", "deleteList-class")
    writeListToFileSorted(unknown, "output/", "unknown-class")
#End main()

if __name__ == "__main__":
    main()

