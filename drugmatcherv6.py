#This is where the program starts from
from common import jfc
import tablegeneration as jft
import drugclassifier as jfd
from eligcritprocesser import eligibilitycritprocessor

import csv

#This will take the nddtrials.csv and process from there (to speed it up)

matchentries = []       #chartsv4A study and other main components
nddoutcomes = []        #chartsv4B outcomes
ndddesignoutcomes  = []  #chartsv4C design outcomes
nddeligsinglecond  = []  #chartsv4D Trials with 1 NDD mention in the Eligibility Criteria
nddeligmulticond   = []  #chartsv4D Trials with 2 or more NDD mention in the Eligibility Criteria

finalentries = []

#Cleanup Output Directory
jfc.cleanOutputFiles() #Comment out for speed boost

#Read in data
with open("output/nddtrials.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        matchentries.append(row)

with open("output/nddoutcomes.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        nddoutcomes.append(row)

with open("output/ndddesignoutcomes.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        ndddesignoutcomes.append(row)

with open("output/eligibility-criteria/nddeligcritsinglecond.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        nddeligsinglecond.append(row)

with open("output/eligibility-criteria/nddeligcritmulticond.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        nddeligmulticond.append(row)

# Row Contents of output/nddtrials.csv
# Row[0] studies.nct_id
# Row[1] studies.official_title
# Row[2] conditions.name
# Row[3] interventions.name
# Row[4] intervention_other_names.name
# Row[5] studies.last_update_posted_date
# Row[6] studies.phase
# Row[7] studies.acronym
# Row[8] studies.enrollment
# Row[9] outcomes.time_frame
# Row[10] studies.study_first_posted_date
# Row[11] studies.overall_status

# Row Contents of queries/chartsv4B.csv
# Row[0] outcomes.nct_id 
# Row[1] outcomes.title
# Row[2] outcomes.description

# Row Contents of queries/chartsv4C.csv
# Row[0] design_outcomes.nct_id 
# Row[1] design_outcomes.measure
# Row[2] design_outcomes.time_frame
# Row[3] design_outcomes.description

# Row Contents of queries/chartsv4D.csv
# Row[0] eligibilities.nct_id 
# Row[1] eligibilities.criteria

# Row Contents of output/eligibility-criteria/nddeligcritsinglecond.csv and nddeligcritmulticond.csv
# Row[0] eligibilities.nct_id 
# Row[1] Number of Identified NDD Acronyms
# Row[2] NDD Acronym list separated by semi-colons.
# Row[3] eligibilities.criteria (big text)

#GOAL: 
#Drug Matched
#NCT_ID
#PHASE
#Diagnosis
#Number of Participants
#Primary Outcome(s)
#Biomarker Outcome(s)
#Year Registered (first posted date)
#Status (with date of last status, use last posted date)

#NEW CODE FOR THE APP (TO MAKE JSON AND KEEP THIS AS OOP
#newest cross ndd tables 4-19-21 on 5-14-21
#Object Oriented Programming Time. Let's make our clinicalTrial objects using diseaseentrylist.csv
matchedCTO = {} #Matched Clinical Trial Object :D
TablesCTO  = [] #Stores All Table contents as Clinical Trial Objects along with matched drug strings (basically the same info as final tables)

currNCTID = "NCT00000000"
for row in matchentries:
    if currNCTID != row[0]: #new NCTID
        matchedCTO[row[0]] = jfc.clinicalTrial(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]) #new trial entry
        currNCTID = row[0]
    else: #still inserting to current NCTID a new condition or intervention so handle it.
        #Try adding condition, intervention, or intervention_other_names
        matchedCTO[row[0]].addCondition(row[2])
        matchedCTO[row[0]].addInterventions(row[3],0)
        matchedCTO[row[0]].addInterventions(row[4],1)
#print('\n'.join(str(matchedCTO[x]) for x in matchedCTO)) #Debug to Print the entire dictionary

#Next let's go ahead and add the outcomes
for row in nddoutcomes:
    matchedCTO[row[0]].addOutcome(row[1],row[2])

#Next let's go ahead and add the design_outcomes (to see if we can fill more info for empty spots)
for row in ndddesignoutcomes:
    matchedCTO[row[0]].addDesignOutcomes(row[1],row[2],row[3])

#New Code for Eligibility Criteria
#Next let's go ahead and add eligibility criteria for our trials and discover new trials worth looking at
ec1matchedtrials = [] #Stores NCTID, Trial Condition List, NDD listed in eligibility criteria text, and raw eligibility criteria text
ec2matchedtrials = [] #Stores NCTID, Trial Condition List, NDD listed in eligibility criteria text,
                      #New NDD appearing in Elig Crit Text, and raw eligibility criteria text
ecnewtrials = [] #Stores NCTID, NDD listed in eligibility criteria text, and raw eligibility criteria text

#We need this here to add exclusion trials that we want to not add NDD for
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

#First for single NDD in Eligibility Criteria
for row in nddeligsinglecond:
    if row[0] in matchedCTO:   
        matchedCTO[row[0]].addEligibilityCriteria(row[1]) #Add eligibilities to our objects in case we want to use it later
        if row[0] in exclusionSet:
            continue #skip this with manual skip
        trialcondlist = set(matchedCTO[row[0]].getConditionAcronyms())
        #If the eligibility criteria NDD we found is already listed in our trial conditions then we don't need to include this
        if row[2] not in trialcondlist: #otherwise we do as we found a NDD that went as unlisted!
            #Let's add one more check to exclude AD/MCI and PD/MCI pairs since we classify that as the same condition.
            if row[2] == 'MCI' and ('AD' in trialcondlist or 'PD' in trialcondlist):
                continue #Don't add it, skip it MCI/AD or MCI/PD pair
            if row[2] == 'AD' and len(trialcondlist) == 1 and 'MCI' in trialcondlist:
                continue #Don't add it, skip it. MCI/AD pair. Still may want to take a look at these later...
            if row[2] == 'PD' and len(trialcondlist) == 1 and 'MCI' in trialcondlist:
                continue #Don't add it, skip it. MCI/PD pair.            
            matchedCTO[row[0]].addNDDInEligCriteria(row[2]) #Store NDD list for use later or for table printing
            ec1matchedtrials.append([row[0], trialcondlist, row[2], str(row[3])]) #we will want to process further*
    else:
        #since we are only worried about single trials we don't need to process this further. However when we do independent trials we
        #don't want to discard this trial just yet as we will want to look at the NDD listed and the intervention as a potential match
        #candidate. For now we are good though. #TODO
        pass

#Next for multiple NDD listed in Eligility Criteria
for row in nddeligmulticond:
    if row[0] in matchedCTO:
        if row[0] in exclusionSet:
            continue #skip this with manual skip
        matchedCTO[row[0]].addEligibilityCriteria(row[1]) #Add eligibilities to our objects in case we want to use it later (if not added already)
        trialcondlist = set(matchedCTO[row[0]].getConditionAcronyms())
        econdlist = set(row[2].split(';')) #split condition acronyms using the ; delimiter
        #If all eligibility criteria text NDD we found are already listed in our trial conditions then we don't need to include this
        if not econdlist.issubset(trialcondlist): #otherwise we do as we found a NDD that went as unlisted!  #Set theory is useful!
            newndds = econdlist.symmetric_difference(trialcondlist) - trialcondlist #store the ones that are unseen for easier processing
            if len(newndds) == 1  and 'MCI' in newndds and ('AD' in trialcondlist or 'PD' in trialcondlist):
                continue #Don't add case where only new NDD is MCI and we already have PD or AD in trial
            if len(newndds) == 1 and len(trialcondlist) == 1 and 'MCI' in trialcondlist and ('AD' in newndds or 'PD' in newndds):
                continue #Don't add case where MCI is only Cond in Trial and we only have 1 extra new NDD (MCI/AD or MCI/PD)
            matchedCTO[row[0]].addNDDInEligCriteria(list(newndds)) #Store NDD list for use later or for table printing
            ec2matchedtrials.append([row[0], trialcondlist, econdlist, newndds, str(row[3])]) #we will want to process further*
    else:
        ecnewtrials.append([row[0], set(row[2].split(';')), row[3]]) #these are new trials not listed as NDD trials. Process further*

#*further processing for ec1mmatchedtrials and ec2mmatchedtrials is to feed it through drugclassifier to see if 
# it's a trial with a dx or sm drug. For ecnewtrials we want to take these NCTIDs and see if any of them are for drugs. 
# But those I have to build CTOs first to be able to process. All of this I am going to do in the new file eligcritprocesser.py
tableSTCTOsEC1, tableSTCTOsEC2 = eligibilitycritprocessor(ec1matchedtrials, ec2matchedtrials, ecnewtrials, matchedCTO)


#write trials to review
with open('output/eligibility-criteria/ec1matchedtrials.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(ec1matchedtrials)
with open('output/eligibility-criteria/ec2matchedtrials.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(ec2matchedtrials)
with open('output/eligibility-criteria/ecnewtrials.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(ecnewtrials)    
#End New Code for Eligibility Critera

#New Code for baseline measurements (demographics project)
#TODO need to add to the elgibility criteria raw trials something similar for demographics
from baselineprocesser import baselinemeasureprocessor
from baselineprocesser import generateDemographics
baselinemeasureprocessor(matchedCTO) #adds to standard trials demographic data fields
generateDemographics(matchedCTO) #Does the rest of the demographics on its own function/file

#Test to see if this worked
#print(matchedCTO["NCT00620191"]) #For Testing the match from the table
#print(matchedCTO["NCT00620191"].generateTableRow())
#print(matchedCTO["NCT04220021"]) #For Testing the match from the table
#print(matchedCTO["NCT04220021"].generateTableRow())

jft.makeJSONmatchedCTO(matchedCTO) #Not used currently but left on since may be useful to have this



#TIME TO MAKE TABLES

#Let's start with Table 2 of Cross NDD
#    Table ST.  All interventions in single trials that included more than 1 neurodegenerative disorder.
# This one is ez
#we will just run through our object dictionary and find ones with length > 1 of the conditions array. Also good to test
#all our system


multiConditionNCTIDList = [] #Will hold all NCTID of Trials that have more than 1 condition listed, Am also going to store the last updated date
#So I can then sort the trials by newest. This will make it look nice.
#multiConditionNCTIDList.append(['NCT00000000', '2000-01-15']) #Test
#print(matchedCTO["NCT03658135"]) #For Testing the match from the table
#print(matchedCTO["NCT03658135"].generateTableRow())
#print(matchedCTO["NCT03658135"].getInterventionDrugsStr())
#multiConditionNCTIDList.append(['NCT03658135', '2019-12-19']) #Test

##TABLE ST MAIN CODE
for ctrial in matchedCTO:
    if (len(matchedCTO[ctrial].condition) > 1 and 
            matchedCTO[ctrial].condition[0] != "Healthy Volunteers" and 
            matchedCTO[ctrial].condition[1] != "Healthy Volunteers"): #Avoid detecting this false positive
        #Found something to add. Save the NCTID and last posted date
        if len(matchedCTO[ctrial].intervention) > 0 or len(matchedCTO[ctrial].otherIntervention) > 0: #don't add trials without drugs.
            #Extra Special Check to avoid including MCI/AD pairs and PD/MCI pairs unless something else is involved.
            try: 
                condlist = matchedCTO[ctrial].getConditionAcronyms()
                if len(matchedCTO[ctrial].condition) == 2:
                    if "MCI" in condlist and ( "PD" in condlist or "AD" in condlist):
                        continue #Don'add!
            except:
                print("warning Filtering MCI/PD and MCI/AD! [1]")
                pass
            #END NEW CODE CHECK
            multiConditionNCTIDList.append([matchedCTO[ctrial].nctid,matchedCTO[ctrial].lastpostedDate])
            #may be able to remove this if statement if we re-do our SQL query and remove non-interventional trials?

#Let's sort by post date so new stuff appears first (so descending order)
multiConditionNCTIDList.sort(key = lambda row: row[1], reverse=True)

#Create our final version of Table 10
tableSTCTOs = jft.generateCTOTableST(multiConditionNCTIDList, matchedCTO)
tableSTFinal = jft.generateTableFromCTOs(jft.TableSTTitle, tableSTCTOs)

#Write the new csv
jft.createCSVfromTable(tableSTFinal, "final-tables/NDDCrossTableST")
#with open('output/NDDCrossTableST.csv', 'w', newline='') as csv_outfile:
#    outfile = csv.writer(csv_outfile)    
#    outfile.writerows(tableSTFinal)


#Create Hyperlinked version of NDDCrossTableST.csv
jft.createHyperLinkedCSV("output/final-tables/","NDDCrossTableST")


#TABLE IT MAIN CODE:
#In this one we are looking for drugs that appear in more than 1 trial. First phase let's find exact match entries
#Second phase later (with old code?) we can try to find partial matches by searching for individual words that match
iTMLP1 = [] #Independent Trial Match List Phase 1, Each entry holds:
# [  Matched Drugname, List of NCTID of Trials Matching (2 or more), Most recent last posted date of the set of trials  ]
# The last one is so that I can sort by newest drugs or also by newest entries the individual dates is for sorting within a drug entry set.
iTMLP2 = [] #Phase 2 of above.

iTMDP1 = {} #Dictionary that we are going to hash into for Phase 1. All we need to store is the key: drug and value: nctid
iTMDP2 = {} #Same for Phase 2. Stands for Independent Trial Match Dictonary Phase 2.

#So my plan for this is to for first pass to simply try hashing the objects using intervention and intervention_other_name as keys
#and then store for value a list of NCTID (so in case of collision we store them all). Store this in iTMDP1

#When done we look through at any key/value pair that has more than 1 trial stored. Then we check to see if there is at least 2 trials
#with different NDD. If so this is what we want so we add an entry into iTMLP1 so we can add it to our Table 1 results.

#Then for the second pass we can try the same hash approach but by using individual words as keys but before we do that we want to 
#look at the word and see if it's a stopword so we can skip those. Other than that we do the same process.

#Phase 1
for ctrial in matchedCTO:
    for drugname in matchedCTO[ctrial].intervention: 
        if jfc.drugnameCheckOK(drugname): #This is how we remove stopwords and other stuff we don't want like Placebo
            #Check if key exists already
            if drugname in iTMDP1: #Yes it exist, so append to existing list of NCTIDs
                iTMDP1[drugname].append(matchedCTO[ctrial].nctid)
            else: #New key so just add new entry
                iTMDP1[drugname] = [matchedCTO[ctrial].nctid] #It's a list of NCTIDs, so we just insert a list with 1 NCTID.
    for drugname in matchedCTO[ctrial].otherIntervention: #Do the same for intervention_other_names as above.
        if jfc.drugnameCheckOK(drugname): #This is how we remove stopwords and other stuff we don't want like Placebo
            if drugname in iTMDP1: 
                iTMDP1[drugname].append(matchedCTO[ctrial].nctid) #Same as above
            else:
                iTMDP1[drugname] = [matchedCTO[ctrial].nctid] #Same as above

#Next let's look at iTMDP1 and find multiple trial drugs and see if there is at least 2 with different NDD listed.
#Make sure we ignore the Healtyh Volunteers category.
for drugname in iTMDP1:
    alreadyAddedDrug = False
    if len(iTMDP1[drugname]) > 1: #We have a drug with multiple NCTIDs so let's see if they are different NDD
        try:
            firstTrialConditions = matchedCTO[iTMDP1[drugname][0]].condition
            for nctid in iTMDP1[drugname]:
                if alreadyAddedDrug:
                    break
                for cond in matchedCTO[nctid].condition:
                    if cond not in firstTrialConditions and cond != "Healthy Volunteers": #Don't count this as a different NDD
                        #we found a trial in the set that has a different NDD, add drug entry to iTMLP1

                        #TODO
                        #Special Check to avoid including MCI/AD pairs and PD/MCI pairs unless something else is involved.
                        #try: 
                        #    T1 = matchedCTO[iTMDP1[drugname][0]].getConditionAcronyms()
                        #    T2 = matchedCTO[nctid].getConditionAcronyms()
                        #    if len(T1) == 1 and len(T2) == 1:
                        #        if "MCI" in T1 and ("AD" in T2 or "PD" in T2):
                        #            continue 
                        #        if "AD"  in T1 and "MCI" in T2:
                        #            continue
                        #        if "PD"  in T1 and "MCI" in T2:
                        #            continue
                        #    if len(T1) == 2 and "MCI" in T1 and "AD" in T1:
                        #        if len(T2) == 1 and "AD" in T2:
                        #            continue
                        #except:
                        #    print("warning Filtering MCI/PD and MCI/AD! [2]")
                        #    pass
                        #END NEW CODE CHECK                       
                        #TODO

                        setNCTIDsWDate = []
                        for n in iTMDP1[drugname]:
                            setNCTIDsWDate.append([n,matchedCTO[n].lastpostedDate]) #make a list holding all nctid and last posted date
                        setNCTIDsWDate.sort(key=lambda col: col[1],reverse=True) #Sort Descending Order by Last Posted Date
                        newestLastPostedDate = setNCTIDsWDate[0][1]
                        #Find newest date to store that 
                        newentry = [drugname, [], newestLastPostedDate] #create entry
                        for i in setNCTIDsWDate:
                            newentry[1].append(i[0]) #Fill entry with only the nctids
                        iTMLP1.append(newentry) #append it

                        #Now that we added the set for this drugname let's move on to the next drugname by breaking to outermost loop
                        alreadyAddedDrug = True
                        break
        except:
            print("ERROR: Could not Find Cliical Trial in matchedCTO: ", nctid)
    #else: #Nothing to see here


#Let's sort by newest post date of each set so new stuff appears first (so descending order)
iTMLP1.sort(key = lambda col: col[2], reverse=True)

#Create our final version of Table IT
tableITCTOs = jft.generateCTOTableIT(iTMLP1, matchedCTO)
tableITFinal = jft.generateTableFromCTOs(jft.TableITTitle, tableITCTOs)

#Write the new csv
jft.createCSVfromTable(tableITFinal, "final-tables/NDDCrossTableIT")

#Create Hyperlinked version of NDDCrossTableIT.csv
jft.createHyperLinkedCSV("output/final-tables/", "NDDCrossTableIT")

#Phase 2 Here. TODO  (Single word matches)

#Make JSONS of Table 1 and 2.  #These would be equivalent to table1Final once rendered as table
jft.makeJSONFromCTOsList(tableITCTOs, 1)
jft.makeJSONFromCTOsList(tableSTCTOs, 2)

#Next we run drugclassifier to separate intervention matched into groups like non-drug, 
#disease-modifying drug, biomarkers, devices etc... for all CTOs  (ST, IT, and STECs)
#IT is Independent Trials, ST is single trials, EC is Eligibility Criteria
jfd.runDrugClassifier(tableITCTOs, tableSTCTOs, tableSTCTOsEC1, tableSTCTOsEC2) 

#END OF PROGRAM. CREATED BY JORGE FONSECA