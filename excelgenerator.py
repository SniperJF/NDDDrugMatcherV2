#This File is for the functions that write out the final excel spreadsheet with pretty formatting
import xlsxwriter #Installed using pip install XlsxWriter. See: https://xlsxwriter.readthedocs.io/
#import openpyxl #For generating pretty charts since XlsxWriter does not do 3D charts. #Installed using pip install openpyxl (Unused for now)
import time #For versioning our file
def generateExcelDemographics(demogHeadings, demogTable):
    #First Let's split data into tables we want: T0: US-ONLY Drug, T1: NON-US Drug, T2: GLOBAL Drug, T3: NONE Drug, 
    #T4: Biomarker, Device, Other (in that order), T5 all Drug trials and T6: Master Data (Original version of Data as it is in demogTable)
    finalTables = DemogTableSplitter(demogTable)

    #Next let's update the top headings and generate individual headings for each table
    individualTableHeadings, footerTotals = demographicHeadingUpdater(demogHeadings, finalTables)

    #workbook = xlsxwriter.Workbook('output/ADMCIdemographicsV'+str(int(time.time())) +'.xlsx') #Versioned 
    workbook = xlsxwriter.Workbook('output/ADMCIdemographics.xlsx') #Same name each run
    worksheet = workbook.add_worksheet()

    #Set Column Widths
    worksheet.set_column(0, 0, 13) #NCTID
    worksheet.set_column(1, 1, 15) #NCTID Hyperlink
    worksheet.set_column(19, 20, 11) #First and Last Posted Dates
    worksheet.set_column(24, 24, 9)  #Trial Type
    worksheet.set_column(25, 25, 35) #Title and Intervention
    worksheet.set_column(26, 26, 90) #Intervention

    merge_format = workbook.add_format({'bold': True, 'bg_color': '#F3857D', 'border': 1, 'font_size': 28,
                                            'align': 'center', 'valign': 'vcenter'}) #Set title format
    worksheet.merge_range(0,0, 0, 26, 'AD/MCI Demographics Table', merge_format) #Prints Cool Title

    rowCounter = 2 #Starts at 2 since we already printed the title at row 0 and left empty space at row 1
    for row in demogHeadings[:-3]:
        if rowCounter < 13:
            cell_format = workbook.add_format({'bold': True})
            worksheet.write(rowCounter, 0, row[0], cell_format)
            worksheet.write(rowCounter, 1, row[1])
        elif rowCounter == 15 or rowCounter == 20 or rowCounter == 25: #Hardcoded :o
            cell_format = workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#E9FF97'})
            worksheet.write_row(rowCounter, 0, row, cell_format) #Write Headings
        else:
            worksheet.write_row(rowCounter, 0, row) #Write Headings
        rowCounter +=1

    rowCounter +=3
    i = 0
    for table in finalTables:
        merge_format = workbook.add_format({'bold': True, 'bg_color': '#B8B8B8', 'border': 1, 'font_size': 22,
                                            'align': 'center', 'valign': 'vcenter'}) #Set header formatting
        if i!=6: worksheet.merge_range(rowCounter,0, rowCounter, 26, demogHeadings[i+2][1], merge_format)
        else: worksheet.merge_range(rowCounter,0, rowCounter, 26, demogHeadings[1][1], merge_format)
        rowCounter +=1       
        for row in individualTableHeadings[i]:
            cell_format = workbook.add_format({'bold': True, 'bg_color': '#96DADA', 'border': 1}) #Set header formatting
            worksheet.write_row(rowCounter, 0, row, cell_format) #Write Headings
            rowCounter +=1
        #For ease of generating graphs we are going to also add totals before data (so they appear twice)
        cell_format = workbook.add_format({'bold': True, 'bg_color': '#F1B07F', 'border': 1,}) #Set Totals formatting        
        worksheet.write_row(rowCounter, 0, footerTotals[i], cell_format) #Write Totals
        rowCounter +=1
        for row in table:
            cell_format = workbook.add_format({'border': 1})
            worksheet.write_row(rowCounter, 0, row, cell_format) #Write Table
            rowCounter +=1
        cell_format = workbook.add_format({'bold': True, 'bg_color': '#F1B07F', 'border': 1,}) #Set footer formatting        
        worksheet.write_row(rowCounter, 0, footerTotals[i], cell_format) #Write Footer Totals
        rowCounter +=4 #For footer and 3 empty rows to separate tables
        i +=1
    print("\n"+str(rowCounter)+" Rows Printed in Excel.\n")
    workbook.close()
#End Function

#Function Split Tables as follows:
#T0: US-ONLY Drug
#T1: NON-US Drug
#T2: GLOBAL Drug
#T3: NONE Drug
#T4: Biomarker, Device, Other (in that order)
#T5: All Drug Trials
#T6: Master Data (Original version of Data as it is in demogTable)
def DemogTableSplitter(demogTable): #row[22] Country Type, #row[24] #Trial Type
    finalTables = [ [],[],[],[],[],[],[] ] #T0-T6
    for row in demogTable:
        if row[24] == 'Drug':
            if row[22] == 'US-ONLY':
                finalTables[0].append(row)
            elif row[22] == 'NON-US':
                finalTables[1].append(row)
            elif row[22] == 'GLOBAL':
                finalTables[2].append(row)
            elif row[22] == 'NONE' or row[22] == "": #No country available
                finalTables[3].append(row)                
            else:
                print("Warning: Excel File Did Not Write Row Due to bad Class: ", row[0], row[23])
            finalTables[5].append(row) #All Drug Trials (useful to make graphics for all drug trials)
        else: #T4
            finalTables[4].append(row)
    finalTables[4].sort(key=lambda row: (row[24], row[0]), reverse=False) #Stable Sort T4
    finalTables[6] = demogTable #T5 is same as start so just throw a ref to it
    return finalTables
#End Function

#Updates demogHeadings and also creates individual headings to go on our final tables (label and totals)
def demographicHeadingUpdater(demogHeadings, finalTables):
    #First let's add new totals at the top. That is insert after row[3]
    demogHeadings.insert(4, [len(finalTables[0]),"Total AD/MCI Drug Trials with Results in US-ONLY"])
    demogHeadings.insert(5, [len(finalTables[1]),"Total AD/MCI Drug Trials with Results in NON-US"])
    demogHeadings.insert(6, [len(finalTables[2]),"Total AD/MCI Drug Trials with Results in GLOBAL"])
    demogHeadings.insert(7, [len(finalTables[3]),"Total AD/MCI Drug Trials with Results with No Country Data"])
    demogHeadings.insert(8, [len(finalTables[4]),"Total AD/MCI Non-Drug Trials with Results"])
    demogHeadings.insert(9, [len(finalTables[5]),"Total AD/MCI All Drug Trials with Results"])
    biomarkerCount = 0
    deviceCount = 0
    otherCount = 0
    for i in finalTables[4]:
        if   i[24] == "Biomarker": biomarkerCount += 1
        elif i[24] == "Device": deviceCount += 1
        else: otherCount += 1
    demogHeadings.insert(10, [biomarkerCount,"Total AD/MCI Biomarker Trials with Results"])
    demogHeadings.insert(11, [deviceCount,"Total AD/MCI Device Trials with Results"])
    demogHeadings.insert(12, [otherCount,"Total AD/MCI Others Trials with Results"])
    #Next let's add each table's individual headings
    individualTableHeadings = []
    for i in range(len(finalTables)): #Final Table Headings is already done
        individualTableHeadings.append([demogHeadings[-3], demogHeadings[-2]])
    #Lastly let's add the footer with the totals at the bottom
    footerTotals = []
    for table in finalTables:
        footerRow = ['Totals for '+str(len(table))+' trials:','','']
        for col in range(3,19): #Only the rows with numerical values we want to sum totals for
            colsum = 0
            for row in table:
                if row[col] != "":
                    try:
                        colsum += row[col]
                    except:
                        print("Warning: Invalid Value when summing total:",type(val),val)
                        exit()
            footerRow.append(colsum)
        footerTotals.append(footerRow)
    #One last thing lets combine row 0,1 and 2,3 to match format
    demogHeadings[0] = [demogHeadings[1][0], demogHeadings[0][0]]
    demogHeadings[2] = [demogHeadings[3][0], demogHeadings[2][0]]
    demogHeadings.pop(3)
    demogHeadings.pop(1)
    return individualTableHeadings, footerTotals
#End File