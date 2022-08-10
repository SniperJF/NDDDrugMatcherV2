#For Additional Processing of fields that we add as time goes on, for now it is Country and Sponsors, but more can be added
#later on as we need them
import csv

#For importing countries data from chartsv4F. Keeps only NDD related NCTIDs, writes to file for further processing.
def countrynddfilter(matchnctid):
    nddcountries = [] #countries.nct_id, countries.name, countries.removed
    with open("queries/chartsv4F.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            if row[0] in matchnctid: #compare NCTID of matchnctid with the row in chartsv4F if match then this is from a trial we care about (NDD)
                nddcountries.append(row) #if we found a match in nddtrials we insert and move on to next row in chartsv4F
    #next we sort the resulting list by NCTID
    sorted_nddcountries = sorted(nddcountries, key=lambda row: row[0], reverse=False) #sort by nctid, stable sort (ROW 0 is NCTID IN THIS CASE!)
    #Save to file for further processing
    with open('output/nddcountries.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(sorted_nddcountries)
#End Function

#For importing Sponsors data from chartsV4G. Keeps only NDD related NCTIDs, writes to file for further processing.
def sponsornddfilter(matchnctid):
    nddsponsors = [] #sponsors.nct_id, sponsors.agency_class, sponsors.lead_or_collaborator, sponsors.name
    with open("queries/chartsv4G.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            if row[0] in matchnctid: #compare NCTID of matchnctid with the row in chartsv4F if match then this is from a trial we care about (NDD)
                nddsponsors .append(row) #if we found a match in nddtrials we insert and move on to next row in chartsv4F
    #next we sort the resulting list by NCTID
    sorted_nddsponsors  = sorted(nddsponsors , key=lambda row: row[0], reverse=False) #sort by nctid, stable sort (ROW 0 is NCTID IN THIS CASE!)
    #Save to file for further processing
    with open('output/nddsponsors.csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(sorted_nddsponsors)
#End Function

#Function to insert Country data as a list that is in the CTO
def countryprocessor(matchedCTO): #NCTID, Country Name, t/f representing if country has been removed (true if removed)
    #First load the data from the file
    nddcountries = []  #chartsv4F baseline measurements
    with open("output/nddcountries.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            nddcountries.append(row)
    #Now I will try to insert each row into the appropriate trial. I'm just going to insert them as lists inside of lists.
    #So by end it will look like this countries = [ ['USA', True], ['UK', False] ].
    for row in nddcountries:
        matchedCTO[row[0]].countries.append([ row[1], True if row[2]=='t' else False ])
    #Next let's do countryType. This field contains a string indiciating whether the trials are
    #US-ONLY, NON-US, GLOBAL (US and at least 1 Non-US country), or NONE (no country listed). Useful for splitting table into these groups
    for nctid in matchedCTO:
        if len(matchedCTO[nctid].countries) > 0: #We have something to look at 
            hasUS = False
            hasNonUS = False
            for entry in matchedCTO[nctid].countries: #Check each country
                if not entry[1]: #if country removed is set to false add it , else skip if it is true
                    if entry[0] == "United States": hasUS = True
                    else: hasNonUS = True
                if hasUS and hasNonUS: break #Once we got both no need to keep going, optimization.
            #Now to add the correct tag based on our flags:
            if hasUS and hasNonUS: matchedCTO[nctid].countryType = "GLOBAL"
            elif hasUS and not hasNonUS: matchedCTO[nctid].countryType = "US-ONLY"
            elif hasNonUS and not hasUS: matchedCTO[nctid].countryType = "NON-US"
            else: matchedCTO[nctid].countryType = "NONE"
#End Function

#Function to insert Country data as a list that is in the CTO
def sponsorprocessor(matchedCTO): #NCTID, Agency Class (NIH/Industry etc), Sponsor lead or collaborator status, Sponsors Name
    #First load the data from the file
    nddsponsors = []  #chartsv4F baseline measurements
    with open("output/nddsponsors.csv") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        for row in csv_data:
            nddsponsors.append(row)
    #Now I will try to insert each row into the appropriate trial. I'm just going to insert them as lists inside of lists.
    #So by end it will look like this:
    #sponsors = [ ['NIH', 'lead', 'National center for blah'], ['NIH', 'collaborator', 'National institute of blah'] ].
    for row in nddsponsors:
        matchedCTO[row[0]].sponsors.append([row[1], row[2], row[3]])
#End Function

#End File