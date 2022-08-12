#For Baseline Measurements Demographic Processing (Gender/Ethnicity/Race for now)

# Row Contents of output/nddbaselinemeasure.csv
# Row[0]  baseline_measurements.id
# Row[1]  baseline_measurements.nct_id
# Row[2]  baseline_measurements.result_group_id
# Row[3]  baseline_measurements.ctgov_group_code
# Row[4]  baseline_measurements.classification
# Row[5]  baseline_measurements.category
# Row[6]  baseline_measurements.title
# Row[7]  baseline_measurements.description
# Row[8]  baseline_measurements.units
# Row[9]  baseline_measurements.param_type
# Row[10] baseline_measurements.param_value
# Row[11] baseline_measurements.param_value_num
# Row[12] baseline_measurements.dispersion_type
# Row[13] baseline_measurements.dispersion_value
# Row[14] baseline_measurements.dispersion_value_num
# Row[15] baseline_measurements.dispersion_lower_limit
# Row[16] baseline_measurements.dispersion_upper_limit
# Row[17] baseline_measurements.explanation_of_na

#Imports:
import csv
from common import jfc

#Globals
#The following are the categories listed in ClinicalTrials.gov. I didn't choose these names or groups. These come from trials
demKey = {}
demKey['Sex']       = set()
demKey['Ethnicity'] = set()
demKey['Race']      = set()

def baselinemeasureprocessor(matchedCTO):
    nddbaselinemeasure = []  #chartsv4E baseline measurements
    with open("output/nddbaselinemeasure.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            nddbaselinemeasure.append(row)
    #First let's pre-process the data by storing only the totals and only the lines we want.
    #Row[1]: NCTID, Row[3]: BG00*, Row[4]: Country, Row[5]: Gender/Race/Ethnicty (GRE), Row[6]: GRE Label, Row[11] Amount/Count.
    demographics = {} #Clean
    skippedCategories = set() #Catches any Categories we skipped for review later.
    invalidEthnicityDataTrialList = []
    for row in nddbaselinemeasure:
        if row[1] not in demographics: #new NCTID, make subcategories
            demographics[row[1]] = {}
            demographics[row[1]]['Sex'] = {}
            demographics[row[1]]['Ethnicity'] = {}
            demographics[row[1]]['Race'] = {}
        if row[11] == '':
            row[11] = -1 #temporary fix for empty values. Usually for when something isn't assessed.
        try:
            if   'Sex' in row[6] or 'Gender' in row[6]:
                if   row[5] != '':
                    demographics[row[1]]['Sex'][row[5].lower()] = int(float(row[11])) #Avoids issues with 702.0
                    demKey['Sex'].add(row[5].lower())
                elif row[4] != '':
                    demographics[row[1]]['Sex'][row[4].lower()] = int(float(row[11])) #Avoids issues with 702.0
                    demKey['Sex'].add(row[4].lower())
                else:
                    print(f"Warning: {row} Invalid Sex Data in Demographic Processor.")                
            elif 'Ethnicity' in row[6]:
                if   row[5] != '':
                    demographics[row[1]]['Ethnicity'][row[5].lower()] = int(float(row[11]))
                    demKey['Ethnicity'].add(row[5].lower())
                elif row[4] != '':
                    demographics[row[1]]['Ethnicity'][row[4].lower()] = int(float(row[11]))
                    demKey['Ethnicity'].add(row[4].lower())
                else:
                    invalidEthnicityDataTrialList.append(row)
                #    print(f"Warning: {row} Invalid Ethnicity Data in Demographic Processor.")
            elif 'Race' in row[6]:
                if   row[5] != '':
                    demographics[row[1]]['Race'][row[5].lower()] = int(float(row[11]))
                    demKey['Race'].add(row[5].lower())
                elif row[4] != '':
                    demographics[row[1]]['Race'][row[4].lower()] = int(float(row[11]))
                    demKey['Race'].add(row[4].lower())
                else:
                    print(f"Warning: {row} Invalid Race Data in Demographic Processor.")
            else:
                skippedCategories.add(row[6])
        except KeyError:
            print(f"Warning: {row} Key Error in Demographic Processor.")
        except ValueError:
            print(f"Warning: {row} Value Error in Demographic Processor.")
    #for i in sorted(skippedCategories): print(i) #Review for anything missed.
    #for key in demKey['Sex']: print(key)
    #for key in demKey['Ethnicity']: print(key)
    #for key in demKey['Race']: print(key)
    #for i in invalidEthnicityDataTrialList: print(i[1]) #All NCTIDs

    #Generate Report of Categories: (we will do the same for only AD ones later so might make this into a function #TODO )
    with open('output/demographicCategories.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerow(['Report on listed demographics in regards to Sex, Ethnicity, and Race'])
        outfile.writerow(['Sex:'])
        for entry in sorted(demKey['Sex']):
            outfile.writerow([entry])
        outfile.writerow([]) #empty Line
        outfile.writerow(['Ethnicity:'])
        for entry in sorted(demKey['Ethnicity']):
            outfile.writerow([entry])
        outfile.writerow([]) #empty Line
        outfile.writerow(['Race:'])
        for entry in sorted(demKey['Race']):
            outfile.writerow([entry])
        outfile.writerow([]) #empty Line
        outfile.writerow(['Trials with Invalid Ethnicity Listed:'])
        outfile.writerows(invalidEthnicityDataTrialList)

    #TODO: Weight/Height/Country/Age info is also present for some, may be useful if we want those demographics

    #Time to add data to each trial. We will store in the CTO of each trial.
    demographicCount = 0 #How many Trials have demographics, So far 1002 matches!
    for nctid in matchedCTO:
        if nctid in demographics:
            matchedCTO[nctid].baseline_measurements = demographics[nctid]
            matchedCTO[nctid].hasDemographics = True
            demographicCount += 1
    #print("Total Trials with Demographic Data Added:", demographicCount)
#End Function

#Generate Aggregate results, tables etc... #TODO
def generateDemographics(matchedCTO):
    selCTO     = {} #Selected CTOs, CTOs that list AD or MCI as condition
    seldemCTO = {} #Of the above, only keep the ones that also contain demographics
    for nctid in matchedCTO:
        condlist = matchedCTO[nctid].getConditionAcronyms()
        if "MCI" in condlist or "AD" in condlist:
            selCTO[nctid] = matchedCTO[nctid] #store all AD/MCI trials (for reference)
            if matchedCTO[nctid].hasDemographics:
                seldemCTO[nctid] = matchedCTO[nctid] #Only store AD/MCI trials with demographic data
    #print("Total Trials of Interest:",len(selCTO)) #2541 AD/MCI trials
    #print("Total Trials of Interest with Demographics:",len(seldemCTO)) #407 AD/MCI trials

    #Get all categories:
    sexOGCategories       = set() #Store all categories
    ethnicityOGCategories = set() #Store all categories
    raceOGCategories      = set() #Store all categories
    toPop                 = set() #can't pop during iteration so will store here pop list

    categoryClasses = {}
    loadSREcategories(categoryClasses)

    for nctid in seldemCTO:
        for i in list(seldemCTO[nctid].baseline_measurements['Sex']):
            sexOGCategories.add(i)
            if i in 'gender unknown, unknown, or unspecified, other':
              seldemCTO[nctid].baseline_measurements['Sex']['unspecified, gender unknown, or other'] = seldemCTO[nctid].baseline_measurements['Sex'][i]
              seldemCTO[nctid].baseline_measurements['Sex'].pop(i, None)
        for i in seldemCTO[nctid].baseline_measurements['Race']:         #Nothing needed here since these match 1:1
            raceOGCategories.add(i)
        for i in list(seldemCTO[nctid].baseline_measurements['Ethnicity']):
            ethnicityOGCategories.add(i)
            #get the race/ethnicity categories from csv this tag belongs to
            try:
                raceTag = categoryClasses[i][0]
                ethnicityTag = categoryClasses[i][1]
            except KeyError as ke:
                print("Invalid Key, Check CSV File and add classification for:", ke)
                continue
            if ethnicityTag == "unspecified": #Not an ethnicity tag, so add only for race and move on, remove it from ethnicity
                seldemCTO[nctid].baseline_measurements['Race'][raceTag] = seldemCTO[nctid].baseline_measurements['Ethnicity'][i]
                seldemCTO[nctid].baseline_measurements['Ethnicity'].pop(i, None) #Remove old  
            else: #Is an ethnicity tag, might be a race tag too
                topop = False
                if ethnicityTag != i: #Skip stuff that is equal to optimize.
                    #This code is for some weird cases where ethnicity for hispanics is split by race, example: NCT00291161
                    if ethnicityTag in seldemCTO[nctid].baseline_measurements['Ethnicity']: #Already exist so we add to current sum
                        seldemCTO[nctid].baseline_measurements['Ethnicity'][ethnicityTag] = \
                        seldemCTO[nctid].baseline_measurements['Ethnicity'][ethnicityTag] + seldemCTO[nctid].baseline_measurements['Ethnicity'][i]
                    else: #doesnt exist so just create it and put value
                        seldemCTO[nctid].baseline_measurements['Ethnicity'][ethnicityTag] = seldemCTO[nctid].baseline_measurements['Ethnicity'][i]
                    topop = True
                if raceTag != 'unknown or not reported':
                    seldemCTO[nctid].baseline_measurements['Race'][raceTag] = seldemCTO[nctid].baseline_measurements['Ethnicity'][i]
                    topop = True
                if topop:
                    seldemCTO[nctid].baseline_measurements['Ethnicity'].pop(i, None) #Remove only after we are done using it


    #Set Predefined Categories by Dr. Cummings and Dr. Samantha John
    #"Biological Sex at Birth"
    sexCleanCategories       = set(['male','female','unspecified, gender unknown, or other'])
    #"Ethnicities"
    ethnicityCleanCategories = set(['hispanic, latino, or spanish origin', 'not of hispanic, latino, or spanish origin', 'unspecified'])
    #"Race"
    raceCleanCategories      = set(['white', 'black or african american', 'american indian or alaska native', 'asian', 
                                    'native hawaiian or other pacific islander', 'more than one race','unknown or not reported'])
    #Other, unknown, unspecified race (includes categories with multiple interpretations)

    #Error Checking:
    if raceOGCategories != raceCleanCategories:
        print("Warning: Race Unmatched")
    

    #Create main list holding demograhpics for each trial
    demographicTable = [] #will Hold table of Demographic Data. Organized as follows:
    #NCTID, HyperlinkedNCTID, Condition, Sex/Races/Ethnicities in the order of columnNames
    columnNames = sorted(sexCleanCategories) + sorted(ethnicityCleanCategories) + sorted(raceCleanCategories) #First Row and Key
    precollabel = [] #Labels the Type above the columnName
    for i in sorted(sexCleanCategories): precollabel.append('Sex')
    for i in sorted(ethnicityCleanCategories): precollabel.append('Ethnicity')
    for i in sorted(raceCleanCategories): precollabel.append('Race')

    #Main data
    for nctid in seldemCTO:
        hyperlinkedNCTID = "=HYPERLINK(\"https://www.clinicaltrials.gov/ct2/show/results/"+nctid+"\", \""+nctid+"\")"
        currRow = [seldemCTO[nctid].nctid, hyperlinkedNCTID,
                   ', '.join(seldemCTO[nctid].getConditionAcronyms())] #save first 3 columns
        for col in columnNames:
            if col in seldemCTO[nctid].baseline_measurements['Sex']:
                currRow.append(seldemCTO[nctid].baseline_measurements['Sex'][col])
            elif col in seldemCTO[nctid].baseline_measurements['Ethnicity']:
                currRow.append(seldemCTO[nctid].baseline_measurements['Ethnicity'][col])
            elif col in seldemCTO[nctid].baseline_measurements['Race']:
                currRow.append(seldemCTO[nctid].baseline_measurements['Race'][col])
            else:
                currRow.append('') #No entry in this column for this row
        currRow.append(seldemCTO[nctid].firstpostedDate) #Shows first posted date
        currRow.append(seldemCTO[nctid].lastpostedDate)  #shows last posted date
        currRow.append(seldemCTO[nctid].getCountryDataStr()) #Shows Country Data
        currRow.append(seldemCTO[nctid].countryType) #Shows Country Type String
        currRow.append(seldemCTO[nctid].getSponsorDataStr()) #Shows Sponsor Data
        currRow.append(seldemCTO[nctid].title) #Shows trial title
        currRow.append(seldemCTO[nctid].getInterventionDrugsStr()) #Intervention list added
        demographicTable.append(currRow)
    
    #Add Aggregate Columns of each row (so like total of all ethnicities, etc)
    precollabel.insert(len(sexCleanCategories)+len(ethnicityCleanCategories)+len(raceCleanCategories), "Race Total")
    precollabel.insert(len(sexCleanCategories)+len(ethnicityCleanCategories), "Ethnicity Total")
    precollabel.insert(len(sexCleanCategories), "Sex Total")
    columnNames.insert(len(sexCleanCategories)+len(ethnicityCleanCategories)+len(raceCleanCategories), "Race Total")
    columnNames.insert(len(sexCleanCategories)+len(ethnicityCleanCategories), "Ethnicity Total")
    columnNames.insert(len(sexCleanCategories), "Sex Total")
    for i in range(len(demographicTable)):
        sumS = 0
        sumR = 0
        sumE = 0
        for j in range(3,len(sexCleanCategories)+3): 
            if demographicTable[i][j] != '':
                sumS += demographicTable[i][j]
        for j in range(len(sexCleanCategories)+3,len(sexCleanCategories)+len(ethnicityCleanCategories)+3): 
            if demographicTable[i][j] != '':
                sumE += demographicTable[i][j]
        for j in range(len(sexCleanCategories)+len(ethnicityCleanCategories)+3,
                       len(sexCleanCategories)+len(ethnicityCleanCategories)+len(raceCleanCategories)+3): 
            if demographicTable[i][j] != '':            
                sumR += demographicTable[i][j]        
        demographicTable[i].insert(len(raceCleanCategories)+len(ethnicityCleanCategories)+len(sexCleanCategories)+3,sumR)
        demographicTable[i].insert(len(sexCleanCategories)+len(ethnicityCleanCategories)+3,sumE)
        demographicTable[i].insert(len(sexCleanCategories)+3,sumS)
    #Sum Column Totals for Aggregation
    colTotals = []
    for i in range(3,len(demographicTable[0])-7): #Skip first 3 and last 7 (Extra rows at end that are other information)
        rowTotal = 0 #It's important that this^ number here is updated whenever you add an extra column!
        for row in demographicTable:
            if row[i] != '':
                try:
                    rowTotal += row[i]
                except:
                    print("Warning: Skipped Invalid Row Data in Demographic Table")
        colTotals.append(rowTotal)
    #TODO do some aggregate data summaries and merge similar tables.

    #Generate Report for AD/MCI Demographics
    headings = [] #Stores copy of the headings we write formatted so we can return them in addition to writing them
    with open('output/ADMCIdemographics.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        headings.append(['Total AD/MCI Trials Checked:'])
        headings.append([len(selCTO)])
        headings.append(['Total AD/MCI Trials with Demographics Available:'])
        headings.append([len(seldemCTO)])
        headings.append([]) #empty Line
        headings.append(['Categories:'])
        headings.append(['Sex:'])
        for entry in sorted(sexCleanCategories):
            headings.append([entry])
        headings.append([]) #empty Line
        headings.append(['Ethnicity:'])
        for entry in sorted(ethnicityCleanCategories):
            headings.append([entry])
        headings.append([]) #empty Line
        headings.append(['Race:'])
        for entry in sorted(raceCleanCategories):
            headings.append([entry])
        headings.append([]) #empty Line
        headings.append(['Demographics Available for Each Trial by Type:'])
        headings.append(['Total Columns: '+str(len(columnNames))])
        headings.append(['Type of Column', '', '']+precollabel+['','']) #Columns of Big Table
        headings.append(['NCTID', 'NCTID HyperLink', 'Condition']+columnNames+['First Posted Date', 'Last Posted Date',
                          'Countries', 'Type: US-ONLY, NON-US, GLOBAL (US and at least 1 Non-US country), or NONE (no country listed)',
                          'Sponsors', 'Trial Title', 'Intervention(s)']) #Columns of Big Table
        headings.append(['Totals', str(len(demographicTable)), 'Trials']+colTotals+['','']) #Columns of Big Table
        outfile.writerows(headings) #Write all headings
        outfile.writerows(demographicTable) #Write all rows 
    return headings, demographicTable #Returns the main table (not headings) so we send it to excel later
#End Function

#Demographics from baseline_measurements in Clincial Trials (chartsv4E)
#We are going to do it the same as how we did it for the design_outcomes section in nddfilter.py so code very similar to that 
def baselinemeasurenddfilter(allNCTIDs): #Requires a set containing all NCTIDs we want
    nddbaselinemeasure = [] #stores baseline measurements:
    #id, nct_id, result_group_id, ctgov_group_code, classification, category, title, description, units, 
    #param_type, param_value, param_value_num, dispersion_type, dispersion_value, dispersion_value_num, 
    #dispersion_lower_limit, dispersion_upper_limit, explanation_of_na
    with open("queries/chartsv4E.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            if row[1] in allNCTIDs: #compare NCTID of allNCTIDs with the row in chartsv4E if match then this is from a trial we care about (NDD)
                nddbaselinemeasure.append(row) #if we found a match in nddtrials we insert and move on to next row in chartsv4E

    #next we sort the resulting list by NCTID
    sorted_nddbaselinemeasure = sorted(nddbaselinemeasure, key=lambda row: row[1], reverse=False) #sort by nctid, stable sort (ROW 1 is NCTID IN THIS CASE!)

    with open('output/nddbaselinemeasure.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(sorted_nddbaselinemeasure)

#Loads CSV File containing the classification for all the variations in sex, race, and ethnicity categories.
# Stores it in a dictionary where each variation in one of is key. contents is the race and ethnicity that key belongs to
# Example: caucasian, white, unspecified --->  caucasian is stored as Race: white, Ethnicity: Unspecified. (but all lower case)
def loadSREcategories(categoryClasses):
    rowCount = -1 #Skip first row
    with open("input/demographics/srecategories.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            rowCount += 1
            if rowCount == 0: 
                continue #skip first row
            #col 0 is original tag, col 1 is clean race tag, col 2 is ethnicity tag
            categoryClasses[row[0].lower()] = [row[1].lower(), row[2].lower()] 
    #return categoryClasses
#End Function

#End File