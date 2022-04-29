#This file was born out of necessity. I need to run a lot of my existing code, but modified, to process these trials where
#the eligibility criteria contains a Neurodegenerative Disease (NDD) meaning the subjects of the trial may have that NDD.
#Because of this, these trials are of interest and I have created these csv files containing a list of NDD the trials 
#mentioned, the 3 files created contain either 
# 1) a single NDD detected that we then found was a new NDD in an existing trial with another NDD
# 2) multiple NDD detected that we then found at least one was new compared to existing NDD listed as condition in a trial
#    we were already tracking as of interest (since it had a NDD listed in conditions)
# 3) multple NDD detected in a trial that had no NDD listed as conditions. Truly a new trial discovered. This one needs us
#    to pull data from our raw files so we can get all the trial info.

# For all three of these I need to classify the interventions listed to generate new tables (or append to existing?)
# For now my big focus is to get the drug ones, but will expand to all intervention types. All that code I wrote/is done
# for the other NDD trials, I just have to adapt it so it works here without crashing :D
#TODO

#Imports
import tablegeneration as jft
from common import jfc

#Parameters: These are 1,2,and3 from above comment. The fourth one is out matchedCTO objects useful for 1,2 checks.
#ec1matchedtrials: Stores NCTID, Trial Condition List, NDD listed in eligibility criteria text, and raw eligibility criteria text
#ec2matchedtrials: Stores NCTID, Trial Condition List, NDD listed in eligibility criteria text,
#                  New NDD appearing in Elig Crit Text, and raw eligibility criteria text
#ecnewtrials:      Stores NCTID, NDD listed in eligibility criteria text, and raw eligibility criteria text
#matchedCTOS:      Clinical Trial Objects. All NDD trials in a beautifully formatted way. Useful for 1 and 2 checks.
def eligibilitycritprocessor(ec1matchedtrials, ec2matchedtrials, ecnewtrials, matchedCTO): 
    #Before anything remove list of trials to exclude due to manual checks
    removeECexclusions(ec1matchedtrials, ec2matchedtrials, ecnewtrials)

    #First let's build tableSTCTOs which we can use for 1 and 2. 
    tableSTCTOsEC1  = buildtableSTCTOs1(ec1matchedtrials,ec2matchedtrials, matchedCTO) #prepare to generate table
 
    #Next let's get all the data (built CTO objects) for all the new trials which we need for 3
    newtrialCTOs = buildECCTOs(ecnewtrials) #Will load output/eligibility-criteria/ csvs with trial data we need
    tableSTCTOsEC2  = buildtableSTCTOs2(newtrialCTOs) #This prepares the data to generate the tables

    #Save output to tables for both CTO groups:
    tableSTEC1Final = jft.generateTableFromCTOsWithEC(jft.TableSTEC1Title, tableSTCTOsEC1) #Make Table
    jft.createCSVfromTable(tableSTEC1Final, "final-tables/NDDCrossTableSTEC1") #Create CSV with table
    jft.createHyperLinkedCSV("output/final-tables/","NDDCrossTableSTEC1") #Make hyperlinked version

    tableSTEC2Final = jft.generateTableFromCTOsWithEC(jft.TableSTEC2Title, tableSTCTOsEC2) #Make Table
    jft.createCSVfromTable(tableSTEC2Final, "final-tables/NDDCrossTableSTEC2") #Create CSV with table
    jft.createHyperLinkedCSV("output/final-tables/","NDDCrossTableSTEC2") #Make hyperlinked version

    return tableSTCTOsEC1, tableSTCTOsEC2 #Return it back so it can be fed to drugmatcher

#Will open our elig-crit-exclusions.txt to get NCTID list of trials to remove from all 3
#of our files since they are false positive matches. List was manually curated. So trust
def removeECexclusions(ec1matchedtrials, ec2matchedtrials, ecnewtrials):    
    exclusionSet = set()
    f = open("input/classifiers/eligCritExcl.txt", "r")
    next(f) #skip first line
    for line in f:
        try:
            nctid = line.partition(";")[0]
            exclusionSet.add(nctid)
        except:
            print("Warning Could not Extract an NCTID from eligCritExcl.txt!")
    f.close()
    #Fix: had to add [:] because we need to pass a copy of list and not list itself else it skips!
    for entry in ec1matchedtrials[:]: #Remove trial
        if entry[0] in exclusionSet:
            ec1matchedtrials.remove(entry)
    for entry in ec2matchedtrials[:]: #Remove trial
        if entry[0] in exclusionSet:
            ec2matchedtrials.remove(entry)
    for entry in ecnewtrials[:]:      #Remove trial
        if entry[0] in exclusionSet:
            ecnewtrials.remove(entry)

def buildtableSTCTOs1(ec1matchedtrials, ec2matchedtrials, matchedCTO):
    matchedNCTIDset = set() #We need a list of NCTIDs of Trials of interest. Set so we remove dups
    for ctrial in ec1matchedtrials:
        matchedNCTIDset.add(ctrial[0]) #add NCTID, no duplicates allowed
    for ctrial in ec2matchedtrials:
        matchedNCTIDset.add(ctrial[0]) #add NCTID, no duplicates allowed 
    #Next we want to get the last posted date of all of these so we sort and store by that order.
    matchedNCTIDList = [] #Will hold all NCTID of Trials we want, And also stores the last updated date
    for ctrial in matchedNCTIDset:
        matchedNCTIDList.append([matchedCTO[ctrial].nctid,matchedCTO[ctrial].lastpostedDate])
 
    #Let's sort by post date so new stuff appears first (so descending order)
    matchedNCTIDList.sort(key = lambda row: row[1], reverse=True)

    #now that we have our list let's get our eligibility criteria version of Table 10 data basically.
    ectableSTCTOs = jft.generateCTOTableST(matchedNCTIDList, matchedCTO)
    return ectableSTCTOs

#Functions serves as a way of using our old code for this new scenario. So it's like the bridge between
#worlds 
def buildtableSTCTOs2(newtrialCTOs):
    ecmatchedNCTIDList = [] #Will hold all NCTID of Trials we want, And also stores the last updated date
    for ctrial in newtrialCTOs:
        ecmatchedNCTIDList.append([newtrialCTOs[ctrial].nctid,newtrialCTOs[ctrial].lastpostedDate])
     #Let's sort by post date so new stuff appears first (so descending order)
    ecmatchedNCTIDList.sort(key = lambda row: row[1], reverse=True)
    #now that we have our list let's get our eligibility criteria version of Table 10 data basically.
    ectableSTCTOs = jft.generateCTOTableST(ecmatchedNCTIDList, newtrialCTOs)
    return ectableSTCTOs

#Function takes a set of trials NCTID that we want and then goes and gets all data from
#raw files and then creates files with just the trials we want and saves them to the 
#output/eligibility-criterial folder with the ec prefix for further processing.
#TL;DR: makes new csvs with trials of interest. Used in nddfilter to eligibility criteria trials
def writeECTrialsfromNCTIDset(nctids): #Requires a set containing all NCTIDs we want
    import csv #needed for function
    ecmatchentries      = [] #stores matches
    ecnddoutcomes       = [] #stores outcomes of matches
    ecndddesignoutcomes = [] #Stores design outcomes of matches
    with open("queries/chartsv4A.csv") as csv_file: #Get Trial data
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            if row[0] in nctids: #row[0] has the studies.nct_id
                ecmatchentries.append(row)
    sorted_ecmatchentries = sorted(ecmatchentries, key=lambda row: row[0], reverse=False) #sort by nctid
    with open('output/eligibility-criteria/ecnddtrials.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(sorted_ecmatchentries)

    with open("queries/chartsv4B.csv") as csv_file: #get outcome data
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            if row[0] in nctids: #this is from a trial we care about
                    ecnddoutcomes.append(row) #save it
    sorted_ecnddoutcomes = sorted(ecnddoutcomes, key=lambda row: row[0], reverse=False) #sort by nctid
    with open('output/eligibility-criteria/ecnddoutcomes.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(sorted_ecnddoutcomes)

    with open("queries/chartsv4C.csv") as csv_file: #get design outcome data
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            if row[0] in nctids:
                    ecndddesignoutcomes.append(row) #gg ez
    sorted_ecndddesignoutcomes = sorted(ecndddesignoutcomes, key=lambda row: row[0], reverse=False) #sort by nctid
    with open('output/eligibility-criteria/ecndddesignoutcomes.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(sorted_ecndddesignoutcomes)

#The plan is to read in the eligibility-criteria data, 
#create our CTO objects from it, and return that at the end. Similar to what we did in
#drugmatcherv6 with the original data. sounds ez right? Oh yeah and only create CTO
#objects from NCTIDs found in the incoming parameter.
#ecnewtrials: Stores NCTID, NDD listed in eligibility criteria text, and raw eligibility criteria text
def buildECCTOs(ecnewtrials):
    import csv #so we can load csv files
    ecmatchentries      = [] #Store the rows of trial data we care about
    ecnddoutcomes       = [] #Store the rows of outcomes we care about
    ecndddesignoutcomes = [] #Stores the rows of design outcomes we care about
    #Read in data
    with open("output/eligibility-criteria/ecnddtrials.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            ecmatchentries.append(row)

    with open("output/eligibility-criteria/ecnddoutcomes.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            ecnddoutcomes.append(row)

    with open("output/eligibility-criteria/ecndddesignoutcomes.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            ecndddesignoutcomes.append(row)

    newNCTIDset = set() #Next let's make a set containing all the NCTIDs we want
    for entry in ecnewtrials:
        newNCTIDset.add(entry[0]) #entry[0] contains the NCTID, removes duplicates
    #Let's try to build the CTO objects
    ecmatchedCTO = {} #Matched Clinical Trial Object :D
    currNCTID = "NCT00000000" #Code straight outa drugmatcher
    for row in ecmatchentries:
        if row[0] in newNCTIDset: #Relevant Trial, build CTO, otherwise we don't need it so ignore it.
            if currNCTID != row[0]: #new NCTID
                ecmatchedCTO[row[0]] = jfc.clinicalTrial(row[0],row[1],row[2],row[3],row[4],row[5],
                             row[6],row[7],row[8],row[9],row[10],row[11], True) #new trial entry
                #The true at end is because we are  setting condition to flexible
                currNCTID = row[0]
            else: #still inserting to current NCTID a new condition or intervention so handle it.
                #Try adding condition, intervention, or intervention_other_names
                ecmatchedCTO[row[0]].addCondition(row[2])
                ecmatchedCTO[row[0]].addInterventions(row[3],0)
                ecmatchedCTO[row[0]].addInterventions(row[4],1)
    #Next let's go ahead and add the outcomes
    for row in ecnddoutcomes:
        if row[0] in newNCTIDset: #Relevant Trial, build CTO, otherwise we don't need it so ignore it.
            ecmatchedCTO[row[0]].addOutcome(row[1],row[2])

    #Next let's go ahead and add the design_outcomes (to see if we can fill more info for empty spots)
    for row in ecndddesignoutcomes:
        if row[0] in newNCTIDset: #Relevant Trial, build CTO, otherwise we don't need it so ignore it.
            ecmatchedCTO[row[0]].addDesignOutcomes(row[1],row[2],row[3])

    #So all objects are made now, so let's just add the eligibility criteria and NDD in elig criteria 
    for row in ecnewtrials:
        if row[0] in ecmatchedCTO:
            ecmatchedCTO[row[0]].addEligibilityCriteria(row[2]) #Add eligibilities to our objects
            ecmatchedCTO[row[0]].addNDDInEligCriteria(list(row[1])) #Store NDD list
        else:
            print("Warning: Could not find NCTID of EC Trial in CTO List!")

    return ecmatchedCTO #Done

#END CODE