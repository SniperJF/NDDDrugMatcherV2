#This File is for the functions that write out the final excel spreadsheet with pretty formatting
import xlsxwriter #Installed using pip install XlsxWriter. See: https://xlsxwriter.readthedocs.io/
import time #For versioning our file
def generateExcelDemographics(demogHeadings, demogTable):
    workbook = xlsxwriter.Workbook('output/ADMCIdemographicsV'+str(int(time.time())) +'.xlsx')
    worksheet = workbook.add_worksheet()
    workbook.close()
#End Function