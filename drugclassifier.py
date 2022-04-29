#This is the classification part of program
from common import jfc
import tablegeneration as jft


#Function creates File with all drugname/interventions that appear in a given CTO set list. 
#Second parameter is name of file
def printAllInterventions(CTOs, fname):
    allInterventions = set()
    for entry in CTOs:
        allInterventions.add(entry.drugname)
    #Now write to a file
    sortedAllInterventions = sorted(allInterventions, key=None, reverse=False)
    f = open("output/" + fname + ".txt", "w")
    for entry in sortedAllInterventions:
        f.write(entry)
        f.write("\n")
    f.close()
    #At this point I can change function to return either a set: allInterventions or a sorted list: sortedAllInterventions
    #return allInterventions, sortedAllInterventions #Should the need arise to work with either of them

#functions to read in the input files containing what interventions belong to what class.
def readFileAsSet(fname):
    filecontents = set()
    f = open(fname, "r")
    for line in f:
        line = line.strip('\n')
        if line != '':
            filecontents.add(line.lower()) #Add everything lowercased (will be useful for string matching later)
    f.close()
    return filecontents

def writeToFileSorted(data, fname):
    sortedData = sorted(fname, key=None, reverse=False)
    f = open("output/" + fname + ".txt", "w")
    for entry in sortedData:
        f.write(entry)
        f.write("\n")
    f.close()    

def readClassifierFiles(): #NEW
    #Will Hold: drugs, biomarkers, devices, behaviors, stemcells, supplements, to_delete (in that order)
    drugClassifiers = {} #7 groups
    drugClassifiers["drugs"]       = readFileAsSet("input/classifiers/drugs-class.txt")
    drugClassifiers["biomarkers"]  = readFileAsSet("input/classifiers/biomarkers-class.txt")
    drugClassifiers["devices"]     = readFileAsSet("input/classifiers/devices-class.txt")
    drugClassifiers["behaviors"]   = readFileAsSet("input/classifiers/behaviors-class.txt")
    drugClassifiers["stemcells"]   = readFileAsSet("input/classifiers/stemcells-class.txt")
    drugClassifiers["supplements"] = readFileAsSet("input/classifiers/supplement-class.txt")
    drugClassifiers["deleteList"]  = readFileAsSet("input/classifiers/deleteList-class.txt")

    subdrugClassifiers = {} #2 groups:  Symptomatic Drugs and Disease Modifying Drugs
    subdrugClassifiers["sx-drugs"] = readFileAsSet("input/classifiers/sx-subclass.txt")
    subdrugClassifiers["dm-drugs"] = readFileAsSet("input/classifiers/dm-subclass.txt")   
    return drugClassifiers, subdrugClassifiers

def printClassifiedCTOs(CTOsList1, CTOsList2, CTOsList3, CTOsList4, subCTOsList1, subCTOsList2, subCTOsList3, subCTOsList4):
    if len(CTOsList1) != 8 or len(CTOsList2) != 8 or len(CTOsList3) != 8 or len(CTOsList4) != 8:
        print("Error: printClassifidCTOs: CTosLists not correct size") #Eight Groups
        return
    printAllInterventions(CTOsList1["drugs"]+CTOsList2["drugs"]+
                          CTOsList3["drugs"]+CTOsList4["drugs"],             "classified-tables/drugs")
    printAllInterventions(CTOsList1["biomarkers"]+CTOsList2["biomarkers"]+
                          CTOsList3["biomarkers"]+CTOsList4["biomarkers"],   "classified-tables/biomarkers")
    printAllInterventions(CTOsList1["devices"]+CTOsList2["devices"]+
                          CTOsList3["devices"]+CTOsList4["devices"],         "classified-tables/devices")
    printAllInterventions(CTOsList1["behaviors"]+CTOsList2["behaviors"]+
                          CTOsList3["behaviors"]+CTOsList4["behaviors"],     "classified-tables/behaviors")
    printAllInterventions(CTOsList1["stemcells"]+CTOsList2["stemcells"]+
                          CTOsList3["stemcells"]+CTOsList4["stemcells"],     "classified-tables/stemcells")
    printAllInterventions(CTOsList1["supplements"]+CTOsList2["supplements"]+
                          CTOsList3["supplements"]+CTOsList4["supplements"], "classified-tables/supplements")
    printAllInterventions(CTOsList1["deleteList"]+CTOsList2["deleteList"]+
                          CTOsList3["deleteList"]+CTOsList4["deleteList"],   "classified-tables/deleteList")
    printAllInterventions(CTOsList1["unknownList"]+CTOsList2["unknownList"]+
                          CTOsList3["unknownList"]+CTOsList4["unknownList"], "classified-tables/unknownList")

    printAllInterventions(subCTOsList1["sx-drugs"]+subCTOsList2["sx-drugs"]+
                          subCTOsList3["sx-drugs"]+subCTOsList4["sx-drugs"], "classified-tables/sx-drugs")
    printAllInterventions(subCTOsList1["dm-drugs"]+subCTOsList2["dm-drugs"]+
                          subCTOsList3["dm-drugs"]+subCTOsList4["dm-drugs"], "classified-tables/dm-drugs")
    printAllInterventions(subCTOsList1["unknownList"]+subCTOsList2["unknownList"]+
                          subCTOsList3["unknownList"]+subCTOsList4["unknownList"], "classified-tables/unknownList-subclass")

def createFinalTables(CTOsListIT, CTOsListST, CTOsListSTEC1, CTOsListSTEC2, 
                      subCTOsListIT, subCTOsListST, subCTOsListSTEC1, subCTOsListSTEC2):
    if len(CTOsListIT) != 8 or len(CTOsListST) != 8: #we want 4 groups
        print("Error: createFinalTables:  CTosLists not correct size")
        return    
    #Independent Trial Tables
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table1Title,  CTOsListIT["drugs"]) ,       "final-tables/NDDCrossTable1")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table3Title,  CTOsListIT["biomarkers"]) ,  "final-tables/NDDCrossTable3")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table5Title,  CTOsListIT["devices"]) ,     "final-tables/NDDCrossTable5")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table7Title,  CTOsListIT["behaviors"]) ,   "final-tables/NDDCrossTable7")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table9Title,  CTOsListIT["stemcells"]) ,   "final-tables/NDDCrossTable9")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table11Title, CTOsListIT["supplements"]) , "final-tables/NDDCrossTable11")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table13Title, CTOsListIT["deleteList"]) ,  "final-tables/NDDCrossTable13")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table15Title, CTOsListIT["unknownList"]) , "final-tables/NDDCrossTable15")

    #Single Trial Tables
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table2Title,  CTOsListST["drugs"]) ,       "final-tables/NDDCrossTable2")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table4Title,  CTOsListST["biomarkers"]) ,  "final-tables/NDDCrossTable4")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table6Title,  CTOsListST["devices"]) ,     "final-tables/NDDCrossTable6")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table8Title,  CTOsListST["behaviors"]) ,   "final-tables/NDDCrossTable8")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table10Title, CTOsListST["stemcells"]) ,   "final-tables/NDDCrossTable10")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table12Title, CTOsListST["supplements"]) , "final-tables/NDDCrossTable12")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table14Title, CTOsListST["deleteList"]) ,  "final-tables/NDDCrossTable14")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table16Title, CTOsListST["unknownList"]) , "final-tables/NDDCrossTable16")

    #Subclassification Tables Independent Trials
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table17Title, subCTOsListIT["sx-drugs"]) ,    "final-tables/NDDCrossTable17")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table19Title, subCTOsListIT["dm-drugs"]) ,    "final-tables/NDDCrossTable19")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table31Title, subCTOsListIT["unknownList"]) , "final-tables/NDDCrossTable31")    
    #Subclassification Tables Single Trials
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table18Title, subCTOsListST["sx-drugs"]) ,    "final-tables/NDDCrossTable18")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table20Title, subCTOsListST["dm-drugs"]) ,    "final-tables/NDDCrossTable20")
    jft.createCSVfromTable( jft.generateTableFromCTOs(jft.Table32Title, subCTOsListST["unknownList"]) , "final-tables/NDDCrossTable32")

    #Eligibility Criteria Flagged Tables:
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table21Title, CTOsListSTEC1["drugs"]) ,          "final-tables/NDDCrossTable21")
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table22Title, CTOsListSTEC2["drugs"]) ,          "final-tables/NDDCrossTable22")
    nondrugsEC1 = (CTOsListSTEC1["biomarkers"]+CTOsListSTEC1["devices"]+CTOsListSTEC1["behaviors"]
                  +CTOsListSTEC1["stemcells"]+CTOsListSTEC1["supplements"]+CTOsListSTEC1["deleteList"]+CTOsListSTEC1["unknownList"])
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table23Title, nondrugsEC1) ,                     "final-tables/NDDCrossTable23")
    nondrugsEC2 = (CTOsListSTEC2["biomarkers"]+CTOsListSTEC2["devices"]+CTOsListSTEC2["behaviors"]
                  +CTOsListSTEC2["stemcells"]+CTOsListSTEC2["supplements"]+CTOsListSTEC2["deleteList"]+CTOsListSTEC2["unknownList"])
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table24Title, nondrugsEC2) ,                     "final-tables/NDDCrossTable24")
    #Subclassification for Eligibility Criteria Flagged Trials
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table25Title, subCTOsListSTEC1["sx-drugs"]) ,    "final-tables/NDDCrossTable25")
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table26Title, subCTOsListSTEC1["dm-drugs"]) ,    "final-tables/NDDCrossTable26")
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table29Title, subCTOsListSTEC1["unknownList"]) , "final-tables/NDDCrossTable29")
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table27Title, subCTOsListSTEC2["sx-drugs"]) ,    "final-tables/NDDCrossTable27")
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table28Title, subCTOsListSTEC2["dm-drugs"]) ,    "final-tables/NDDCrossTable28")
    jft.createCSVfromTable( jft.generateTableFromCTOsWithEC(jft.Table30Title, subCTOsListSTEC2["unknownList"]) , "final-tables/NDDCrossTable30")

    #Create Hyperlinked Tables:
    for i in range(1,32+1): #32 because that's how many tables there are so far
        jft.createHyperLinkedCSV("output/final-tables/", "NDDCrossTable"+str(i))

#Function classifies all CTOs into independent groups and returns a list of CTOs
def classifyCTOs(CTOs, drugClassifiers, subClassifiers):
    unclassified = set() #List of drugs that we couldn't classify
    classifiedCTOs = {}
    classifiedCTOs["drugs"]       = []
    classifiedCTOs["biomarkers"]  = []
    classifiedCTOs["devices"]     = []
    classifiedCTOs["behaviors"]   = []
    classifiedCTOs["stemcells"]   = []
    classifiedCTOs["supplements"] = []
    classifiedCTOs["deleteList"]  = []
    classifiedCTOs["unknownList"] = []
    #Subclassification of drugs
    subclassifiedCTOs = {}
    subclassifiedCTOs["sx-drugs"]    = []
    subclassifiedCTOs["dm-drugs"]    = []
    subclassifiedCTOs["unknownList"] = []
    #Time to Classify!
    for entry in CTOs:
        drugName = entry.drugname.lower() #Match lowercase version so it string matches
        classified_success = False
        #Check Each Category to see if the intervention is in it

        #Can add more custom skipping here for drugnames

        #First let's find exact matches.
        #for i in range(len(drugClassifiers)):
        for i in drugClassifiers: #Iterate through all the keys
            if drugName in drugClassifiers[i]:
                #We have matched to a class
                classifiedCTOs[i].append(entry) #add CTO to this class
                if i == "drugs": #If this CTO match is a drug, let's try to add to a drug subclass
                    subclassified_success = False
                    for j in subClassifiers:
                        if drugName in subClassifiers[j]:
                            subclassified_success = True #we matched a subclass
                            subclassifiedCTOs[j].append(entry) #add CTO to this subclass too
                    if not subclassified_success:
                        subclassifiedCTOs["unknownList"].append(entry)
                classified_success = True
                break #so we don't add same trial to 2 classes for now
        #If we havent found a match it may be because this is a single trial multiple NDD table where
        #The drugname is a list of all items. In which case we want to check each one separately
        #Since they are comma separated we will go ahead and parse that.
        if not classified_success:
            splitdrugName = drugName.split(", ")
            if len(splitdrugName) > 1: #if true then this was one of those cases and we are now going to process it
                #To process it we will run through each intervention and classify them individually,
                #To decide what class we put the overall trial we will try several checks
                #A - if one class has more interventions we group it to that (excluding deleteList class)
                #B - If we have a tie we prioritize: drug > biom > device > behavior > stem > suppl. (exclude deleteList again)
                #C  - Also we want to take out all deletList items from the string so those don't print on the list
                #D  - if we still have no match then we just keep going to the other if statement
                separatedInterventions = dict() #to store separate ones.
                for dname in splitdrugName:
                    for i in drugClassifiers: #Iterate through all the keys
                        if dname in drugClassifiers[i]:
                            #we found a match on the substring save it before doing master logic
                            if i in separatedInterventions: #If key exists append
                                separatedInterventions[i].append(dname)
                            else: #make new one
                                separatedInterventions[i] = [dname]
                #Now we can do the logic mentioned above
                
                maxlength = 0
                classcount = len(separatedInterventions)
                #Find max length
                for k in separatedInterventions:
                    if len(separatedInterventions[k]) > maxlength:
                        maxlength = len(separatedInterventions[k])
                if maxlength > 0: #We found at least one match so keep going, otherwise give up, #Case #D
                    finalclass = ""
                    #Find all of the classes that got maxlength
                    allmaxlengthclasses = []
                    for k in separatedInterventions:
                        if len(separatedInterventions[k]) == maxlength:
                            allmaxlengthclasses.append(k)
                    if classcount == 1: #only 1 class so just go with that regardless
                        finalclass = allmaxlengthclasses[0] #no choice but to go with deletelist
                    #From here on out it means we have multiple classes and have to make a choice... :
                    #Multiple classes but there is one with more interventions, so go with that as long as it's not deleteList
                    elif len(allmaxlengthclasses) == 1 and allmaxlengthclasses[0] != "deleteList": #case #A from above
                        finalclass = allmaxlengthclasses[0]
                    else: #Case #B Tie so prioritize
                        if len(allmaxlengthclasses) == 1 and allmaxlengthclasses[0] == "deleteList":
                            #the most common class was deleteclasses so before we go further let's find the next maxlength
                            #and also update allmaxlengthclasses
                            maxlength = 0
                            allmaxlengthclasses = []
                            for k in separatedInterventions:
                                if len(separatedInterventions[k]) > maxlength and k != "deleteList":
                                    maxlength = len(separatedInterventions[k])
                            for k in separatedInterventions:
                                if len(separatedInterventions[k]) == maxlength:
                                    allmaxlengthclasses.append(k)
                        #Okay now we can move on without worrying about that special case
                        if len(allmaxlengthclasses) == 1:
                            #the next maxlength only had one class, that's easy just pick that
                            finalclass = allmaxlengthclasses[0]
                        else: #we are here because it the current max length has more than 1 class
                            #we got here either because deletelist was removed and next tier has a tie
                            #or because the top winner has a tie and deleteList may be among those with tie
                            #however if deletelist is here then there has to be another class too by the
                            #logic written, and my logic is undeniable so do not worry about ending up
                            #with having to pick deleteList, this should never happen at this point.
                            #Priority: drug > biom > device > behavior > stem > suppl. (exclude deleteList again)
                            #let's just do this with a bunch of if statements
                            if "drugs" in allmaxlengthclasses:
                                #Top priority assign this.
                                finalclass = "drugs"
                            elif "biomarkers" in allmaxlengthclasses:
                                finalclass = "biomarkers"
                            elif "devices" in allmaxlengthclasses:
                                finalclass = "devices"
                            elif "behaviors" in allmaxlengthclasses:
                                finalclass = "behaviors"
                            elif "stemcells" in allmaxlengthclasses:
                                finalclass = "stemcells"
                            elif "supplements" in allmaxlengthclasses:
                                finalclass = "supplements"
                            elif "deleteList" in allmaxlengthclasses:
                                print("Warning: We shouldn't see deleteList Here, check code!")
                                finalclass = "deleteList"
                            else:
                                print("Warning: Unable to resolve final class!")
                    #Now that we have decided on a class, before appending, let's remove any 
                    #deleteList items from the drugname if we did not classify this to deleteList.
                    if finalclass != "deleteList" and "deleteList" in separatedInterventions:
                        splitOriginalDrugname = entry.drugname.split(", ") #Current list of drugs
                        newDrugName = ""
                        #create new drugname, same as current but without deleteList interventions
                        for i in splitOriginalDrugname:
                            if i.lower() not in separatedInterventions["deleteList"]:
                                newDrugName += i + ", "
                        entry.drugname = newDrugName[:-2] #save the new drugname, remove last comma and space
                    #Let's apppend!
                    classifiedCTOs[finalclass].append(entry) #add CTO to this class
                    classified_success = True

                    if finalclass == "drugs": #If this finalclass is a drug, let's try to add to a drug subclass
                        subclassified_success = False
                        already_inserted_list = []
                        for dname in splitdrugName:
                            for i in subClassifiers: #Iterate through all the keys
                                if i not in already_inserted_list and dname in subClassifiers[i]:
                                    subclassified_success = True #we found a match on the substring 
                                    subclassifiedCTOs[i].append(entry)
                                    already_inserted_list.append(i) #So we dont insert something twice if it has 2 sx
                                    break
                        if not subclassified_success:
                            subclassifiedCTOs["unknownList"].append(entry)

        if not classified_success: #If we still haven't matched then let's try to search for partial match
            #in the new version this  case really should not happen
            #for i in range(len(drugClassifiers)): #check each class
            for i in drugClassifiers: #check each class by key
                for intervention in drugClassifiers[i]: #check each intervention in that class
                    if intervention in drugName:
                        classifiedCTOs[i].append(entry) #we found a partial match so let's go with that
                        classified_success = True
                        if i == "drugs":
                            print("Verify:", intervention+":", drugName)
                            #let's try to add to a drug subclass
                            subclassified_success = False
                            already_inserted_list = []
                            for dname in splitdrugName:
                                for i in subClassifiers: #Iterate through all the keys
                                    if i not in already_inserted_list and dname in subClassifiers[i]:
                                        subclassified_success = True #we found a match on the substring 
                                        subclassifiedCTOs[i].append(entry)
                                        already_inserted_list.append(i) #So we dont insert something twice if it has 2 sx
                                        break
                            if not subclassified_success:
                                subclassifiedCTOs["unknownList"].append(entry)
                        break #so we stop checking for this drug
                if classified_success: #If we found a match in previous class
                    break #movie on to next CTO
        if not classified_success: #if we still haven't found a match...
            #let's just assume it's a non-drug, but also let's make a list of them for improving the system
            classifiedCTOs["unknownList"].append(entry)
            unclassified.add(entry.drugname) #Append the normal casing
    return classifiedCTOs, subclassifiedCTOs, unclassified


#drugclassifier main function to separate intervention matched into groups like non-drug
#disease-modifying drug, biomarkers, devices etc... for both CTOs: 
# CTOsIT (Independent Trials) and CTOsST (Single Trials)
def runDrugClassifier(CTOsIT, CTOsST,  CTOsSTEC1, CTOsSTEC2):

    #First let's save all interventions into a file and call it allinterventions
    #This is pre removal of anything
    printAllInterventions(CTOsIT+CTOsST+CTOsSTEC1+CTOsSTEC2, "classified-tables/all-interventions")

    #next, load all text files to use to separate items
    drugClassifiers, subclassifiers = readClassifierFiles()
    
    #Do classification and return a list of 3 CTOs sets classified
    classifiedCTOsListIT, subclassifiedCTOsListIT, unclassified1 = classifyCTOs(CTOsIT, drugClassifiers, subclassifiers)
    classifiedCTOsListST, subclassifiedCTOsListST, unclassified2 = classifyCTOs(CTOsST, drugClassifiers, subclassifiers)
    classifiedCTOsListSTEC1, subclassifiedCTOsListSTEC1, unclassified3 = classifyCTOs(CTOsSTEC1, drugClassifiers, subclassifiers)
    classifiedCTOsListSTEC2, subclassifiedCTOsListSTEC2, unclassified4 = classifyCTOs(CTOsSTEC2, drugClassifiers, subclassifiers)
    unclassified = unclassified1.union(unclassified2).union(unclassified3).union(unclassified4)

    #Create a list with all the unclassified so we can improve later
    if len(unclassified1) != 0:
        jfc.writeListToFileSorted(unclassified, "output/classified-tables/", "unclassified-interventions")

    #create output files to be used for verification
    printClassifiedCTOs(classifiedCTOsListIT, classifiedCTOsListST, classifiedCTOsListSTEC1, classifiedCTOsListSTEC2,
                        subclassifiedCTOsListIT, subclassifiedCTOsListST, subclassifiedCTOsListSTEC1, subclassifiedCTOsListSTEC2)

    #finally let's create our final tables as CSV
    createFinalTables(classifiedCTOsListIT, classifiedCTOsListST, classifiedCTOsListSTEC1, classifiedCTOsListSTEC2,
                      subclassifiedCTOsListIT, subclassifiedCTOsListST, subclassifiedCTOsListSTEC1, subclassifiedCTOsListSTEC2)

#END CODE

