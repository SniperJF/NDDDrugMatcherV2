#Pre processing the query files to only handle the NDD trials we want for speeding up matching and not dealing with large files
#Also sorts by NCTID resulting csvs (stores to output folder)
#Current Runtime: 1 minute 36 seconds. 

import csv
#import json #For JSON Export/Imports
from common import jfc
from eligcritprocesser import writeECTrialsfromNCTIDset

# Row Contents
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


matchentries = [] #store matches
nddoutcomes = [] #stores nctid, outcome title/desc of relevant entries that match matchentries
ndddesignoutcomes = [] #stores design outcomes nctid, measure, time frame, description (fills in missing stuff from normal outcomes)
nddeligibilities = [] #stores nctid and elgibility criteria (for finding mentions of diseases that we are interested in)
ignoretrials = set() #stores nctid of trials we want to ignore - used to ignore eligibility trials that are beyond time range we want
trialsSaved = set() #stores nctid of all trials we currently identified as with a ndd
with open("queries/chartsv4A.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        #Since we want time range 2010 to 2021 we are going to splice it from the string. Example 2018-06-23 we will take the
        #2018 which is first 4 characters , cast to number, then compare if that value is in our range! else continue
        #if int(row[5][0:4]) < 2010 or int(row[5][0:4]) > 2021: #so 2009 or 2022 would not show up
        if int(row[10][0:4]) < 2000 or int(row[10][0:4]) > 2021: #Changed range for demographic study, using FIRST POSTED DATE 2000-2021
            ignoretrials.add(row[0])
            continue #Remove these three lines to disable dating limits

        toappend = False #becomes true when we find something with a matching NDD
        #Check diseases in disease section
        for disease in jfc.diseaseLongChecked: #check standard names
            if disease in row[2]:
                toappend = True
                break
        #Check acronyms
        if (toappend == False) and (row[2] in jfc.diseaseAcronymsChecked):
            toappend = True
        #Removed row[7] acronym check because it was useless and got all false positives
        #Check studies on healthy individuals that mention disease in the title of the trial.
        if (toappend == False) and ("Healthy Volunteers" in row[2]):
            for disease in jfc.diseaseinTitleChecked:
                if disease in row[1]:
                    toappend = True

        #check lowercase or any title stuff we missed
        if (toappend == False):
            for disease in jfc.diseaselowercase:
                if disease in row[2].lower():
                    toappend = True
                    break

        if toappend:
            matchentries.append(row)
            trialsSaved.add(row[0]) #save this nctid as a trial we want to save in pass #2

#first pass we get all NCTIDs we want, second pass we want to do a check of NCTID we skipped that have relevant titles
#to see if a trial has a NDD title but no mention of NDD
reviewskipped = [] #stores all trials we may want to review because they contain NDD in title, but not in condition
multiplereview = {} #Has Trial and conditions matched. Used to then find the ones that have more than 1 condition
multiplereviewfinal = [] #NDD trials that contain multiple NDD in title. Higher priority to review!
with open("queries/chartsv4A.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        if row[0] not in trialsSaved and row[0] not in ignoretrials: #if we arent saving it and we arent ignoring it
            for disease in jfc.diseaselowercase:
                if disease in row[1].lower(): #to see if this catches anything
                    reviewskipped.append([jfc.diseaseHashMap[disease],row[0],row[1],row[2],row[3],row[4]]) 
                    if row[0] in multiplereview:
                        multiplereview[row[0]].add(jfc.diseaseHashMap[disease])
                    else:
                        multiplereview[row[0]] = set([jfc.diseaseHashMap[disease]])
print("Trials skipped with NDD in title, but not in Condition:", len(multiplereview)) #if we want to see skipped telemetry
#search for any trials with multiple NDD in title
for key in multiplereview:
    if len(multiplereview[key]) > 1:
        if len(multiplereview[key]) == 2 and 'MCI' in multiplereview[key] and 'AD' in multiplereview[key]:
            continue #Skip MCI/AD pair
        if len(multiplereview[key]) == 2 and 'MCI' in multiplereview[key] and 'PD' in multiplereview[key]:
            continue #Skip MCI/PD pair
        multiplereviewfinal.append([key, list(multiplereview[key])])
if len(multiplereviewfinal) > 0:
    reviewfinalmsg = "Trials skipped we may want to review:\n"
    for row in multiplereviewfinal:
        reviewfinalmsg += row[0]+": "+row[1][0]
        for i in range(1,len(row[1])):
            reviewfinalmsg += ", "+row[1][i]
        reviewfinalmsg += "\n"
    print(reviewfinalmsg) #If we want to see telemetry on any trials to review.

sorted_reviewskipped = sorted(reviewskipped, key=lambda row: row[1], reverse=False) #sort by nctid
#Write skipped trials to review
with open('output/nddreviewskipped.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(sorted_reviewskipped)

#print(matchentries)
diseasechecked = []
for entry in matchentries:
    if not (entry[2] in diseasechecked):
        diseasechecked.append(entry[2])
diseasechecked.sort()
#Write all Disease Name Variations we matched to our NDD for verification purposes
jfc.writeListToFileSorted(diseasechecked, "output/", "ListofDiseaseNameMatched")

#next we sort the resulting list by NCTID
sorted_matchentries = sorted(matchentries, key=lambda row: row[0], reverse=False) #sort by nctid

#lets write to csv all matches for trials on these diseases to pass to the next file.
#This script should only have to run once too.
with open('output/nddtrials.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(sorted_matchentries)
    #outfile.writerows(matchentries)

#now let's add all of the outcome rows that match trials we care about that are in nddtrials.csv (since rest we don't care)

matchnctid = {"NCT00000000"} #to speed up search let's make a set with all NCTIDs we care about
for row in matchentries:
    if row[0] not in matchnctid:
        matchnctid.add(row[0])

with open("queries/chartsv4B.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        if row[0] in matchnctid: #compare NCTID of matchentry with the row in chartsv4B if match then this is from a trial we care about
                nddoutcomes.append(row) #if we found a match in nddtrials we insert and move on to next row in chartsv4B

#next we sort the resulting list by NCTID
sorted_nddoutcomes = sorted(nddoutcomes, key=lambda row: row[0], reverse=False) #sort by nctid

with open('output/nddoutcomes.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(sorted_nddoutcomes)

#let's do the same with design_outcomes (chartsv4C)
with open("queries/chartsv4C.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        if row[0] in matchnctid: #compare NCTID of matchentry with the row in chartsv4B if match then this is from a trial we care about
                ndddesignoutcomes.append(row) #if we found a match in nddtrials we insert and move on to next row in chartsv4B

#next we sort the resulting list by NCTID
sorted_ndddesignoutcomes = sorted(ndddesignoutcomes, key=lambda row: row[0], reverse=False) #sort by nctid

with open('output/ndddesignoutcomes.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(sorted_ndddesignoutcomes)

#Next let's load the eligbility criteria for trials (chartsv4D)
with open("queries/chartsv4D.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data: #row[0] is nctid, row[1] is eligibility criteria text (big text)
        if row[0] in ignoretrials:
            continue #skip trials we are ignoring because they are out of search parameters (time range)
        toappend = False #becomes true when we find something we want to save
        #we need to only look in inclusion criteria so let's remove all text after the phrase
        #"Exclusion Criteria:" appears in our string.
        row1clean = row[1].lower()
        if "inclusion/exclusion" not in row1clean:
            row1clean = row1clean.split('exclusion criteria',1)[0]
        condlist = [] #store conditions we find here
        #Check each disease in disease section
        for disease in jfc.diseaseLongChecked: #check standard names
            if disease in row1clean: #if the text of a disease shows up
                condlist.append(disease)
                toappend = True
                #break #Don't break so we can find more matches
        #Check lowercase exceptions and some acronyms
        if (toappend == False):
            for disease in jfc.diseaselowercase:
                if disease in row1clean.lower():
                    condlist.append(disease)
                    toappend = True
        #Store the row if we flagged it as worthwhile
        if toappend:
            #Cleanup conditionlist.
            clean_condlist = []
            for c in condlist:
                clean_condlist.append(jfc.diseaseHashMap[c])
            nddeligibilities.append([row[0], len(condlist), ';'.join(clean_condlist) ,row[1] ])

#sort the results by NCTID
sorted_nddeligibilities = sorted(nddeligibilities, key=lambda row: row[0], reverse=False) #sort by nctid

#Generate list of trials with 1  condition or with more than 1 condition listed
nddeligibilities_multicond = []
nddeligibilities_singlecond = []
for row in sorted_nddeligibilities: 
    if row[1] > 1:
        if row[1] == 2 and "AD" in row[2] and "MCI" in row[2]:
                continue #2 conditions, skip if it is MCI/AD pair since we don't want it
        if row[1] == 2 and "PD" in row[2] and "MCI" in row[2]:
                continue #2 conditions, skip if it is MCI/PD pair since we don't want it    
        nddeligibilities_multicond.append(row)
    else:
        nddeligibilities_singlecond.append(row)

#write trials with eligibilities to review
with open('output/eligibility-criteria/nddeligcritall.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(sorted_nddeligibilities)
with open('output/eligibility-criteria/nddeligcritsinglecond.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(nddeligibilities_singlecond)
with open('output/eligibility-criteria/nddeligcritmulticond.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(nddeligibilities_multicond)

#Write All Trial Data for trials with eligibilities to review
ecNCTIDset = set() #Set to store all the NCTIDs we want
for entry in sorted_nddeligibilities:
    ecNCTIDset.add(entry[0]) #Adds all NCTIDs we want and removes duplicates :D
writeECTrialsfromNCTIDset(ecNCTIDset) #Run code to write all trial data to files.

#Create files that stores list of all NCTIDs it can be useful later.
#Do one of the matched NCTIDs (not eligibilty)
with open('output/matchnctidlist.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    data = sorted(matchnctid)
    for entry in data:
        outfile.writerow([entry]) #[] Fix to avoid it splitting a single string...
#Do one for the new trials found in eligibility criteria searches
ecNCTIDset = ecNCTIDset - matchnctid #Remove ones we already had in our normal search. 
#Comment out line above to capture a comprehensive list of elig crit flagged trials.
with open('output/ecnctidlist.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    data = sorted(ecNCTIDset)
    for entry in data:
        outfile.writerow([entry])

#Next do the demographics. It's very close to code from design_outcomes but it's separate to keep this short.
from baselineprocesser import baselinemeasurenddfilter
baselinemeasurenddfilter(matchnctid)


#Countries chartsv4F. Keeps only NDD related NCTIDs, writes to file for further processing.
nddcountries = [] #countries.nct_id, countries.name, countries.removed
with open("queries/chartsv4F.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        if row[1] in allNCTIDs: #compare NCTID of allNCTIDs with the row in chartsv4F if match then this is from a trial we care about (NDD)
            nddcountries.append(row) #if we found a match in nddtrials we insert and move on to next row in chartsv4F
#next we sort the resulting list by NCTID
sorted_nddcountries = sorted(nddcountries, key=lambda row: row[0], reverse=False) #sort by nctid, stable sort (ROW 0 is NCTID IN THIS CASE!)
#Save to file for further processing
with open('output/nddcountries.csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(sorted_nddcountries)

#Sponsors chartsV4G. Keeps only NDD related NCTIDs, writes to file for further processing.
nddsponsors = [] #sponsors.nct_id, sponsors.agency_class, sponsors.lead_or_collaborator, sponsors.name
with open("queries/chartsv4F.csv") as csv_file:
    csv_data = csv.reader(csv_file, delimiter=',')
    for row in csv_data:
        if row[1] in allNCTIDs: #compare NCTID of allNCTIDs with the row in chartsv4F if match then this is from a trial we care about (NDD)
            nddsponsors .append(row) #if we found a match in nddtrials we insert and move on to next row in chartsv4F
#next we sort the resulting list by NCTID
sorted_nddsponsors  = sorted(nddsponsors , key=lambda row: row[0], reverse=False) #sort by nctid, stable sort (ROW 0 is NCTID IN THIS CASE!)
#Save to file for further processing
with open('output/nddsponsors .csv', 'w', newline='') as csv_outfile:
    outfile = csv.writer(csv_outfile)
    outfile.writerows(sorted_nddsponsors )

#END CODE