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
    with open('output/nddsponsors .csv', 'w', newline='') as csv_outfile:
        outfile = csv.writer(csv_outfile)
        outfile.writerows(sorted_nddsponsors)
#End Function

def countryprocessor(matchedCTO):
    pass

def sponsorprocessor(matchedCTO):
    pass
#End File