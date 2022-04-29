#For table generation
from common import jfc
import csv
import json #For JSON Export/Imports

#common variables 

#This entry will hold table headings and we can add it to the top of the CSV file so it looks nice
Table1Title   = ["Table 1.  Drugs in independent trials involving more than 1 neurodegenerative disorder."]
Table2Title   = ["Table 2.  Drugs in single trials that included more than 1 neurodegenerative disorder."]
Table3Title   = ["Table 3.  Biomarkers in independent trials involving more than 1 neurodegenerative disorder."]
Table4Title   = ["Table 4.  Biomarkers in single trials that included more than 1 neurodegenerative disorder."]
Table5Title   = ["Table 5.  Device Interventions in independent trials involving more than 1 neurodegenerative disorder."]
Table6Title   = ["Table 6.  Devices Interventions in single trials that included more than 1 neurodegenerative disorder."]
Table7Title   = ["Table 7.  Behavioral Interventions in independent trials involving more than 1 neurodegenerative disorder."]
Table8Title   = ["Table 8.  Behavioral Interventions in single trials that included more than 1 neurodegenerative disorder."]
Table9Title   = ["Table 9.   Stem Cell Interventions in independent trials involving more than 1 neurodegenerative disorder."]
Table10Title  = ["Table 10.  Stem Cell Interventions in single trials that included more than 1 neurodegenerative disorder."]
Table11Title  = ["Table 11.  Supplements as Interventions in independent trials involving more than 1 neurodegenerative disorder."]
Table12Title  = ["Table 12.  Supplements as Interventions in single trials that included more than 1 neurodegenerative disorder."]
#These are for reference only to make sure no trial that shouldn't have been deleted is listed here
Table13Title  = ["Table 13.  Deleted Intervention Matches in independent trials involving more than 1 neurodegenerative disorder."]
Table14Title  = ["Table 14.  Deleted Intervention Matches in single trials that included more than 1 neurodegenerative disorder."]
#These are for reference only to make sure no trials appear here. If they do then they need to be classified somewhere
Table15Title  = ["Table 15.  Unknown Intervention Class in independent trials involving more than 1 neurodegenerative disorder."]
Table16Title  = ["Table 16.  Unknown Intervention Class in single trials that included more than 1 neurodegenerative disorder."]
Table31Title  = ["Table 31.  Unknown Intervention Subclass in independent trials involving more than 1 neurodegenerative disorder."]
Table32Title  = ["Table 32.  Unknown Intervention Subclass in single trials that included more than 1 neurodegenerative disorder."]
#These are for the subclasses
Table17Title   = ["Table 17.  Symptomatic Drugs in independent trials involving more than 1 neurodegenerative disorder."]
Table18Title   = ["Table 18.  Symptomatic Drugs in single trials that included more than 1 neurodegenerative disorder."]
Table19Title   = ["Table 19.  Disease Modifying Drugs in independent trials involving more than 1 neurodegenerative disorder."]
Table20Title   = ["Table 20.  Disease Modifying Drugs in single trials that included more than 1 neurodegenerative disorder."]

#These are aggregate tables for reference only
TableITTitle  = ["Table IT.  All Intervention Matches in independent trials involving more than 1 neurodegenerative disorder."]
TableSTTitle  = ["Table ST.  All Intervention Matches in single trials that included more than 1 neurodegenerative disorder."]
TableSTEC1Title  = ["Table STEC1.  All Intervention Matches in single trials that included more than 1 neurodegenerative " +
                    "disorder by having at least one NDD listed as a Condition and by having one or more NDD listed in the " +
                    "Eligibility Criteria that do not appear in the Conditions."]
TableSTEC2Title  = ["Table STEC2.  All Intervention Matches in single trials that included more than 1 neurodegenerative disorder " +
                    "by having no NDD listed as Condition, but having one or more NDD listed in the Eligibility Criteria."]

#New Tables for Eligibility Criteria Matches
Table21Title   = ["Table 21.  Drugs in single trials that included more than 1 neurodegenerative disorder " +
                  "by having at least one NDD listed as a Condition and by having one or more NDD listed in the " +
                  "Eligibility Criteria that do not appear in the Conditions."]
Table22Title   = ["Table 22.  Drugs in single trials that included more than 1 neurodegenerative disorder " +
                  "by having no NDD listed as Condition, but having one or more NDD listed in the Eligibility Criteria."]
Table23Title   = ["Table 23.  Non-Drug Interventions in single trials that included more than 1 neurodegenerative disorder " +
                  "by having at least one NDD listed as a Condition and by having one or more NDD listed in the " +
                  "Eligibility Criteria that do not appear in the Conditions."]
Table24Title   = ["Table 24.  Non-Drug Interventions in single trials that included more than 1 neurodegenerative disorder " +
                  "by having no NDD listed as Condition, but having one or more NDD listed in the Eligibility Criteria."]
#Subclasses for Eligibility Criteria Matches:
Table25Title   = ["Table 25.  Symptomatic Drugs in single trials that included more than 1 neurodegenerative disorder " +
                  "by having at least one NDD listed as a Condition and by having one or more NDD listed in the " +
                  "Eligibility Criteria that do not appear in the Conditions."]
Table26Title   = ["Table 26.  Disease Modifying Drugs in single trials that included more than 1 neurodegenerative disorder " +
                  "by having at least one NDD listed as a Condition and by having one or more NDD listed in the " +
                  "Eligibility Criteria that do not appear in the Conditions."]
Table27Title   = ["Table 27.  Symptomatic Drugs in single trials that included more than 1 neurodegenerative disorder " +
                  "by having no NDD listed as Condition, but having one or more NDD listed in the Eligibility Criteria."]
Table28Title   = ["Table 28.  Disease Modifying Drugs in single trials that included more than 1 neurodegenerative disorder " +
                  "by having no NDD listed as Condition, but having one or more NDD listed in the Eligibility Criteria."]
Table29Title   = ["Table 29.  Unknown Intervention Subclass in single trials that included more than 1 neurodegenerative disorder " +
                  "by having at least one NDD listed as a Condition and by having one or more NDD listed in the " +
                  "Eligibility Criteria that do not appear in the Conditions."]
Table30Title   = ["Table 30.  Unknown Intervention Subclass in single trials that included more than 1 neurodegenerative disorder " +
                  "by having no NDD listed as Condition, but having one or more NDD listed in the Eligibility Criteria."]


################## START FUNCTIONS ################## START FUNCTIONS ################## START FUNCTIONS ##################

#Function that is same as generateTable2 but instead makes a list of the  CTO objects (good for further processing)
def generateCTOTableST(trialNCTIDlist, CTO): #generates list of objects
    tableAsCTO = []
    for nctid in trialNCTIDlist:
        #For this table each entry only has 1 nctid
        try:
            newCTOSet = jfc.drugClinicalTrialSet(CTO[nctid[0]].getInterventionDrugsStr()) #create new set, give drug name
            #For now we are just adding all drugs in there yolo, but we will want to maybe pick 1 later
            newCTOSet.insertClinicalTrial(CTO[nctid[0]])
        except KeyError:
            print("CTO Hashing Error with NCTID:", nctid[0])
        tableAsCTO.append(newCTOSet)
    return tableAsCTO

#iTML: [Matched Drugname, List of NCTID of Trials Matching, Most recent last posted date of the set of trials]
#Function that generates our final table as objects. Which can then be fed to generateTableFromCTOs to generate any table.
#By doing this we generalize all data which is good
def generateCTOTableIT(iTML, CTO): #generates list of objects
    tableAsCTO = []
    for entry in iTML:
        newCTOSet = jfc.drugClinicalTrialSet(entry[0]) #create new set, give drug name
        for curr_nctid in entry[1]: #now for the rest of the rows of this set
            try:
                newCTOSet.insertClinicalTrial(CTO[curr_nctid])
            except KeyError:
                print("Hashing Error with NCTID:", curr_nctid)
        tableAsCTO.append(newCTOSet) #add set to list
    return tableAsCTO

#This puppy can generate any table from our generic CTOs class
def generateTableFromCTOs(tableTitle, CTOs):
    columnTitles = ['Drug', 'Trial', 'Phase', 'Diagnosis','Number of Participants', 
                    'Duration of Trial', 'Primary Outcome(s)', 'Biomarker Outcome(s)', 'Year Registered', 'Status']
    FinalTable = [tableTitle, columnTitles]    
    for entry in CTOs:
        for i in range(len(entry.clinicalTrialList)):
            FinalTable.append(entry.clinicalTrialList[i].generateTableRow()) #create first row of set
            if i == 0: 
                FinalTable[-1][0] = entry.drugname #Save Matched Drug in first row
    return FinalTable

#Modified pupper that has an extra column for Additional NDD in Eligibility Criteria
def generateTableFromCTOsWithEC(tableTitle, CTOs):
    columnTitles = ['Drug', 'Trial', 'Phase', 'Diagnosis', 'New NDD in Eligibility Criteria' ,'Number of Participants', 
                    'Duration of Trial', 'Primary Outcome(s)', 'Biomarker Outcome(s)', 'Year Registered', 'Status']
    FinalTable = [tableTitle, columnTitles]    
    for entry in CTOs:
        for i in range(len(entry.clinicalTrialList)):
            FinalTable.append(entry.clinicalTrialList[i].generateTableRow(withEC=True)) #create first row of set
            if i == 0: 
                FinalTable[-1][0] = entry.drugname #Save Matched Drug in first row
    return FinalTable

def createCSVfromTable(tableName, fname):
    with open('output/' + fname + '.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)    
        outfile.writerows(tableName)


def createHyperLinkedCSV(fdir, fname): # Hyperlinked version of NDDCrossTableX.csv DO NOT ADD .CSV AT END
    with open(fdir+fname+'.csv') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        with open(fdir+"hyperlinked/"+fname+'HyperLinked.csv', 'w', newline='') as csv_outfile:
            outfile = csv.writer(csv_outfile)
            skipFirst2Rows = 2
            for row in csv_data:
                if skipFirst2Rows == 0:
                    row[1] = "=HYPERLINK(\"https://www.clinicaltrials.gov/ct2/show/"+row[1]+"\", \""+row[1]+"\")"
                else:
                    skipFirst2Rows -= 1
                outfile.writerow(row)

def makeJSONmatchedCTO(matchedCTO):
    #Next let's generate and export the JSON of the dictionary to a file
    #Note: right now we are just testing feasability of JSON and then importation into the app
    #      Eventually what we will want to export are objects that are matching or other
    #      stuff we will deal with.
    #jsonmatchedCTO = json.dumps(matchedCTO["NCT00455143"].__dict__, indent = 4)
    jsonmatchedCTO = "{\n"
    for x in matchedCTO:
        jsonmatchedCTO += "\"" + x + "\" : " + json.dumps(matchedCTO[x].__dict__, indent = 4) + ",\n"
    jsonmatchedCTO = jsonmatchedCTO [:-2] + "\n}"
    #jsonmatchedCTO = "{\n" + ',\n'.join(str("\"" + x + "\" : " + json.dumps(matchedCTO[x].__dict__, indent = 4)) for x in matchedCTO) + "\n}"
    #one-liner of the above 4 lines of code. Could be made even better with more joins but seems to be irrelevant for this size data
    jsonFile = open("output/json-tables/jsonMatchedCTO.json", "w")
    jsonFile.write(jsonmatchedCTO)
    jsonFile.close()

#Function to generate a JSON from a list of CTOset objects, essentially to generate Final Tables in JSON Format
def makeJSONFromCTOsList(CTOs, tablenum):
    jsonCTOs = "{\n"
    for entry in CTOs:
        jsonCTOs += "\"" + entry.drugname + "\": [\n" 
        for ctrial in entry.clinicalTrialList:
            jsonCTOs += json.dumps(ctrial.__dict__, indent = 4) + ",\n"
        jsonCTOs = jsonCTOs[:-2] + "\n],\n"
    jsonCTOs = jsonCTOs[:-2] + "\n}\n"
    jsonFile = open("output/json-tables/jsonCTOTable" + str(tablenum) + ".json", "w")
    jsonFile.write(jsonCTOs)
    jsonFile.close()

################### END FUNCTIONS ################### END FUNCTIONS ################### END FUNCTIONS ###################