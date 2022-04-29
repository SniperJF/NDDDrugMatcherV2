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
    sexCategories       = set() #Store all categories
    ethnicityCategories = set() #Store all categories
    raceCategories      = set() #Store all categories
    for nctid in seldemCTO:
        for i in seldemCTO[nctid].baseline_measurements['Sex']:
            sexCategories.add(i)
        for i in seldemCTO[nctid].baseline_measurements['Ethnicity']:
            ethnicityCategories.add(i)
        for i in seldemCTO[nctid].baseline_measurements['Race']:
            raceCategories.add(i)

    #Create main list holding demograhpics for each trial
    demographicTable = [] #will Hold table of Demographic Data. Organized as follows:
    #NCTID, HyperlinkedNCTID, Condition, Sex/Races/Ethnicities in the order of columnNames
    columnNames = sorted(sexCategories) + sorted(ethnicityCategories) + sorted(raceCategories) #First Row and Key
    precollabel = [] #Labels the Type above the columnName
    for i in sorted(sexCategories): precollabel.append('Sex')
    for i in sorted(ethnicityCategories): precollabel.append('Ethnicity')
    for i in sorted(raceCategories): precollabel.append('Race')

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
        currRow.append(seldemCTO[nctid].lastpostedDate)
        currRow.append(seldemCTO[nctid].title)
        demographicTable.append(currRow)
    
    #Add Aggregate Columns of each row (so like total of all ethnicities, etc)
    precollabel.insert(len(sexCategories)+len(ethnicityCategories)+len(raceCategories), "Race Total")
    precollabel.insert(len(sexCategories)+len(ethnicityCategories), "Ethnicity Total")
    precollabel.insert(len(sexCategories), "Sex Total")
    columnNames.insert(len(sexCategories)+len(ethnicityCategories)+len(raceCategories), "Race Total")
    columnNames.insert(len(sexCategories)+len(ethnicityCategories), "Ethnicity Total")
    columnNames.insert(len(sexCategories), "Sex Total")
    for i in range(len(demographicTable)):
        sumS = 0
        sumR = 0
        sumE = 0
        for j in range(3,len(sexCategories)+3): 
            if demographicTable[i][j] != '':
                sumS += demographicTable[i][j]
        for j in range(len(sexCategories)+3,len(sexCategories)+len(ethnicityCategories)+3): 
            if demographicTable[i][j] != '':
                sumE += demographicTable[i][j]
        for j in range(len(sexCategories)+len(ethnicityCategories)+3,
                       len(sexCategories)+len(ethnicityCategories)+len(raceCategories)+3): 
            if demographicTable[i][j] != '':            
                sumR += demographicTable[i][j]        
        demographicTable[i].insert(len(raceCategories)+len(ethnicityCategories)+len(sexCategories)+3,sumR)
        demographicTable[i].insert(len(sexCategories)+len(ethnicityCategories)+3,sumE)
        demographicTable[i].insert(len(sexCategories)+3,sumS)
    #Sum Column Totals for Aggregation
    colTotals = []
    for i in range(3,len(demographicTable[0])-2): #Skip first 3 and last 2
        rowTotal = 0
        for row in demographicTable:
            if row[i] != '':
                try:
                    rowTotal += row[i]
                except:
                    print("Warning: Skipped Invalid Row Data in Demographic Table")
        colTotals.append(rowTotal)
    #TODO do some aggregate data summaries and merge similar tables.

    #Generate Report for AD/MCI Demographics
    with open('output/ADMCIdemographics.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerow(['Total AD/MCI Trials Checked:'])
        outfile.writerow([len(selCTO)])
        outfile.writerow(['Total AD/MCI Trials with Demographics Available:'])
        outfile.writerow([len(seldemCTO)])
        outfile.writerow([]) #empty Line
        outfile.writerow(['Categories:'])
        outfile.writerow(['Sex:'])
        for entry in sorted(sexCategories):
            outfile.writerow([entry])
        outfile.writerow([]) #empty Line
        outfile.writerow(['Ethnicity:'])
        for entry in sorted(ethnicityCategories):
            outfile.writerow([entry])
        outfile.writerow([]) #empty Line
        outfile.writerow(['Race:'])
        for entry in sorted(raceCategories):
            outfile.writerow([entry])
        outfile.writerow([]) #empty Line
        outfile.writerow(['Demographics Available for Each Trial by Type:'])
        outfile.writerow(['Total Columns: '+str(len(columnNames))])
        outfile.writerow(['Type of Column', '', '']+precollabel+['','']) #Columns of Big Table
        outfile.writerow(['NCTID', 'NCTID HyperLink', 'Condition']+columnNames+['Last Posted Date','Trial Title']) #Columns of Big Table
        outfile.writerow(['Totals', str(len(demographicTable)), 'Trials']+colTotals+['','']) #Columns of Big Table
        outfile.writerows(demographicTable) #Write all rows 

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