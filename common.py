#This file contains all the common objects/list/classes used in the program
import csv 

class jfc:
    diseaseAcronymsChecked = {"AD", "ALS", "CBD", "CTE", "LBD", "DLB", "LWB", "FTDLD", "HD", "MSA", "PD", "PSP", "MCI"}

    diseaseLongChecked = {"Alzh","Amyotro","Chronic Traumatic Encephalopathy","Corticobasal Degen",
                      "Dementia With Lewy Bodies","Frontotemporal","Huntington","Multiple System Atrophy",
                      "Parkin","Progressive Supranuclear Palsy", "Mild Cognitive Impairment"}

    #To try partial matching
    diseaselowercase = {"alzh","amyotro","chronic traumatic encephalopathy","corticobasal degen",
                      "dementia with lewy bodies","frontotemporal","huntington","multiple system atrophy",
                      "parkin","progressive supranuclear palsy", "mild cognitive impairment", "palsy", " pd ",
                      " msa ", " ad ", "ftdld", " dlb ", "lewy body dementia", "(pd,", "lewy body disease",
                      "multiple systems atrophy", "lewy body dementia"}

    #So this one is so we can see if diseases are different by using the power of hashing
    #only meant for duplicate removal atm
    diseaseHashMap = {
        "AD": "AD",
        " pd ": "PD",
        " ad ": "AD",
        "ALS": "ALS",
        "CBD": "CBD",
        "CTE": "CTE",
        "DLB": "DLB",
        " dlb ": "DLB",
        "LWB": "LWB",
        "FTDLD": "FTDLD",
        "ftdld": "FTDLD",
        "HD": "HD",
        "MSA": "MSA",
        " msa ": "MSA",
        "PD": "PD",
        "(pd,": "PD",
        "PSP": "PSP",
        "MCI": "MCI",
        "Alzh": "AD",
        "alzh": "AD",
        "ALZ" : "AD", #TODO, use to lower in getCleanCondition....
        "Amyotro": "ALS",
        "amyotro": "ALS",
        "Alzheimer's Disease": "AD",
        "Corticobasal Degeneration": "CBD",
        "corticobasal degen": "CBD",
        #"Lewy Body Disease": "LWB",
        "Frontotemporal Lobar Degeneration": "FTDLD",
        "Huntington's Disease": "HD",
        "huntington": "HD",
        "Parkinson's Disease": "PD",
        "Amyotrophic Lateral Sclerosis": "ALS",
        "AMYOTROPHIC LATERAL SCLEROSIS": "ALS",
        "Chronic Traumatic Encephalopathy": "CTE",
        "chronic traumatic encephalopathy": "CTE",
        "Encephalo": "CTE",
        "Corticobasal Degen": "CTE",
        "Cortico": "CTE",
        "Dementia With Lewy Bodies": "DLB",
        "Dementia with Lewy Bodies": "DLB",
        "dementia with lewy bodies": "DLB",
        "Lewy Body Dementia": "DLB",
        "lewy body dementia": "DLB",
        "Dementia, Lewy Body": "DLB",
        "Lewy Body Disease": "DLB",
        "lewy body disease": "DLB",
        "Frontotemporal": "FTDLD",
        "frontotemporal": "FTDLD",
        "Fronto": "FTDLD",
        "Huntington": "HD",
        "Multiple System Atrophy": "MSA",
        "multiple system atrophy": "MSA",
        "Multiple Systems Atrophy": "MSA",
        "multiple systems atrophy": "MSA",
        "Parkin": "PD",
        "parkin": "PD",
        "PARKIN": "PD",
        "Progressive Supranuclear Palsy": "PSP",
        "progressive supranuclear palsy": "PSP",
        "Supranuclear Palsy, Progressive": "PSP",
        "supranuclear palsy": "PSP",
        "Palsy": "PSP",
        "palsy": "PSP",
        "Parkinson": "PD",
        "Mild Cognitive Impairment": "MCI",
        "MILD COGNITIVE IMPAIRMENT": "MCI",
        "Mild CognitIve Impairment": "MCI",
        "mild cognitive impairment": "MCI",
        "Healthy Volunteers": " " #could also do "HV"
    }


    diseaseinTitleChecked = {"Chronic Traumatic Encephalopathy","Corticobasal Degen","Dementia With Lewy Bodies",
                         "Frontotemporal","Huntington","Multiple System Atrophy",
                         "Parkinson","Progressive Supranuclear Palsy", "Mild Cognitive Impairment"}

    #New Disease Hash Map for getCleanCondition
    #"AD", "ALS", "CBD", "CTE", "DLB", "LWB", "FTDLD", "HD", "MSA", "PD", "PSP"
    diseaseAcronymFullNameMap = {
        "AD": "Alzheimer's Disease",
        "ALS": "Amyotrophic Lateral Sclerosis",
        "CBD": "Corticobasal Degeneration",
        "CTE": "Chronic Traumatic Encephalopathy",
        "DLB": "Dementia With Lewy Bodies",
        "LBD": "Dementia With Lewy Bodies",
        "LWB": "Lewy Body Disease",
        "FTDLD": "Frontotemporal Lobar Degeneration",
        "HD": "Huntington's Disease",
        "MSA": "Multiple System Atrophy",
        "PD": "Parkinson's Disease",
        "PSP": "Progressive Supranuclear Palsy",
        "MCI": "Mild Cognitive Impairment"
    }

    diseaseFullNames = { #Set with full name of diseases for string matching
        "Alzheimer's Disease",
        "Amyotrophic Lateral Sclerosis",
        "Corticobasal Degeneration",
        "Chronic Traumatic Encephalopathy",
        "Dementia With Lewy Bodies",
        "Lewy Body Disease",
        "Frontotemporal Lobar Degeneration",
        "Huntington's Disease",
        "Multiple System Atrophy",
        "Parkinson's Disease",
        "Progressive Supranuclear Palsy",
        "Mild Cognitive Impairment",
        "Healthy Volunteers"
    }
    @staticmethod #Function that checks if the drugname is ok to add (currently removed placebo, but we can add stopwords here)
    def drugnameCheckOK(drugname): #Also going to check for control since that is control group
        dname = drugname.lower()
        if "placebo" not in dname and "control" not in dname: #If there is placebo we want to return false
            return True
        else:
            return False

    #Function that returns clean condition name for comparison. NEW FUNCTION 
    @staticmethod
    def getCleanCondition(cond):
        cleanCond = cond
        if cleanCond in jfc.diseaseAcronymsChecked:
            cleanCond = jfc.diseaseAcronymFullNameMap[cleanCond] #Standard Acronym so we're fine
            return cleanCond #split into two lines for debugging
        elif cleanCond in jfc.diseaseFullNames:
            return cleanCond #perfect match!
        else:
            for entry in jfc.diseaseHashMap:
                if entry in cleanCond:
                    cleanCond = jfc.diseaseAcronymFullNameMap[jfc.diseaseHashMap[entry]]
                    return cleanCond
        #fi we reach here the for loop failed to find something so we need to see what it was!
        print("WARNING: Unable to Identify Condition:", cond)
        return cleanCond

    #Class to more cleanly store the trials (which we will then convert to JSON for the App)
    class clinicalTrial:
        def __init__(self, nctid, title, condition, intervention, otherIntervention, lastpostedDate, 
                    phase, acronym, enrollment, timeFrame, firstpostedDate,
                    studyStatus, flexibleCondition=False): #outcomeTitle #outcomeDescription
            self.nctid = nctid
            self.title = title
            self.condition = []
            self.intervention = []
            self.otherIntervention = []
            self.lastpostedDate = lastpostedDate
            self.phase = phase #phase.replace("Phase ", "P") #for our table appearance
            self.acronym = acronym
            self.enrollment = enrollment
            self.timeFrame = timeFrame
            self.designTimeFrame = "" #We will add this later
            self.designMeasures = [] #We will add this later
            self.designDescription = [] #We will add this later
            self.countries = [] #We will add this later
            self.countryType = "" #We will update this later to indicate if it is US-ONLY/NON-US/GLOBAL/NONE (no country)
            self.sponsors = [] #We will add this later
            self.firstpostedDate = firstpostedDate
            self.studyStatus = studyStatus
            self.outcomeTitle = [] #we will add these later
            self.outcomeDescription = [] #we will add these later
            self.eligibilityCriteria = [] #we optionally can add these later
            self.nddInEligCriteria = [] #we optionally can add these later, if any, only stores NDD that dont appear already in conditions
            self.baseline_measurements = {} #Dictionary  to hold all the different demographic data for each trial, if we have any
            self.hasDemographics = False #Stores boolean if we have demographic data for this trial (Only result trials have it)
            #By default we want warnings if condition isn't found in hashmap but can disable for non NDD Trials. So we used default
            self.flexibleCondition = flexibleCondition #paramater set to false so can only actively disable the check
            self.addCondition(condition)
            self.addInterventions(intervention, 0)
            self.addInterventions(otherIntervention, 1)
        def addCondition(self, cond):
            #Todo, clean up condition by storing under one clean name so like no mispellings, also dont store dups
            if not self.flexibleCondition:
                cleanCond = jfc.getCleanCondition(cond)
            else: #Flexible condition, throw it in do no checks. Yolo
                cleanCond = cond
            if cleanCond not in self.condition:
                self.condition.append(cleanCond)
        def addInterventions(self, intervention, intType):
            if intervention == "":
                return #don't add empty stuff
            if intType == 0: #intervention
                if intervention not in self.intervention:
                    self.intervention.append(intervention) #to avoid duplicates
            else: #other intervention
                if intervention not in self.otherIntervention:
                    self.otherIntervention.append(intervention)
        def setFlexibleCondition(self): #Enables flexibility in condition, will disable warning
            self.flexibleCondition = True
        def addOutcome(self, oT, oD):
            if oT not in self.outcomeTitle:
                self.outcomeTitle.append(oT)
            if oD not in self.outcomeDescription:
                self.outcomeDescription.append(oD)
        def addDesignOutcomes(self, dMeasure, dTimeFrame, dDescription):
            self.designTimeFrame = dTimeFrame
            if dMeasure not in self.designMeasures:
                self.designMeasures.append(dMeasure)
            if dDescription not in self.designDescription:
                self.designDescription.append(dDescription)
        def addEligibilityCriteria(self, e):
            if e not in self.eligibilityCriteria:
                self.eligibilityCriteria.append(e)
        def addNDDInEligCriteria(self, nddlist): #Note this only stores clean version, aka not NDD that appear in cond already
            if isinstance(nddlist, list):
                for ndd in nddlist: #list of them try to insert one at a time
                    if ndd not in self.nddInEligCriteria:
                        self.nddInEligCriteria.append(ndd)
            else: #not a list, single NDD so try to insert it directly
                if nddlist not in self.nddInEligCriteria:
                    self.nddInEligCriteria.append(nddlist)
        def getShortPhase(self):
            return self.phase.replace("Phase ", "P") #for our table appearance
        def getShortTimeFrame(self):
            if self.timeFrame != "":
                shortend = self.timeFrame
            else:
                shortend = self.designTimeFrame
            shortend = shortend.replace("months", "m")
            shortend = shortend.replace("days", "d")
            shortend = shortend.replace("weeks", "w")
            return shortend
        def getConditionAcronyms(self): #Returns acronyms of all conditions here as a list
            if(self.flexibleCondition): #If flexible condition is enabled we can't generate acronyms
                return self.condition #so just return the raw condition list.
            cond = []
            for i in self.condition:
                #for x in jfc.diseaseHashMap: #for when we dont trust if there are errors
                #    if x in i:
                #        cleanCond = x
                #        break
                #cond.append(jfc.diseaseHashMap[cleanCond])
                cond.append(jfc.diseaseHashMap[i]) #For when there are no errors   (We ought to be ok)
            return cond
        def getConditionAcronymsStr(self): #Returns acronyms of all conditions here as a list
            condlist = self.getConditionAcronyms()
            finalstring = ""
            if len(condlist) > 0:
                finalstring = condlist[0]
                if len(condlist) > 1:
                    for i in range(1,len(condlist)):
                        finalstring += ", " + condlist[i] #for comma to look nice
            return finalstring
        def getNDDInEligCriteriaStr(self): #Returns string version of nddInEligCriteria
            finalstring = ""
            if len(self.nddInEligCriteria) > 0:
                finalstring = self.nddInEligCriteria[0]
                if len(self.nddInEligCriteria) > 1:
                    for i in range(1, len(self.nddInEligCriteria)):
                        finalstring += ", " + self.nddInEligCriteria[i] #for comma to look nice
            return finalstring
        def getComboStatus(self): #Function that returns the fancy YEAR; Status from table
            return str(self.getOnlyDateYear(self.lastpostedDate)) + "; " + self.studyStatus
        def getTablePrimaryOutcomeStr(self): #makes string with the outcome titles separated by a ;
            finalstr = ""
            if len(self.outcomeTitle) > 0:
                finalstr = self.outcomeTitle[0]
                if len(self.outcomeTitle) > 1: #nasty logic to get ; in right spot!
                    for i in range(1,len(self.outcomeTitle)):
                        finalstr += "; " + self.outcomeTitle[i]
            #If the above fails, let's look in Design_Outcome(s)!
            elif len(self.designMeasures) > 0:
                finalstr = self.designMeasures[0]
                if len(self.designMeasures) > 1: #nasty logic to get ; in right spot!
                    for i in range(1,len(self.designMeasures)):
                        finalstr += "; " + self.designMeasures[i]
            return finalstr
        def getTableBiomarkerOutcomeStr(self): #TODO, gotta figure out how to magically get these from primary outcomes... 
            #may be able to use the outcomes.descriptions to do this at some point
            finalstr = ""
            return finalstr
        def generateTableRow(self, withEC=False): #Returns formatted list representing csv entry to fill out, leaves drug/match space blank
            #The default parameter withEC can be set to True in call to print out extra column of NDD in Eligbility Criteria.
            finalrow = [] #We will return a 1 dimensional list
            finalrow.append("") #column[0] is empty, I'll either keep empty for formatting or I'll add drug match if it's the first of a set
            finalrow.append(self.nctid) #column[1] is NCTID  (this is all coming from Cross NDD worksheet Dr. Cummings sent as template)
            finalrow.append(self.getShortPhase()) #column[2] is the Phase but shortened
            finalrow.append(self.getConditionAcronymsStr()) #column[3] is the Diagnosis, AKA condition. 
            #Acronym isnt very reliable so instead used the condition name, but can revisit acronym at some point
            if withEC: #This is optional column only added if withEC enabled
                finalrow.append(self.getNDDInEligCriteriaStr())
            finalrow.append(self.enrollment) #column[4] Number of participants
            finalrow.append(self.getShortTimeFrame()) #column[5] Duration of Trial
            finalrow.append(self.getTablePrimaryOutcomeStr()) #column[6] Primary Outcome(s)
            finalrow.append(self.getTableBiomarkerOutcomeStr()) #column[7] Biomarker Outcome(s)
            finalrow.append(self.getOnlyDateYear(self.firstpostedDate)) #column[8] Year Registered
            finalrow.append(self.getComboStatus()) #column[9] Status (combo of last post date and actual status)
            return finalrow
        def getInterventionDrugsStr(self): #This tries to make a string with the drug name, for now just interventions, but 
            #we may eventually make this more sophisticated
            finalstr = ""
            if len(self.intervention) > 0:
                finalstr = self.intervention[0]
                if len(self.intervention) > 1: #nasty logic to get , in right spot!
                    for i in range(1,len(self.intervention)):
                        if jfc.drugnameCheckOK(self.intervention[i]): #False if placebo is in name
                        #if self.intervention[i].lower() != 'placebo': #get rid of placebo
                           finalstr += ", " + self.intervention[i]
            elif len(self.otherIntervention) > 0:
                finalstr = self.otherIntervention[0]
                if len(self.otherIntervention) > 1: #nasty logic to get , in right spot!
                    for i in range(1,len(self.otherIntervention)):
                        if jfc.drugnameCheckOK(self.otherIntervention[i]): #false if placebo in name
                        #if self.otherIntervention[i].lower() != 'placebo': #get rid of placebo
                           finalstr += ", " + self.otherIntervention[i]
            return finalstr
        def getCountryDataStr(self): #This function returns a nicely formatted string with country data
            if len(self.countries) == 0:
                return "No Country Data Available" #For no data
            finalcstr = ""
            removedcountries = ""
            for i in self.countries:
                if not i[1]: #if country removed is set to false just add it
                    finalcstr += i[0] + ", "
                else:
                    removedcountries += i[0] + ", "
            if finalcstr == "": #This trial has no countries added, just removed so write word NONE to flag it
                finalcstr += "NONE, " #adding comma and space just for consistency
            if removedcountries != "": #we have removed countries, append at end
                finalcstr = finalcstr[:-2] #removed extra comma and space
                finalcstr += " / Removed Countries: " + removedcountries #add removed countries
            return finalcstr[:-2] #removed extra comma and space
        def getSponsorDataStr(self): #This function returns all sponsor data smashed together as a big string. Kinda messy
            if len(self.sponsors) == 0:
                return "No Sponsor Data Available" #For no data
            finalsponsorstr = ""
            for i in self.sponsors: #Agency Class, Lead or Collab, Name
                finalsponsorstr += i[0] + ", " + i[1] + ", " + i[2] + "; "
            return finalsponsorstr[:-2]
        @staticmethod
        def getOnlyDateYear(d):  #Static Function gets only the year from a date string (i.e: last posted date or first posted date)
            return d[0:4]
        def __str__(self):
            printstr = "NCTID: " + self.nctid + "\nTitle: " + self.title + "\nFirst Posted Date: " \
            + self.firstpostedDate + "\nLast Posted Date: " + self.lastpostedDate + "\nPhase: " \
            + self.phase + ", Acronym: " + self.acronym + ", Enrollment: " \
            + self.enrollment + "\nTime Frame: " + self.timeFrame + "\nCondition(s): "  #The \ is some python magic for multi-line i guess lol
            for i in self.condition:
                printstr += i + "\n"
            printstr += "Intervention(s): "
            for i in self.intervention:
                printstr += i + "\n"
            printstr += "Intervention(s) Other Name(s): "
            for i in self.otherIntervention:
                printstr += i + "\n"
            if len(self.outcomeTitle) > 0:
                printstr += "Outcome(s): "
                if len(self.outcomeTitle) != len(self.outcomeDescription):
                    printstr += "Warning Outcome Title / Descriptions do not match!" 
                    printstr += str(len(self.outcomeTitle)) + ", " + str(len(self.outcomeDescription)) + "\n" 
                else:
                    for i in range(len(self.outcomeTitle)):
                        printstr += "Title: " + self.outcomeTitle[i] + "\n"
                        printstr += "Description: " + self.outcomeDescription[i] + "\n"
            else:
                printstr += "No Outcomes Listed.\n"
            #Currently we do not print eligibility criteria, if we want to we can uncomment this to print them
            #if len(self.eligibilityCriteria) > 0:
            #    printstr += "Eligibility Criteria: "
            #    for e in self.eligibilityCriteria:
            #        printstr += str(e)
            if len(self.nddInEligCriteria) > 0: #For NDD in Eligibility Criteria
                printstr += "NDD Listed in Eligibility Criteria that do not appear in Condition(s):\n"
                printstr += self.getNDDInEligCriteriaStr() + "\n"
            if self.hasDemographics: #For Demographics, for now just tells if we have. Not doing detailed writing of it here.
                printstr += "Trial Has Demographics Data.\n"
            printstr += "Country Data: " + self.getCountryDataStr() #Country data
            printstr += ". Type: " + self.countryType + "\n"
            printstr += "Sponsor Data: " + self.getSponsorDataStr() + "\n" #Sponsor Data
            return printstr
    #End clinicalTrial class
    class drugClinicalTrialSet: #Class I use instead of a dictionary for Tables 1 and 3
        def __init__(self, drugname):
            self.drugname = drugname
            self.clinicalTrialList = []
        def insertClinicalTrial(self, newCT):
            self.clinicalTrialList.append(newCT)
        def __str__(self):
            printstr = "Drugname: " + self.drugname + "\n"
            for ctrial in self.clinicalTrialList:
                printstr += str(ctrial)
            return printstr
    @staticmethod
    def cleanOutputFiles():
        import os
        try:
            for f in os.scandir("output/json-tables"):
                os.remove(f.path)
            for f in os.scandir("output/classified-tables"):
                os.remove(f.path)
            for f in os.scandir("output/final-tables/hyperlinked"):
                os.remove(f.path)
            for f in os.scandir("output/final-tables"):
                if not f.is_dir(): #Don't try to delete directories or this explodes
                    os.remove(f.path)
        except:
            print("Warning: Issues Cleaning up output directory before starting run")
    @staticmethod
    def writeListToFileSorted(dataToWrite, fdir, fname): #Small function to write to a file a list of sorted items
        sortedData = sorted(dataToWrite)
        f = open(fdir + fname + ".txt", "w")
        for entry in sortedData:
            f.write(entry)
            f.write("\n")
        f.close()
#END jfc