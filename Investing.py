#!/usr/bin/env python
#-------------------------------------------------------------------------------
import sys, os, datetime, time, getpass, glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
#-------------------------------------------------------------------------------
# NOTES: Here, keep a copy of your email and password for Investing.com.
# Email:
# Password:
#-------------------------------------------------------------------------------
# GLOBAL VARIABLES:
sleeptime = 2
# Email for Investing.com
userEmail = raw_input("Email: ")
# Password for Investing.com
password = getpass.getpass("Password: ")
# Operating mode from the list below
OperatingMode = raw_input("Mode: ")
# Time interval of data collection -- 10 years is typical to observe trends
interval = raw_input("Interval: ")
# Copy the path of the destination folder
DownloadPath = raw_input("Paste the file path to the destination folder: ")
# As an example, mine was 'C:\Users\Frankie\Desktop\Investing.com'
# You can hardcode Email, Password, Interval, and Download Path
# to speed up the program.
#-------------------------------------------------------------------------------
# Main() function:
#-------------------------------------------------------------------------------
# This function calls DownloadData, login, GetURLMap, GetHistoricalData,
# RenameLatestFile, then GetFiles, in a linked sequential chain.
# At GetURLMap, we've built 72 modes for the program, to be called with "Mode."
#-------------------------------------------------------------------------------
def main():
    DownloadData()
    return True
#-------------------------------------------------------------------------------
# DownloadData: Step 1
#-------------------------------------------------------------------------------
def DownloadData(TimeInterval=None):
    #Login
    browser = login(DownloadPath)
    
    #Interval default set to 10
    if TimeInterval is None:
        interval = int(10)
    else: #DownloadPath passed in
        interval = TimeInterval
        
    #Set Start/End Date Range
    # Datetime object representing today.
    t = datetime.datetime.today()
    #Year-formatted interval in the past from which to begin data collection.
    interval = int(interval)
    #This converts the year-formatted time difference to days precisely.
    interval = datetime.timedelta(days=(365.2425*interval))
    y = (t-interval)
    #Start date as a mm/dd/yyyy formatted string.
    y = (y.strftime("%m/%d/%Y"))
    #End date as a mm/dd/yyyy formatted string.
    t = (t.strftime("%m/%d/%Y"))
    startDate = y
    endDate = t

    #Get List of URLs to Process
    urlMap = GetURLMap()
    #Cycle through Each URL in urlMap
    for key in urlMap.keys():
        #Notify User
        print("Downloading: " + str(key))
        print("URL: " + urlMap[key])
        #Grab Historical Data from URL
        GetHistoricalData(browser, urlMap[key], startDate, endDate)
        #Rename File to key
        RenameLatestFile(DownloadPath, key + '.csv')
        #Print Blank Line for Readability
        print('')
    #Browser Cleanup
    browser.quit()
    return True
#-------------------------------------------------------------------------------
# login: Step 2: downloadPath comes from DownloadData
#-------------------------------------------------------------------------------
def login(downloadPath):
    #Get login info

    #Instantiate Chrome Options to Set Download Path
    chromeOptions = webdriver.ChromeOptions()
    #Set downloadDirectory
    downloadDirectory = downloadPath
    #Set default directory preference
    prefs = {"download.default_directory" : downloadDirectory}
    #Add prefference to ChromeOptions
    chromeOptions.add_experimental_option("prefs", prefs)

    #Instantiate Browser Object passing in ChromeOptions
    browser = webdriver.Chrome(chrome_options = chromeOptions)
    #Navigate to URL
    browser.get('http://www.investing.com')
    #Get Sign In Element
    signIn = browser.find_element_by_css_selector('#userAccount > .topBarText > .login ')
    #Click Sign In element
    signIn.click()
    #Wait sleeptime seconds for popup to show
    time.sleep(sleeptime)

    #Get Email Element
    emailElement = browser.find_element_by_id('loginFormUser_email')
    #Clear Email Form
    emailElement.clear()
    #Enter in Email
    emailElement.send_keys(userEmail)
    #wait sleeptime seconds for text to enter
    time.sleep(sleeptime)

    #Get Password Element
    pwdElement = browser.find_element_by_id('loginForm_password')
    #Clear Password Form
    pwdElement.clear()
    #Enter in password
    pwdElement.send_keys(password)

    #Get Sign In Button
    signInBTN = browser.find_element_by_css_selector('#loginPopup > #signup > a')
    #Sign In
    signInBTN.click()

    #Fix the orange button problem
    browser.get('https://www.investing.com/indices/us-spx-500-historical-data')
    #Get orange button
    OrangeButton = browser.find_element_by_css_selector('body > div.wrapper > div.userDataPopup.js-userDataPopup > div.js-userDataPopup-questions > div.buttons > a:nth-child(2)')
    #Wait sleeptime seconds for popup to show
    time.sleep(sleeptime)
    #Click orange button
    OrangeButton.click()

    return browser
#-------------------------------------------------------------------------------
# GetURLMap: Step 3: Returns dictionary where Key is filename and value is URL
#-------------------------------------------------------------------------------
if OperatingMode == "Bonds":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ARG1Y'] = "https://www.investing.com/rates-bonds/argentina-1-year-historical-data"

        outputDict['AUS1Y'] = "https://www.investing.com/rates-bonds/australia-1-year-bond-yield-historical-data"
        outputDict['AUS5Y'] = "https://www.investing.com/rates-bonds/australia-5-year-bond-yield-historical-data"
        outputDict['AUS10Y'] = "https://www.investing.com/rates-bonds/australia-10-year-bond-yield-historical-data"

        outputDict['AUT1Y'] = "https://www.investing.com/rates-bonds/austria-1-year-bond-yield-historical-data"
        outputDict['AUT5Y'] = "https://www.investing.com/rates-bonds/austria-5-year-bond-yield-historical-data"
        outputDict['AUT10Y'] = "https://www.investing.com/rates-bonds/austria-10-year-bond-yield-historical-data"

        outputDict['BEL1Y'] = "https://www.investing.com/rates-bonds/belguim-1-year-bond-yield-historical-data"
        outputDict['BEL5Y'] = "https://www.investing.com/rates-bonds/belguim-5-year-bond-yield-historical-data"
        outputDict['BEL10Y'] = "https://www.investing.com/rates-bonds/belguim-10-year-bond-yield-historical-data"

        outputDict['BGD1Y'] = "https://www.investing.com/rates-bonds/bangladesh-1-year-historical-data"
        outputDict['BGD5Y'] = "https://www.investing.com/rates-bonds/bangladesh-5-year-historical-data"
        outputDict['BGD10Y'] = "https://www.investing.com/rates-bonds/bangladesh-10-year-historical-data"

        outputDict['BGR1Y'] = "https://www.investing.com/rates-bonds/bulgaria-1-year-bond-yield-historical-data"
        outputDict['BGR5Y'] = "https://www.investing.com/rates-bonds/bulgaria-5-year-bond-yield-historical-data"
        outputDict['BGR10Y'] = "https://www.investing.com/rates-bonds/bulgaria-10-year-bond-yield-historical-data"

        outputDict['BHR1Y'] = "https://www.investing.com/rates-bonds/bahrain-1-year-historical-data"
        outputDict['BHR5Y'] = "https://www.investing.com/rates-bonds/bahrain-5-year-historical-data"

        outputDict['BRA1Y'] = "https://www.investing.com/rates-bonds/brazil-1-year-bond-yield-historical-data"
        outputDict['BRA5Y'] = "https://www.investing.com/rates-bonds/brazil-5-year-bond-yield-historical-data"
        outputDict['BRA10Y'] = "https://www.investing.com/rates-bonds/brazil-10-year-bond-yield-historical-data"

        outputDict['BWA5Y'] = "https://www.investing.com/rates-bonds/botswana-5-years-historical-data"

        outputDict['CAN1Y'] = "https://www.investing.com/rates-bonds/canada-1-year-bond-yield-historical-data"
        outputDict['CAN5Y'] = "https://www.investing.com/rates-bonds/canada-5-year-bond-yield-historical-data"
        outputDict['CAN10Y'] = "https://www.investing.com/rates-bonds/canada-10-year-bond-yield-historical-data"

        outputDict['CHE1Y'] = "https://www.investing.com/rates-bonds/switzerland-1-year-bond-yield-historical-data"
        outputDict['CHE5Y'] = "https://www.investing.com/rates-bonds/switzerland-5-year-bond-yield-historical-data"
        outputDict['CHE10Y'] = "https://www.investing.com/rates-bonds/switzerland-10-year-bond-yield-historical-data"

        outputDict['CHL1Y'] = "https://www.investing.com/rates-bonds/chile-1-year-bond-yield-historical-data"
        outputDict['CHL5Y'] = "https://www.investing.com/rates-bonds/chile-5-year-bond-yield-historical-data"
        outputDict['CHL10Y'] = "https://www.investing.com/rates-bonds/chile-10-year-bond-yield-historical-data"

        outputDict['CHN1Y'] = "https://www.investing.com/rates-bonds/china-1-year-bond-yield-historical-data"
        outputDict['CHN5Y'] = "https://www.investing.com/rates-bonds/china-5-year-bond-yield-historical-data"
        outputDict['CHN10Y'] = "https://www.investing.com/rates-bonds/china-10-year-bond-yield-historical-data"

        outputDict['COL1Y'] = "https://www.investing.com/rates-bonds/colombia-2-year-bond-yield-historical-data"
        outputDict['COL5Y'] = "https://www.investing.com/rates-bonds/colombia-5-year-bond-yield-historical-data"
        outputDict['COL10Y'] = "https://www.investing.com/rates-bonds/colombia-10-year-bond-yield-historical-data"

        outputDict['CZE1Y'] = "https://www.investing.com/rates-bonds/czech-republic-1-year-bond-yield-historical-data"
        outputDict['CZE5Y'] = "https://www.investing.com/rates-bonds/czech-republic-5-year-bond-yield-historical-data"
        outputDict['CZE10Y'] = "https://www.investing.com/rates-bonds/czech-republic-10-year-bond-yield-historical-data"

        outputDict['DEU1Y'] = "https://www.investing.com/rates-bonds/germany-1-year-bond-yield-historical-data"
        outputDict['DEU5Y'] = "https://www.investing.com/rates-bonds/germany-5-year-bond-yield-historical-data"
        outputDict['DEU10Y'] = "https://www.investing.com/rates-bonds/germany-10-year-bond-yield-historical-data"

        outputDict['DNK5Y'] = "https://www.investing.com/rates-bonds/denmark-5-year-bond-yield-historical-data"
        outputDict['DNK10Y'] = "https://www.investing.com/rates-bonds/denmark-10-year-bond-yield-historical-data"

        outputDict['EGY1Y'] = "https://www.investing.com/rates-bonds/egypt-1-year-bond-yield-historical-data"
        outputDict['EGY5Y'] = "https://www.investing.com/rates-bonds/egypt-5-year-bond-yield-historical-data"
        outputDict['EGY10Y'] = "https://www.investing.com/rates-bonds/egypt-10-year-bond-yield-historical-data"

        outputDict['ESP1Y'] = "https://www.investing.com/rates-bonds/spain-1-year-bond-yield-historical-data"
        outputDict['ESP5Y'] = "https://www.investing.com/rates-bonds/spain-5-year-bond-yield-historical-data"
        outputDict['ESP10Y'] = "https://www.investing.com/rates-bonds/spain-10-year-bond-yield-historical-data"

        outputDict['FIN5Y'] = "https://www.investing.com/rates-bonds/finland-5-year-bond-yield-historical-data"
        outputDict['FIN10Y'] = "https://www.investing.com/rates-bonds/finland-10-year-bond-yield-historical-data"

        outputDict['FRA1Y'] = "https://www.investing.com/rates-bonds/france-1-year-bond-yield-historical-data"
        outputDict['FRA5Y'] = "https://www.investing.com/rates-bonds/france-5-year-bond-yield-historical-data"
        outputDict['FRA10Y'] = "https://www.investing.com/rates-bonds/france-10-year-bond-yield-historical-data"

        outputDict['GBR1Y'] = "https://www.investing.com/rates-bonds/uk-1-year-bond-yield-historical-data"
        outputDict['GBR5Y'] = "https://www.investing.com/rates-bonds/uk-5-year-bond-yield-historical-data"
        outputDict['GBR10Y'] = "https://www.investing.com/rates-bonds/uk-10-year-bond-yield-historical-data"

        outputDict['GRC5Y'] = "https://www.investing.com/rates-bonds/greece-5-year-bond-yield-historical-data"
        outputDict['GRC10Y'] = "https://www.investing.com/rates-bonds/greece-10-year-bond-yield-historical-data"

        outputDict['HKG1Y'] = "https://www.investing.com/rates-bonds/hong-kong-1-year-bond-yield-historical-data"
        outputDict['HKG5Y'] = "https://www.investing.com/rates-bonds/hong-kong-5-year-bond-yield-historical-data"
        outputDict['HKG10Y'] = "https://www.investing.com/rates-bonds/hong-kong-10-year-bond-yield-historical-data"

        outputDict['HRV1Y'] = "https://www.investing.com/rates-bonds/croatia-1-year-bond-yield-historical-data"
        outputDict['HRV5Y'] = "https://www.investing.com/rates-bonds/croatia-5-year-bond-yield-historical-data"
        outputDict['HRV10Y'] = "https://www.investing.com/rates-bonds/croatia-10-year-bond-yield-historical-data"

        outputDict['HUN1Y'] = "https://www.investing.com/rates-bonds/hungary-1-year-bond-yield-historical-data"
        outputDict['HUN5Y'] = "https://www.investing.com/rates-bonds/hungary-5-year-bond-yield-historical-data"
        outputDict['HUN10Y'] = "https://www.investing.com/rates-bonds/hungary-10-year-bond-yield-historical-data"

        outputDict['IDN1Y'] = "https://www.investing.com/rates-bonds/indonesia-1-year-bond-yield-historical-data"
        outputDict['IDN5Y'] = "https://www.investing.com/rates-bonds/indonesia-5-year-bond-yield-historical-data"
        outputDict['IDN10Y'] = "https://www.investing.com/rates-bonds/indonesia-10-year-bond-yield-historical-data"

        outputDict['IND1Y'] = "https://www.investing.com/rates-bonds/india-1-year-bond-yield-historical-data"
        outputDict['IND5Y'] = "https://www.investing.com/rates-bonds/india-5-year-bond-yield-historical-data"
        outputDict['IND10Y'] = "https://www.investing.com/rates-bonds/india-10-year-bond-yield-historical-data"

        outputDict['IRL1Y'] = "https://www.investing.com/rates-bonds/ireland-1-year-bond-yield-historical-data"
        outputDict['IRL5Y'] = "https://www.investing.com/rates-bonds/ireland-5-year-bond-yield-historical-data"
        outputDict['IRL10Y'] = "https://www.investing.com/rates-bonds/ireland-10-year-bond-yield-historical-data"

        outputDict['ISL5Y'] = "https://www.investing.com/rates-bonds/iceland-5-year-bond-yield-historical-data"
        outputDict['ISL10Y'] = "https://www.investing.com/rates-bonds/iceland-10-year-bond-yield-historical-data"

        outputDict['ISR1Y'] = "https://www.investing.com/rates-bonds/israel-1-year-bond-yield-historical-data"
        outputDict['ISR5Y'] = "https://www.investing.com/rates-bonds/israel-5-year-bond-yield-historical-data"
        outputDict['ISR10Y'] = "https://www.investing.com/rates-bonds/israel-10-year-bond-yield-historical-data"

        outputDict['ITA1Y'] = "https://www.investing.com/rates-bonds/italy-1-year-bond-yield-historical-data"
        outputDict['ITA5Y'] = "https://www.investing.com/rates-bonds/italy-5-year-bond-yield-historical-data"
        outputDict['ITA10Y'] = "https://www.investing.com/rates-bonds/italy-10-year-bond-yield-historical-data"

        outputDict['JOR1Y'] = "https://www.investing.com/rates-bonds/jordan-1-year-historical-data"
        outputDict['JOR5Y'] = "https://www.investing.com/rates-bonds/jordan-5-year-historical-data"
        outputDict['JOR10Y'] = "https://www.investing.com/rates-bonds/jordan-10-year-historical-data"

        outputDict['JPN1Y'] = "https://www.investing.com/rates-bonds/japan-1-year-bond-yield-historical-data"
        outputDict['JPN5Y'] = "https://www.investing.com/rates-bonds/japan-5-year-bond-yield-historical-data"
        outputDict['JPN10Y'] = "https://www.investing.com/rates-bonds/japan-10-year-bond-yield-historical-data"

        outputDict['KEN1Y'] = "https://www.investing.com/rates-bonds/kenya-1-year-bond-yield-historical-data"
        outputDict['KEN5Y'] = "https://www.investing.com/rates-bonds/kenya-5-year-bond-yield-historical-data"
        outputDict['KEN10Y'] = "https://www.investing.com/rates-bonds/kenya-10-year-bond-yield-historical-data"

        outputDict['KOR1Y'] = "https://www.investing.com/rates-bonds/south-korea-1-year-bond-yield-historical-data"
        outputDict['KOR5Y'] = "https://www.investing.com/rates-bonds/south-korea-5-year-bond-yield-historical-data"
        outputDict['KOR10Y'] = "https://www.investing.com/rates-bonds/south-korea-10-year-bond-yield-historical-data"

        outputDict['LKA1Y'] = "https://www.investing.com/rates-bonds/sri-lanka-1-year-bond-yield-historical-data"
        outputDict['LKA5Y'] = "https://www.investing.com/rates-bonds/sri-lanka-5-year-bond-yield-historical-data"
        outputDict['LKA10Y'] = "https://www.investing.com/rates-bonds/sri-lanka-10-year-historical-data"

        outputDict['LTU5Y'] = "https://www.investing.com/rates-bonds/lithuania-5-years-bond-yield-historical-data"
        outputDict['LTU10Y'] = "https://www.investing.com/rates-bonds/lithuania-10-years-bond-yield-historical-data"

        outputDict['LVA5Y'] = "https://www.investing.com/rates-bonds/latvia-5-years-bond-yield-historical-data"

        outputDict['MAR5Y'] = "https://www.investing.com/rates-bonds/morocco-5-year-historical-data"
        outputDict['MAR10Y'] = "https://www.investing.com/rates-bonds/morocco-10-year-historical-data"

        outputDict['MEX1Y'] = "https://www.investing.com/rates-bonds/mexico-1-year-historical-data"
        outputDict['MEX5Y'] = "https://www.investing.com/rates-bonds/mexico-5-year-historical-data"
        outputDict['MEX10Y'] = "https://www.investing.com/rates-bonds/mexico-10-year-historical-data"

        outputDict['MLT1Y'] = "https://www.investing.com/rates-bonds/malta-1-year-historical-data"
        outputDict['MLT5Y'] = "https://www.investing.com/rates-bonds/malta-5-year-historical-data"
        outputDict['MLT10Y'] = "https://www.investing.com/rates-bonds/malta-10-year-historical-data"

        outputDict['MUS1Y'] = "https://www.investing.com/rates-bonds/mauritius-1-year-bond-yield-historical-data"
        outputDict['MUS5Y'] = "https://www.investing.com/rates-bonds/mauritius-5-year-historical-data"
        outputDict['MUS10Y'] = "https://www.investing.com/rates-bonds/mauritius-10-year-historical-data"

        outputDict['MYS1Y'] = "https://www.investing.com/rates-bonds/malaysia-1-year-bond-yield-historical-data"
        outputDict['MYS5Y'] = "https://www.investing.com/rates-bonds/malaysia-5-year-bond-yield-historical-data"
        outputDict['MYS10Y'] = "https://www.investing.com/rates-bonds/malaysia-10-year-bond-yield-historical-data"

        outputDict['NAM1Y'] = "https://www.investing.com/rates-bonds/namibia-1-year-historical-data"
        outputDict['NAM10Y'] = "https://www.investing.com/rates-bonds/namibia-10-year-historical-data"

        outputDict['NGA1Y'] = "https://www.investing.com/rates-bonds/nigeria-1-year-historical-data"
        outputDict['NGA5Y'] = "https://www.investing.com/rates-bonds/nigeria-5-year-historical-data"
        outputDict['NGA10Y'] = "https://www.investing.com/rates-bonds/nigeria-10-year-historical-data"

        outputDict['NLD5Y'] = "https://www.investing.com/rates-bonds/netherlands-5-year-bond-yield-historical-data"
        outputDict['NLD10Y'] = "https://www.investing.com/rates-bonds/netherlands-10-year-bond-yield-historical-data"

        outputDict['NOR1Y'] = "https://www.investing.com/rates-bonds/norway-1-year-bond-yield-historical-data"
        outputDict['NOR5Y'] = "https://www.investing.com/rates-bonds/norway-5-year-bond-yield-historical-data"
        outputDict['NOR10Y'] = "https://www.investing.com/rates-bonds/norway-10-year-bond-yield-historical-data"

        outputDict['NZL1Y'] = "https://www.investing.com/rates-bonds/new-zealand-1-year-historical-data"
        outputDict['NZL5Y'] = "https://www.investing.com/rates-bonds/new-zealand-5-years-bond-yield-historical-data"
        outputDict['NZL10Y'] = "https://www.investing.com/rates-bonds/new-zealand-10-years-bond-yield-historical-data"

        outputDict['PAK1Y'] = "https://www.investing.com/rates-bonds/pakistan-1-year-bond-yield-historical-data"
        outputDict['PAK5Y'] = "https://www.investing.com/rates-bonds/pakistan-5-year-bond-yield-historical-data"
        outputDict['PAK10Y'] = "https://www.investing.com/rates-bonds/pakistan-10-year-bond-yield-historical-data"

        outputDict['PER5Y'] = "https://www.investing.com/rates-bonds/peru-5-year-bond-yield-historical-data"

        outputDict['PHL1Y'] = "https://www.investing.com/rates-bonds/philippines-1-year-bond-yield-historical-data"
        outputDict['PHL5Y'] = "https://www.investing.com/rates-bonds/philippines-5-year-bond-yield-historical-data"
        outputDict['PHL10Y'] = "https://www.investing.com/rates-bonds/philippines-10-year-bond-yield-historical-data"

        outputDict['POL1Y'] = "https://www.investing.com/rates-bonds/poland-1-year-bond-yield-historical-data"
        outputDict['POL5Y'] = "https://www.investing.com/rates-bonds/poland-5-year-bond-yield-historical-data"
        outputDict['POL10Y'] = "https://www.investing.com/rates-bonds/poland-10-year-bond-yield-historical-data"

        outputDict['PRT1Y'] = "https://www.investing.com/rates-bonds/portugal-1-year-historical-data"
        outputDict['PRT5Y'] = "https://www.investing.com/rates-bonds/portugal-5-year-bond-yield-historical-data"
        outputDict['PRT10Y'] = "https://www.investing.com/rates-bonds/portugal-10-year-bond-yield-historical-data"

        outputDict['QAT5Y'] = "https://www.investing.com/rates-bonds/qatar-5-year-bond-yield-historical-data"
        outputDict['QAT10Y'] = "https://www.investing.com/rates-bonds/qatar-10-year-bond-yield-historical-data"

        outputDict['ROU1Y'] = "https://www.investing.com/rates-bonds/romania-1-year-bond-yield-historical-data"
        outputDict['ROU5Y'] = "https://www.investing.com/rates-bonds/romania-5-year-bond-yield-historical-data"
        outputDict['ROU10Y'] = "https://www.investing.com/rates-bonds/romania-10-year-bond-yield-historical-data"

        outputDict['RUS1Y'] = "https://www.investing.com/rates-bonds/russia-1-year-bond-yield-historical-data"
        outputDict['RUS5Y'] = "https://www.investing.com/rates-bonds/russia-5-year-bond-yield-historical-data"
        outputDict['RUS10Y'] = "https://www.investing.com/rates-bonds/russia-10-year-bond-yield-historical-data"

        outputDict['SGP1Y'] = "https://www.investing.com/rates-bonds/singapore-1-year-bond-yield-historical-data"
        outputDict['SGP5Y'] = "https://www.investing.com/rates-bonds/singapore-5-year-bond-yield-historical-data"
        outputDict['SGP10Y'] = "https://www.investing.com/rates-bonds/singapore-10-year-bond-yield-historical-data"

        outputDict['SRB1Y'] = "https://www.investing.com/rates-bonds/serbia-1-year-historical-data"
        outputDict['SRB5Y'] = "https://www.investing.com/rates-bonds/serbia-5-year-historical-data"

        outputDict['SVK1Y'] = "https://www.investing.com/rates-bonds/slovakia-1-year-bond-yield-historical-data"
        outputDict['SVK5Y'] = "https://www.investing.com/rates-bonds/slovakia-5-year-bond-yield-historical-data"
        outputDict['SVK10Y'] = "https://www.investing.com/rates-bonds/slovakia-10-year-historical-data"

        outputDict['SVN1Y'] = "https://www.investing.com/rates-bonds/slovenia-1-year-historical-data"
        outputDict['SVN5Y'] = "https://www.investing.com/rates-bonds/slovenia-5-year-bond-yield-historical-data"
        outputDict['SVN10Y'] = "https://www.investing.com/rates-bonds/slovenia-10-year-bond-yield-historical-data"

        outputDict['SWE5Y'] = "https://www.investing.com/rates-bonds/sweden-5-year-bond-yield-historical-data"
        outputDict['SWE10Y'] = "https://www.investing.com/rates-bonds/sweden-10-year-bond-yield-historical-data"

        outputDict['THA1Y'] = "https://www.investing.com/rates-bonds/thailand-1-year-bond-yield-historical-data"
        outputDict['THA5Y'] = "https://www.investing.com/rates-bonds/thailand-5-year-bond-yield-historical-data"
        outputDict['THA10Y'] = "https://www.investing.com/rates-bonds/thailand-10-year-bond-yield-historical-data"

        outputDict['TUR1Y'] = "https://www.investing.com/rates-bonds/turkey-1-year-bond-yield-historical-data"
        outputDict['TUR5Y'] = "https://www.investing.com/rates-bonds/turkey-5-year-bond-yield-historical-data"
        outputDict['TUR10Y'] = "https://www.investing.com/rates-bonds/turkey-10-year-bond-yield-historical-data"

        outputDict['TWN5Y'] = "https://www.investing.com/rates-bonds/taiwan-5-year-bond-yield-historical-data"
        outputDict['TWN10Y'] = "https://www.investing.com/rates-bonds/taiwan-10-year-bond-yield-historical-data"

        outputDict['UGA1Y'] = "https://www.investing.com/rates-bonds/uganda-1-year-bond-yield-historical-data"
        outputDict['UGA5Y'] = "https://www.investing.com/rates-bonds/uganda-5-years-bond-yield-historical-data"
        outputDict['UGA10Y'] = "https://www.investing.com/rates-bonds/uganda-10-years-bond-yield-historical-data"

        outputDict['UKR1Y'] = "https://www.investing.com/rates-bonds/ukraine-1-year-bond-yield-historical-data"

        outputDict['USA1Y'] = "https://www.investing.com/rates-bonds/u.s.-1-year-bond-yield-historical-data"
        outputDict['USA5Y'] = "https://www.investing.com/rates-bonds/u.s.-5-year-bond-yield-historical-data"
        outputDict['USA10Y'] = "https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data"

        outputDict['VEN5Y'] = "https://www.investing.com/rates-bonds/venezuela-4-year-bond-yield-historical-data"

        outputDict['VNM1Y'] = "https://www.investing.com/rates-bonds/vietnam-1-year-bond-yield-historical-data"
        outputDict['VNM5Y'] = "https://www.investing.com/rates-bonds/vietnam-5-year-bond-yield-historical-data"
        outputDict['VNM10Y'] = "https://www.investing.com/rates-bonds/vietnam-10-year-bond-yield-historical-data"

        outputDict['ZAF5Y'] = "https://www.investing.com/rates-bonds/south-africa-5-year-bond-yield-historical-data"
        outputDict['ZAF10Y'] = "https://www.investing.com/rates-bonds/south-africa-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "Watchlist":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['LYB'] = "https://www.investing.com/equities/lyondellbasell-industries-historical-data"
        outputDict['PPG'] = "https://www.investing.com/equities/ppg-industries-historical-data"
        outputDict['SHW'] = "https://www.investing.com/equities/sherwinwilliams-historical-data"
        outputDict['IFF'] = "https://www.investing.com/equities/intl-flav---frag-historical-data"
        outputDict['DWDP'] = "https://www.investing.com/equities/du-pont-historical-data"
        outputDict['PX'] = "https://www.investing.com/equities/praxair-inc-historical-data"
        outputDict['APD'] = "https://www.investing.com/equities/air-prods---chem-historical-data"
        outputDict['EMN'] = "https://www.investing.com/equities/eastman-chem-historical-data"
        outputDict['FMC'] = "https://www.investing.com/equities/fmc-corp-historical-data"
        outputDict['CF'] = "https://www.investing.com/equities/cf-industries-historical-data"
        outputDict['JNJ'] = "https://www.investing.com/equities/johnson-johnson-historical-data"
        outputDict['PFE'] = "https://www.investing.com/equities/pfizer-historical-data"
        outputDict['MRK'] = "https://www.investing.com/equities/merck---co-historical-data"
        outputDict['ABBV'] = "https://www.investing.com/equities/abbvie-inc-historical-data"
        outputDict['BMY'] = "https://www.investing.com/equities/bristol-myer-squiib-historical-data"
        outputDict['LLY'] = "https://www.investing.com/equities/eli-lilly-and-co-historical-data"
        outputDict['UNH'] = "https://www.investing.com/equities/united-health-group-historical-data"
        outputDict['CVS'] = "https://www.investing.com/equities/cvs-corp-historical-data"
        outputDict['ESRX'] = "https://www.investing.com/equities/express-scripts-inc-historical-data"
        outputDict['AET'] = "https://www.investing.com/equities/aetna-inc-historical-data"
        outputDict['ANTM'] = "https://www.investing.com/equities/wellpoint-inc-historical-data"
        outputDict['CI'] = "https://www.investing.com/equities/cigna-corp-historical-data"
        outputDict['HUM'] = "https://www.investing.com/equities/humana-inc-historical-data"
        outputDict['GILD'] = "https://www.investing.com/equities/gilead-sciences-inc-historical-data"
        outputDict['AMGN'] = "https://www.investing.com/equities/amgen-inc-historical-data"
        outputDict['CELG'] = "https://www.investing.com/equities/celgene-corp-historical-data"
        outputDict['BIIB'] = "https://www.investing.com/equities/biogen-idec-inc-historical-data"
        outputDict['REGN'] = "https://www.investing.com/equities/regeneron-phar.-historical-data"
        outputDict['ALXN'] = "https://www.investing.com/equities/alexion-pharmaceuticals,-inc.-historical-data"
        outputDict['VRTX'] = "https://www.investing.com/equities/vertex-pharm-historical-data"
        outputDict['MDT'] = "https://www.investing.com/equities/medtronic-historical-data"
        outputDict['ABT'] = "https://www.investing.com/equities/abbott-laboratories-historical-data"
        outputDict['SYK'] = "https://www.investing.com/equities/stryker-historical-data"
        outputDict['BSX'] = "https://www.investing.com/equities/boston-scien-cp-historical-data"
        outputDict['ZBH'] = "https://www.investing.com/equities/zimmer-hldgs-historical-data"
        outputDict['ISRG'] = "https://www.investing.com/equities/intuitive-surgical-inc-historical-data"
        outputDict['EW'] = "https://www.investing.com/equities/edward-lifescience-historical-data"
        outputDict['VAR'] = "https://www.investing.com/equities/varian-medical-historical-data"
        outputDict['TMO'] = "https://www.investing.com/equities/thermo-fisher-sc-historical-data"
        outputDict['A'] = "https://www.investing.com/equities/agilent-tech-historical-data"
        outputDict['LH'] = "https://www.investing.com/equities/laboratory-corp-of-amer-historical-data"
        outputDict['DGX'] = "https://www.investing.com/equities/quest-diag-historical-data"
        outputDict['PKI'] = "https://www.investing.com/equities/perkinelmer-historical-data"
        outputDict['BDX'] = "https://www.investing.com/equities/becton-dickinsn-historical-data"
        outputDict['BAX'] = "https://www.investing.com/equities/baxter-intl-historical-data"
        outputDict['WAT'] = "https://www.investing.com/equities/waters-corp-historical-data"
        outputDict['XRAY'] = "https://www.investing.com/equities/dentsply-intl-inc-new-historical-data"
        outputDict['HCA'] = "https://www.investing.com/equities/hca-holdings-inc-historical-data"
        outputDict['UHS'] = "https://www.investing.com/equities/universal-health-services-historical-data"
        outputDict['THC'] = "https://www.investing.com/equities/tenet-healthcare-historical-data"
        outputDict['ENDP'] = "https://www.investing.com/equities/endo-pharmaceuticals-historical-data"
        outputDict['DVA'] = "https://www.investing.com/equities/davita-inc-historical-data"
        outputDict['PRGO'] = "https://www.investing.com/equities/perrigo-co-historical-data"
        outputDict['AGN'] = "https://www.investing.com/equities/actavis-historical-data"
        outputDict['MYL'] = "https://www.investing.com/equities/mylan-inc-historical-data"
        outputDict['ZTS'] = "https://www.investing.com/equities/zoetis-inc-historical-data"
        outputDict['MNK'] = "https://www.investing.com/equities/mallinckrodt-historical-data"
        outputDict['AI.PA'] = "https://www.investing.com/equities/air-liquide-historical-data"
        outputDict['BNP.PA'] = "https://www.investing.com/equities/bnp-paribas-historical-data"
        outputDict['ACA.PA'] = "https://www.investing.com/equities/credit-agricole-historical-data"
        outputDict['SAN.PA'] = "https://www.investing.com/equities/sanofi-aventis-historical-data"
        outputDict['GLE.PA'] = "https://www.investing.com/equities/societe-generale-historical-data"
        outputDict['SOLB.BR'] = "https://www.investing.com/equities/solvay-historical-data"
        outputDict['FTI.PA'] = "https://www.investing.com/equities/fmc-technologies-inc-historical-data?cid=7006"
        outputDict['FP.PA'] = "https://www.investing.com/equities/total-historical-data"


        return outputDict
elif OperatingMode == "ETF":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['XLY'] = "https://www.investing.com/etfs/spdr-consumer-discr.-select-sector-historical-data"
        outputDict['XLP'] = "https://www.investing.com/etfs/spdr---consumer-staples-historical-data"
        outputDict['XLE'] = "https://www.investing.com/etfs/spdr-energy-select-sector-fund-historical-data"
        outputDict['XLF'] = "https://www.investing.com/etfs/financial-select-sector-spdr-fund-historical-data"
        outputDict['XLV'] = "https://www.investing.com/etfs/spdr---health-care-historical-data"
        outputDict['XLI'] = "https://www.investing.com/etfs/industrial-sector-spdr-trust-historical-data"
        outputDict['XLB'] = "https://www.investing.com/etfs/spdr-materials-select-sector-etf-historical-data"
        outputDict['XLRE'] = "https://www.investing.com/etfs/real-estate-select-sector-spdr-historical-data"
        outputDict['XLK'] = "https://www.investing.com/etfs/spdr-select-sector---technology-historical-data"
        outputDict['XLU'] = "https://www.investing.com/etfs/spdr-select-sector---utilities-historical-data"
        outputDict['XITK'] = "https://www.investing.com/etfs/spdr-factset-innovative-technology-historical-data"
        outputDict['XNTK'] = "https://www.investing.com/etfs/spdr-ms-technology-historical-data"
        outputDict['XAR'] = "https://www.investing.com/etfs/spdr-s-p-aerospace---defense-historical-data"
        outputDict['KBE'] = "https://www.investing.com/etfs/spdr-kbw-bank-historical-data"
        outputDict['XBI'] = "https://www.investing.com/etfs/spdr-s-p-biotech-historical-data"
        outputDict['KCE'] = "https://www.investing.com/etfs/spdr-kbw-capital-markets-historical-data"
        outputDict['XHE'] = "https://www.investing.com/etfs/spdr-s-p-health-care-equipment-historical-data"
        outputDict['XHS'] = "https://www.investing.com/etfs/spdr-s-p-health-care-services-historical-data"
        outputDict['XHB'] = "https://www.investing.com/etfs/spdr-s-p-homebuilders-historical-data"
        outputDict['KIE'] = "https://www.investing.com/etfs/spdr-kbw-insurance-historical-data"
        outputDict['XWEB'] = "https://www.investing.com/etfs/spdr-sp-internet-historical-data"
        outputDict['XME'] = "https://www.investing.com/etfs/spdr-s-p-metals---mining-historical-data"
        outputDict['XES'] = "https://www.investing.com/etfs/spdr-s-p-oil---gas-eq---services-historical-data"
        outputDict['XOP'] = "https://www.investing.com/etfs/spdr-s-p-oil--gas-explor---product-historical-data"
        outputDict['XPH'] = "https://www.investing.com/etfs/spdr-s-p-pharmaceuticals-historical-data"
        outputDict['KRE'] = "https://www.investing.com/etfs/spdr-kbw-regional-banking-historical-data"
        outputDict['XRT'] = "https://www.investing.com/etfs/spdr-s-p-retail-historical-data"
        outputDict['XSD'] = "https://www.investing.com/etfs/spdr-s-p-semiconductor-historical-data"
        outputDict['XSW'] = "https://www.investing.com/etfs/spdr-s-p-software---services-historical-data"
        outputDict['XTH'] = "https://www.investing.com/etfs/spdr-sp-technology-hardware-historical-data"
        outputDict['XTL'] = "https://www.investing.com/etfs/spdr-s-p-telecom-historical-data"
        outputDict['XTN'] = "https://www.investing.com/etfs/spdr-s-p-transportation-historical-data"
        outputDict['RWO'] = "https://www.investing.com/etfs/spdr-wilshire-global-real-estate-historical-data"
        outputDict['RWX'] = "https://www.investing.com/etfs/spdr-dj-wilshire-intl-real-estate-historical-data"
        outputDict['RWR'] = "https://www.investing.com/etfs/spdr-dj-wilshire-reit-historical-data"
        outputDict['GLD'] = "https://www.investing.com/etfs/spdr-gold-trust-historical-data"
        outputDict['SLV'] = "https://www.investing.com/etfs/ishares-silver-trust-historical-data"
        outputDict['GLDW'] = "https://www.investing.com/etfs/spdr-long-dollar-gold-trust-historical-data"
        outputDict['GII'] = "https://www.investing.com/etfs/spdr-ftse-macquarie-gi-100-historical-data"
        outputDict['GNR'] = "https://www.investing.com/etfs/spdr-s-p-global-natural-resources-historical-data"
        outputDict['NANR'] = "https://www.investing.com/etfs/spdr-sp-north-american-natural-res-historical-data"


        return outputDict
elif OperatingMode == "AR":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ARG1Y'] = "https://www.investing.com/rates-bonds/argentina-1-year-historical-data"
        outputDict['ARG4Y'] = "https://www.investing.com/rates-bonds/argentina-4-year-bond-yield-historical-data"
        outputDict['ARG6Y'] = "https://www.investing.com/rates-bonds/argentina-6-year-historical-data"
        outputDict['ARG9Y'] = "https://www.investing.com/rates-bonds/argentina-9-year-historical-data"


        return outputDict
elif OperatingMode == "AU":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['AUS1Y'] = "https://www.investing.com/rates-bonds/australia-1-year-bond-yield-historical-data"
        outputDict['AUS2Y'] = "https://www.investing.com/rates-bonds/australia-2-year-bond-yield-historical-data"
        outputDict['AUS3Y'] = "https://www.investing.com/rates-bonds/australia-3-year-bond-yield-historical-data"
        outputDict['AUS4Y'] = "https://www.investing.com/rates-bonds/australia-4-year-bond-yield-historical-data"
        outputDict['AUS5Y'] = "https://www.investing.com/rates-bonds/australia-5-year-bond-yield-historical-data"
        outputDict['AUS6Y'] = "https://www.investing.com/rates-bonds/australia-6-year-bond-yield-historical-data"
        outputDict['AUS7Y'] = "https://www.investing.com/rates-bonds/australia-7-year-bond-yield-historical-data"
        outputDict['AUS8Y'] = "https://www.investing.com/rates-bonds/australia-8-year-bond-yield-historical-data"
        outputDict['AUS9Y'] = "https://www.investing.com/rates-bonds/australia-9-year-bond-yield-historical-data"
        outputDict['AUS10Y'] = "https://www.investing.com/rates-bonds/australia-10-year-bond-yield-historical-data"
        outputDict['AUS12Y'] = "https://www.investing.com/rates-bonds/australia-12-year-bond-yield-historical-data"
        outputDict['AUS15Y'] = "https://www.investing.com/rates-bonds/australia-15-year-bond-yield-historical-data"
        outputDict['AUS20Y'] = "https://www.investing.com/rates-bonds/australia-20-year-historical-data"
        outputDict['AUS30Y'] = "https://www.investing.com/rates-bonds/australia-30-year-historical-data"


        return outputDict
elif OperatingMode == "AT":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['AUT1Y'] = "https://www.investing.com/rates-bonds/austria-1-year-bond-yield-historical-data"
        outputDict['AUT2Y'] = "https://www.investing.com/rates-bonds/austria-2-year-bond-yield-historical-data"
        outputDict['AUT3Y'] = "https://www.investing.com/rates-bonds/austria-3-year-bond-yield-historical-data"
        outputDict['AUT4Y'] = "https://www.investing.com/rates-bonds/austria-4-year-bond-yield-historical-data"
        outputDict['AUT5Y'] = "https://www.investing.com/rates-bonds/austria-5-year-bond-yield-historical-data"
        outputDict['AUT6Y'] = "https://www.investing.com/rates-bonds/austria-6-year-bond-yield-historical-data"
        outputDict['AUT7Y'] = "https://www.investing.com/rates-bonds/austria-7-year-bond-yield-historical-data"
        outputDict['AUT8Y'] = "https://www.investing.com/rates-bonds/austria-8-year-bond-yield-historical-data"
        outputDict['AUT9Y'] = "https://www.investing.com/rates-bonds/austria-9-year-historical-data"
        outputDict['AUT10Y'] = "https://www.investing.com/rates-bonds/austria-10-year-bond-yield-historical-data"
        outputDict['AUT15Y'] = "https://www.investing.com/rates-bonds/austria-15-year-bond-yield-historical-data"
        outputDict['AUT20Y'] = "https://www.investing.com/rates-bonds/austria-9-year-bond-yield-historical-data"
        outputDict['AUT25Y'] = "https://www.investing.com/rates-bonds/austria-25-year-bond-yield-historical-data"
        outputDict['AUT30Y'] = "https://www.investing.com/rates-bonds/austria-30-year-historical-data"
        outputDict['AUT50Y'] = "https://www.investing.com/rates-bonds/austria-50-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "BH":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['BHR3M'] = "https://www.investing.com/rates-bonds/bahrain-3-month-historical-data"
        outputDict['BHR6M'] = "https://www.investing.com/rates-bonds/bahrain-6-month-historical-data"
        outputDict['BHR9M'] = "https://www.investing.com/rates-bonds/bahrain-9-month-historical-data"
        outputDict['BHR1Y'] = "https://www.investing.com/rates-bonds/bahrain-1-year-historical-data"
        outputDict['BHR2Y'] = "https://www.investing.com/rates-bonds/bahrain-2-year-historical-data"
        outputDict['BHR5Y'] = "https://www.investing.com/rates-bonds/bahrain-5-year-historical-data"


        return outputDict
elif OperatingMode == "BD":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['BGD3M'] = "https://www.investing.com/rates-bonds/bangladesh-3-month-historical-data"
        outputDict['BGD6M'] = "https://www.investing.com/rates-bonds/bangladesh-6-month-historical-data"
        outputDict['BGD1Y'] = "https://www.investing.com/rates-bonds/bangladesh-1-year-historical-data"
        outputDict['BGD2Y'] = "https://www.investing.com/rates-bonds/bangladesh-2-year-historical-data"
        outputDict['BGD5Y'] = "https://www.investing.com/rates-bonds/bangladesh-5-year-historical-data"
        outputDict['BGD10Y'] = "https://www.investing.com/rates-bonds/bangladesh-10-year-historical-data"
        outputDict['BGD15Y'] = "https://www.investing.com/rates-bonds/bangladesh-15-year-historical-data"
        outputDict['BGD20Y'] = "https://www.investing.com/rates-bonds/bangladesh-20-year-historical-data"


        return outputDict
elif OperatingMode == "BE":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['BEL1M'] = "https://www.investing.com/rates-bonds/belgium-1-month-historical-data"
        outputDict['BEL3M'] = "https://www.investing.com/rates-bonds/belguim-3-month-bond-yield-historical-data"
        outputDict['BEL6M'] = "https://www.investing.com/rates-bonds/belguim-6-month-bond-yield-historical-data"
        outputDict['BEL9M'] = "https://www.investing.com/rates-bonds/belgium-9-month-historical-data"
        outputDict['BEL1Y'] = "https://www.investing.com/rates-bonds/belguim-1-year-bond-yield-historical-data"
        outputDict['BEL2Y'] = "https://www.investing.com/rates-bonds/belguim-2-year-bond-yield-historical-data"
        outputDict['BEL3Y'] = "https://www.investing.com/rates-bonds/belguim-3-year-bond-yield-historical-data"
        outputDict['BEL4Y'] = "https://www.investing.com/rates-bonds/belguim-4-year-bond-yield-historical-data"
        outputDict['BEL5Y'] = "https://www.investing.com/rates-bonds/belguim-5-year-bond-yield-historical-data"
        outputDict['BEL6Y'] = "https://www.investing.com/rates-bonds/belguim-6-year-bond-yield-historical-data"
        outputDict['BEL7Y'] = "https://www.investing.com/rates-bonds/belguim-7-year-bond-yield-historical-data"
        outputDict['BEL8Y'] = "https://www.investing.com/rates-bonds/belguim-8-year-bond-yield-historical-data"
        outputDict['BEL9Y'] = "https://www.investing.com/rates-bonds/belguim-9-year-bond-yield-historical-data"
        outputDict['BEL10Y'] = "https://www.investing.com/rates-bonds/belguim-10-year-bond-yield-historical-data"
        outputDict['BEL15Y'] = "https://www.investing.com/rates-bonds/belguim-15-year-bond-yield-historical-data"
        outputDict['BEL20Y'] = "https://www.investing.com/rates-bonds/belguim-20-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "BW":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['BWA6M'] = "https://www.investing.com/rates-bonds/botswana-6-months-bond-yield-historical-data"
        outputDict['BWA3Y'] = "https://www.investing.com/rates-bonds/botswana-3-years-bond-yield-historical-data"
        outputDict['BWA5Y'] = "https://www.investing.com/rates-bonds/botswana-5-years-historical-data"
        outputDict['BWA7Y'] = "https://www.investing.com/rates-bonds/botswana-7-years-bond-yield-historical-data"
        outputDict['BWA13Y'] = "https://www.investing.com/rates-bonds/botswana-13-years-historical-data"


        return outputDict
elif OperatingMode == "BR":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['BRA3M'] = "https://www.investing.com/rates-bonds/brazil-3-month-historical-data"
        outputDict['BRA6M'] = "https://www.investing.com/rates-bonds/brazil-6-month-historical-data"
        outputDict['BRA9M'] = "https://www.investing.com/rates-bonds/brazil-9-month-bond-yield-historical-data"
        outputDict['BRA1Y'] = "https://www.investing.com/rates-bonds/brazil-1-year-bond-yield-historical-data"
        outputDict['BRA2Y'] = "https://www.investing.com/rates-bonds/brazil-2-year-bond-yield-historical-data"
        outputDict['BRA3Y'] = "https://www.investing.com/rates-bonds/brazil-3-year-bond-yield-historical-data"
        outputDict['BRA5Y'] = "https://www.investing.com/rates-bonds/brazil-5-year-bond-yield-historical-data"
        outputDict['BRA8Y'] = "https://www.investing.com/rates-bonds/brazil-6-year-bond-yield-historical-data"
        outputDict['BRA10Y'] = "https://www.investing.com/rates-bonds/brazil-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "BG":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['BGR1M'] = "https://www.investing.com/rates-bonds/bulgaria-1-month-bond-yield-historical-data"
        outputDict['BGR1Y'] = "https://www.investing.com/rates-bonds/bulgaria-1-year-bond-yield-historical-data"
        outputDict['BGR3Y'] = "https://www.investing.com/rates-bonds/bulgaria-3-year-bond-yield-historical-data"
        outputDict['BGR5Y'] = "https://www.investing.com/rates-bonds/bulgaria-5-year-bond-yield-historical-data"
        outputDict['BGR7Y'] = "https://www.investing.com/rates-bonds/bulgaria-7-year-bond-yield-historical-data"
        outputDict['BGR10Y'] = "https://www.investing.com/rates-bonds/bulgaria-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "CA":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['CAN1M'] = "https://www.investing.com/rates-bonds/canada-1-month-bond-yield-historical-data"
        outputDict['CAN2M'] = "https://www.investing.com/rates-bonds/canada-2-month-bond-yield-historical-data"
        outputDict['CAN3M'] = "https://www.investing.com/rates-bonds/canada-3-month-bond-yield-historical-data"
        outputDict['CAN6M'] = "https://www.investing.com/rates-bonds/canada-6-month-bond-yield-historical-data"
        outputDict['CAN1Y'] = "https://www.investing.com/rates-bonds/canada-1-year-bond-yield-historical-data"
        outputDict['CAN2Y'] = "https://www.investing.com/rates-bonds/canada-2-year-bond-yield-historical-data"
        outputDict['CAN3Y'] = "https://www.investing.com/rates-bonds/canada-3-year-bond-yield-historical-data"
        outputDict['CAN4Y'] = "https://www.investing.com/rates-bonds/canada-4-year-bond-yield-historical-data"
        outputDict['CAN5Y'] = "https://www.investing.com/rates-bonds/canada-5-year-bond-yield-historical-data"
        outputDict['CAN7Y'] = "https://www.investing.com/rates-bonds/canada-7-year-bond-yield-historical-data"
        outputDict['CAN10Y'] = "https://www.investing.com/rates-bonds/canada-10-year-bond-yield-historical-data"
        outputDict['CAN20Y'] = "https://www.investing.com/rates-bonds/canada-20-year-bond-yield-historical-data"
        outputDict['CAN30Y'] = "https://www.investing.com/rates-bonds/canada-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "CL":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['CHL1M'] = "https://www.investing.com/rates-bonds/chile-1-month-bond-yield-historical-data"
        outputDict['CHL1Y'] = "https://www.investing.com/rates-bonds/chile-1-year-bond-yield-historical-data"
        outputDict['CHL2Y'] = "https://www.investing.com/rates-bonds/chile-2-year-bond-yield-historical-data"
        outputDict['CHL3Y'] = "https://www.investing.com/rates-bonds/chile-3-year-bond-yield-historical-data"
        outputDict['CHL4Y'] = "https://www.investing.com/rates-bonds/chile-4-year-bond-yield-historical-data"
        outputDict['CHL5Y'] = "https://www.investing.com/rates-bonds/chile-5-year-bond-yield-historical-data"
        outputDict['CHL8Y'] = "https://www.investing.com/rates-bonds/chile-8-year-bond-yield-historical-data"
        outputDict['CHL10Y'] = "https://www.investing.com/rates-bonds/chile-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "CN":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['CHN1Y'] = "https://www.investing.com/rates-bonds/china-1-year-bond-yield-historical-data"
        outputDict['CHN2Y'] = "https://www.investing.com/rates-bonds/china-2-year-bond-yield-historical-data"
        outputDict['CHN3Y'] = "https://www.investing.com/rates-bonds/china-3-year-bond-yield-historical-data"
        outputDict['CHN5Y'] = "https://www.investing.com/rates-bonds/china-5-year-bond-yield-historical-data"
        outputDict['CHN7Y'] = "https://www.investing.com/rates-bonds/china-7-year-bond-yield-historical-data"
        outputDict['CHN10Y'] = "https://www.investing.com/rates-bonds/china-10-year-bond-yield-historical-data"
        outputDict['CHN15Y'] = "https://www.investing.com/rates-bonds/china-15-year-bond-yield-historical-data"
        outputDict['CHN20Y'] = "https://www.investing.com/rates-bonds/china-20-year-bond-yield-historical-data"
        outputDict['CHN30Y'] = "https://www.investing.com/rates-bonds/china-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "CO":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['COL1Y'] = "https://www.investing.com/rates-bonds/colombia-2-year-bond-yield-historical-data"
        outputDict['COL4Y'] = "https://www.investing.com/rates-bonds/colombia-3-year-bond-yield-historical-data"
        outputDict['COL5Y'] = "https://www.investing.com/rates-bonds/colombia-5-year-bond-yield-historical-data"
        outputDict['COL10Y'] = "https://www.investing.com/rates-bonds/colombia-10-year-bond-yield-historical-data"
        outputDict['COL15Y'] = "https://www.investing.com/rates-bonds/colombia-15-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "HR":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['HRV6M'] = "https://www.investing.com/rates-bonds/croatia-6-month-bond-yield-historical-data"
        outputDict['HRV9M'] = "https://www.investing.com/rates-bonds/croatia-9-month-bond-yield-historical-data"
        outputDict['HRV1Y'] = "https://www.investing.com/rates-bonds/croatia-1-year-bond-yield-historical-data"
        outputDict['HRV3Y'] = "https://www.investing.com/rates-bonds/croatia-3-year-bond-yield-historical-data"
        outputDict['HRV5Y'] = "https://www.investing.com/rates-bonds/croatia-5-year-bond-yield-historical-data"
        outputDict['HRV10Y'] = "https://www.investing.com/rates-bonds/croatia-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "CZ":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['CZE1Y'] = "https://www.investing.com/rates-bonds/czech-republic-1-year-bond-yield-historical-data"
        outputDict['CZE2Y'] = "https://www.investing.com/rates-bonds/czech-republic-2-year-bond-yield-historical-data"
        outputDict['CZE3Y'] = "https://www.investing.com/rates-bonds/czech-republic-3-year-bond-yield-historical-data"
        outputDict['CZE4Y'] = "https://www.investing.com/rates-bonds/czech-republic-4-year-bond-yield-historical-data"
        outputDict['CZE5Y'] = "https://www.investing.com/rates-bonds/czech-republic-5-year-bond-yield-historical-data"
        outputDict['CZE6Y'] = "https://www.investing.com/rates-bonds/czech-republic-6-year-bond-yield-historical-data"
        outputDict['CZE7Y'] = "https://www.investing.com/rates-bonds/czech-republic-7-year-bond-yield-historical-data"
        outputDict['CZE8Y'] = "https://www.investing.com/rates-bonds/czech-republic-8-year-historical-data"
        outputDict['CZE9Y'] = "https://www.investing.com/rates-bonds/czech-republic-9-year-bond-yield-historical-data"
        outputDict['CZE10Y'] = "https://www.investing.com/rates-bonds/czech-republic-10-year-bond-yield-historical-data"
        outputDict['CZE15Y'] = "https://www.investing.com/rates-bonds/czech-republic-15-year-bond-yield-historical-data"
        outputDict['CZE20Y'] = "https://www.investing.com/rates-bonds/czech-republic-20-year-historical-data"
        outputDict['CZE50Y'] = "https://www.investing.com/rates-bonds/czech-republic-50-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "DK":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['DNK3M'] = "https://www.investing.com/rates-bonds/denmark-3-month-bond-yield-historical-data"
        outputDict['DNK6M'] = "https://www.investing.com/rates-bonds/denmark-6-month-bond-yield-historical-data"
        outputDict['DNK2Y'] = "https://www.investing.com/rates-bonds/denmark-2-year-bond-yield-historical-data"
        outputDict['DNK3Y'] = "https://www.investing.com/rates-bonds/denmark-3-year-bond-yield-historical-data"
        outputDict['DNK5Y'] = "https://www.investing.com/rates-bonds/denmark-5-year-bond-yield-historical-data"
        outputDict['DNK8Y'] = "https://www.investing.com/rates-bonds/denmark-8-year-bond-yield-historical-data"
        outputDict['DNK10Y'] = "https://www.investing.com/rates-bonds/denmark-10-year-bond-yield-historical-data"
        outputDict['DNK30Y'] = "https://www.investing.com/rates-bonds/denmark-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "EG":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['EGYOvernight'] = "https://www.investing.com/rates-bonds/egypt-overnight-rate-historical-data"
        outputDict['EGY3M'] = "https://www.investing.com/rates-bonds/egypt-3-month-bond-yield-historical-data"
        outputDict['EGY6M'] = "https://www.investing.com/rates-bonds/egypt-6-month-bond-yield-historical-data"
        outputDict['EGY9M'] = "https://www.investing.com/rates-bonds/egypt-9-month-bond-yield-historical-data"
        outputDict['EGY1Y'] = "https://www.investing.com/rates-bonds/egypt-1-year-bond-yield-historical-data"
        outputDict['EGY2Y'] = "https://www.investing.com/rates-bonds/egypt-2-year-historical-data"
        outputDict['EGY3Y'] = "https://www.investing.com/rates-bonds/egypt-3-year-bond-yield-historical-data"
        outputDict['EGY5Y'] = "https://www.investing.com/rates-bonds/egypt-5-year-bond-yield-historical-data"
        outputDict['EGY7Y'] = "https://www.investing.com/rates-bonds/egypt-7-year-bond-yield-historical-data"
        outputDict['EGY10Y'] = "https://www.investing.com/rates-bonds/egypt-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "FI":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['FIN2Y'] = "https://www.investing.com/rates-bonds/finland-2-year-bond-yield-historical-data"
        outputDict['FIN3Y'] = "https://www.investing.com/rates-bonds/finland-3-year-bond-yield-historical-data"
        outputDict['FIN4Y'] = "https://www.investing.com/rates-bonds/finland-4-year-bond-yield-historical-data"
        outputDict['FIN5Y'] = "https://www.investing.com/rates-bonds/finland-5-year-bond-yield-historical-data"
        outputDict['FIN6Y'] = "https://www.investing.com/rates-bonds/finland-6-year-bond-yield-historical-data"
        outputDict['FIN8Y'] = "https://www.investing.com/rates-bonds/finland-8-year-bond-yield-historical-data"
        outputDict['FIN10Y'] = "https://www.investing.com/rates-bonds/finland-10-year-bond-yield-historical-data"
        outputDict['FIN15Y'] = "https://www.investing.com/rates-bonds/finland-15-year-bond-yield-historical-data"
        outputDict['FIN30Y'] = "https://www.investing.com/rates-bonds/finland-30-year-historical-data"


        return outputDict
elif OperatingMode == "FR":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['FRA1M'] = "https://www.investing.com/rates-bonds/france-1-month-bond-yield-historical-data"
        outputDict['FRA3M'] = "https://www.investing.com/rates-bonds/france-3-month-bond-yield-historical-data"
        outputDict['FRA6M'] = "https://www.investing.com/rates-bonds/france-6-month-bond-yield-historical-data"
        outputDict['FRA9M'] = "https://www.investing.com/rates-bonds/france-9-month-bond-yield-historical-data"
        outputDict['FRA1Y'] = "https://www.investing.com/rates-bonds/france-1-year-bond-yield-historical-data"
        outputDict['FRA2Y'] = "https://www.investing.com/rates-bonds/france-2-year-bond-yield-historical-data"
        outputDict['FRA3Y'] = "https://www.investing.com/rates-bonds/france-3-year-bond-yield-historical-data"
        outputDict['FRA4Y'] = "https://www.investing.com/rates-bonds/france-4-year-bond-yield-historical-data"
        outputDict['FRA5Y'] = "https://www.investing.com/rates-bonds/france-5-year-bond-yield-historical-data"
        outputDict['FRA6Y'] = "https://www.investing.com/rates-bonds/france-6-year-bond-yield-historical-data"
        outputDict['FRA7Y'] = "https://www.investing.com/rates-bonds/france-7-year-bond-yield-historical-data"
        outputDict['FRA8Y'] = "https://www.investing.com/rates-bonds/france-8-year-bond-yield-historical-data"
        outputDict['FRA9Y'] = "https://www.investing.com/rates-bonds/france-9-year-bond-yield-historical-data"
        outputDict['FRA10Y'] = "https://www.investing.com/rates-bonds/france-10-year-bond-yield-historical-data"
        outputDict['FRA15Y'] = "https://www.investing.com/rates-bonds/france-15-year-bond-yield-historical-data"
        outputDict['FRA20Y'] = "https://www.investing.com/rates-bonds/france-20-year-bond-yield-historical-data"
        outputDict['FRA25Y'] = "https://www.investing.com/rates-bonds/france-25-year-historical-data"
        outputDict['FRA30Y'] = "https://www.investing.com/rates-bonds/france-30-year-bond-yield-historical-data"
        outputDict['FRA50Y'] = "https://www.investing.com/rates-bonds/france-50-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "DE":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['DEU3M'] = "https://www.investing.com/rates-bonds/germany-3-month-bond-yield-historical-data"
        outputDict['DEU6M'] = "https://www.investing.com/rates-bonds/germany-6-month-bond-yield-historical-data"
        outputDict['DEU9M'] = "https://www.investing.com/rates-bonds/germany-9-month-bond-yield-historical-data"
        outputDict['DEU1Y'] = "https://www.investing.com/rates-bonds/germany-1-year-bond-yield-historical-data"
        outputDict['DEU2Y'] = "https://www.investing.com/rates-bonds/germany-2-year-bond-yield-historical-data"
        outputDict['DEU3Y'] = "https://www.investing.com/rates-bonds/germany-3-year-bond-yield-historical-data"
        outputDict['DEU4Y'] = "https://www.investing.com/rates-bonds/germany-4-year-bond-yield-historical-data"
        outputDict['DEU5Y'] = "https://www.investing.com/rates-bonds/germany-5-year-bond-yield-historical-data"
        outputDict['DEU6Y'] = "https://www.investing.com/rates-bonds/germany-6-year-bond-yield-historical-data"
        outputDict['DEU7Y'] = "https://www.investing.com/rates-bonds/germany-7-year-bond-yield-historical-data"
        outputDict['DEU8Y'] = "https://www.investing.com/rates-bonds/germany-8-year-bond-yield-historical-data"
        outputDict['DEU9Y'] = "https://www.investing.com/rates-bonds/germany-9-year-bond-yield-historical-data"
        outputDict['DEU10Y'] = "https://www.investing.com/rates-bonds/germany-10-year-bond-yield-historical-data"
        outputDict['DEU15Y'] = "https://www.investing.com/rates-bonds/germany-15-year-bond-yield-historical-data"
        outputDict['DEU20Y'] = "https://www.investing.com/rates-bonds/germany-20-year-bond-yield-historical-data"
        outputDict['DEU25Y'] = "https://www.investing.com/rates-bonds/germany-25-year-historical-data"
        outputDict['DEU30Y'] = "https://www.investing.com/rates-bonds/germany-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "GR":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['GRC1M'] = "https://www.investing.com/rates-bonds/greece-7-year-bond-yield-historical-data"
        outputDict['GRC3M'] = "https://www.investing.com/rates-bonds/greece-3-month-bond-yield-historical-data"
        outputDict['GRC6M'] = "https://www.investing.com/rates-bonds/greece-6-month-bond-yield-historical-data"
        outputDict['GRC5Y'] = "https://www.investing.com/rates-bonds/greece-5-year-bond-yield-historical-data"
        outputDict['GRC10Y'] = "https://www.investing.com/rates-bonds/greece-10-year-bond-yield-historical-data"
        outputDict['GRC15Y'] = "https://www.investing.com/rates-bonds/greece-15-year-bond-yield-historical-data"
        outputDict['GRC20Y'] = "https://www.investing.com/rates-bonds/greece-3-year-bond-yield-historical-data"
        outputDict['GRC25Y'] = "https://www.investing.com/rates-bonds/greece-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "HK":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['HKG1W'] = "https://www.investing.com/rates-bonds/hong-kong-1-week-bond-yield-historical-data"
        outputDict['HKG1M'] = "https://www.investing.com/rates-bonds/hong-kong-1-month-bond-yield-historical-data"
        outputDict['HKG3M'] = "https://www.investing.com/rates-bonds/hong-kong-3-month-bond-yield-historical-data"
        outputDict['HKG6M'] = "https://www.investing.com/rates-bonds/hong-kong-6-month-bond-yield-historical-data"
        outputDict['HKG9M'] = "https://www.investing.com/rates-bonds/hong-kong-9-month-bond-yield-historical-data"
        outputDict['HKG1Y'] = "https://www.investing.com/rates-bonds/hong-kong-1-year-bond-yield-historical-data"
        outputDict['HKG2Y'] = "https://www.investing.com/rates-bonds/hong-kong-2-year-bond-yield-historical-data"
        outputDict['HKG3Y'] = "https://www.investing.com/rates-bonds/hong-kong-3-year-bond-yield-historical-data"
        outputDict['HKG5Y'] = "https://www.investing.com/rates-bonds/hong-kong-5-year-bond-yield-historical-data"
        outputDict['HKG7Y'] = "https://www.investing.com/rates-bonds/hong-kong-7-year-bond-yield-historical-data"
        outputDict['HKG10Y'] = "https://www.investing.com/rates-bonds/hong-kong-10-year-bond-yield-historical-data"
        outputDict['HKG15Y'] = "https://www.investing.com/rates-bonds/hong-kong-15-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "HU":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['HUN3M'] = "https://www.investing.com/rates-bonds/hungary-3-month-bond-yield-historical-data"
        outputDict['HUN6M'] = "https://www.investing.com/rates-bonds/hungary-6-month-bond-yield-historical-data"
        outputDict['HUN1Y'] = "https://www.investing.com/rates-bonds/hungary-1-year-bond-yield-historical-data"
        outputDict['HUN3Y'] = "https://www.investing.com/rates-bonds/hungary-3-year-bond-yield-historical-data"
        outputDict['HUN5Y'] = "https://www.investing.com/rates-bonds/hungary-5-year-bond-yield-historical-data"
        outputDict['HUN10Y'] = "https://www.investing.com/rates-bonds/hungary-10-year-bond-yield-historical-data"
        outputDict['HUN15Y'] = "https://www.investing.com/rates-bonds/hungary-15-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "IS":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ISL2Y'] = "https://www.investing.com/rates-bonds/iceland-2-year-bond-yield-historical-data"
        outputDict['ISL5Y'] = "https://www.investing.com/rates-bonds/iceland-5-year-bond-yield-historical-data"
        outputDict['ISL10Y'] = "https://www.investing.com/rates-bonds/iceland-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "IN":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['IND3M'] = "https://www.investing.com/rates-bonds/india-3-month-bond-yield-historical-data"
        outputDict['IND6M'] = "https://www.investing.com/rates-bonds/india-6-month-bond-yield-historical-data"
        outputDict['IND1Y'] = "https://www.investing.com/rates-bonds/india-1-year-bond-yield-historical-data"
        outputDict['IND2Y'] = "https://www.investing.com/rates-bonds/india-2-year-bond-yield-historical-data"
        outputDict['IND3Y'] = "https://www.investing.com/rates-bonds/india-3-year-bond-yield-historical-data"
        outputDict['IND4Y'] = "https://www.investing.com/rates-bonds/india-4-year-bond-yield-historical-data"
        outputDict['IND5Y'] = "https://www.investing.com/rates-bonds/india-5-year-bond-yield-historical-data"
        outputDict['IND6Y'] = "https://www.investing.com/rates-bonds/india-6-year-bond-yield-historical-data"
        outputDict['IND7Y'] = "https://www.investing.com/rates-bonds/india-7-year-bond-yield-historical-data"
        outputDict['IND8Y'] = "https://www.investing.com/rates-bonds/india-8-year-bond-yield-historical-data"
        outputDict['IND9Y'] = "https://www.investing.com/rates-bonds/india-9-year-bond-yield-historical-data"
        outputDict['IND10Y'] = "https://www.investing.com/rates-bonds/india-10-year-bond-yield-historical-data"
        outputDict['IND11Y'] = "https://www.investing.com/rates-bonds/india-11-year-bond-yield-historical-data"
        outputDict['IND12Y'] = "https://www.investing.com/rates-bonds/india-12-year-bond-yield-historical-data"
        outputDict['IND13Y'] = "https://www.investing.com/rates-bonds/india-13-year-bond-yield-historical-data"
        outputDict['IND14Y'] = "https://www.investing.com/rates-bonds/india-14-year-bond-yield-historical-data"
        outputDict['IND15Y'] = "https://www.investing.com/rates-bonds/india-15-year-bond-yield-historical-data"
        outputDict['IND19Y'] = "https://www.investing.com/rates-bonds/india-19-year-bond-yield-historical-data"
        outputDict['IND24Y'] = "https://www.investing.com/rates-bonds/india-24-year-bond-yield-historical-data"
        outputDict['IND30Y'] = "https://www.investing.com/rates-bonds/india-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "ID":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['IDN1M'] = "https://www.investing.com/rates-bonds/indonesia-1-month-historical-data"
        outputDict['IDN3M'] = "https://www.investing.com/rates-bonds/indonesia-3-month-historical-data"
        outputDict['IDN6M'] = "https://www.investing.com/rates-bonds/indonesia-6-month-bond-yield-historical-data"
        outputDict['IDN1Y'] = "https://www.investing.com/rates-bonds/indonesia-1-year-bond-yield-historical-data"
        outputDict['IDN3Y'] = "https://www.investing.com/rates-bonds/indonesia-3-year-bond-yield-historical-data"
        outputDict['IDN5Y'] = "https://www.investing.com/rates-bonds/indonesia-5-year-bond-yield-historical-data"
        outputDict['IDN10Y'] = "https://www.investing.com/rates-bonds/indonesia-10-year-bond-yield-historical-data"
        outputDict['IDN15Y'] = "https://www.investing.com/rates-bonds/indonesia-15-year-bond-yield-historical-data"
        outputDict['IDN20Y'] = "https://www.investing.com/rates-bonds/indonesia-20-year-bond-yield-historical-data"
        outputDict['IDN25Y'] = "https://www.investing.com/rates-bonds/indonesia-25-year-bond-yield-historical-data"
        outputDict['IDN30Y'] = "https://www.investing.com/rates-bonds/indonesia-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "IE":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['IRL3M'] = "https://www.investing.com/rates-bonds/ireland-3-month-historical-data"
        outputDict['IRL6M'] = "https://www.investing.com/rates-bonds/ireland-6-month-historical-data"
        outputDict['IRL1Y'] = "https://www.investing.com/rates-bonds/ireland-1-year-bond-yield-historical-data"
        outputDict['IRL2Y'] = "https://www.investing.com/rates-bonds/ireland-2-year-bond-yield-historical-data"
        outputDict['IRL3Y'] = "https://www.investing.com/rates-bonds/ireland-3-year-bond-yield-historical-data"
        outputDict['IRL4Y'] = "https://www.investing.com/rates-bonds/ireland-4-year-historical-data"
        outputDict['IRL5Y'] = "https://www.investing.com/rates-bonds/ireland-5-year-bond-yield-historical-data"
        outputDict['IRL6Y'] = "https://www.investing.com/rates-bonds/ireland-6-year-historical-data"
        outputDict['IRL7Y'] = "https://www.investing.com/rates-bonds/ireland-7-year-bond-yield-historical-data"
        outputDict['IRL8Y'] = "https://www.investing.com/rates-bonds/ireland-8-year-bond-yield-historical-data"
        outputDict['IRL10Y'] = "https://www.investing.com/rates-bonds/ireland-10-year-bond-yield-historical-data"
        outputDict['IRL15Y'] = "https://www.investing.com/rates-bonds/ireland-15-year-bond-yield-historical-data"
        outputDict['IRL20Y'] = "https://www.investing.com/rates-bonds/ireland-20-year-bond-yield-historical-data"
        outputDict['IRL30Y'] = "https://www.investing.com/rates-bonds/ireland-30-year-historical-data"


        return outputDict
elif OperatingMode == "IL":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ISR1M'] = "https://www.investing.com/rates-bonds/israel-1-month-historical-data"
        outputDict['ISR3M'] = "https://www.investing.com/rates-bonds/israel-3-month-bond-yield-historical-data"
        outputDict['ISR6M'] = "https://www.investing.com/rates-bonds/israel-6-month-historical-data"
        outputDict['ISR9M'] = "https://www.investing.com/rates-bonds/israel-9-month-historical-data"
        outputDict['ISR1Y'] = "https://www.investing.com/rates-bonds/israel-1-year-bond-yield-historical-data"
        outputDict['ISR2Y'] = "https://www.investing.com/rates-bonds/israel-2-year-historical-data"
        outputDict['ISR3Y'] = "https://www.investing.com/rates-bonds/israel-3-year-bond-yield-historical-data"
        outputDict['ISR5Y'] = "https://www.investing.com/rates-bonds/israel-5-year-bond-yield-historical-data"
        outputDict['ISR10Y'] = "https://www.investing.com/rates-bonds/israel-10-year-bond-yield-historical-data"
        outputDict['ISR30Y'] = "https://www.investing.com/rates-bonds/israel-30-year-historical-data"


        return outputDict
elif OperatingMode == "IT":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ITA1M'] = "https://www.investing.com/rates-bonds/italy-1-month-historical-data"
        outputDict['ITA3M'] = "https://www.investing.com/rates-bonds/italy-3-month-bond-yield-historical-data"
        outputDict['ITA6M'] = "https://www.investing.com/rates-bonds/italy-6-month-bond-yield-historical-data"
        outputDict['ITA9M'] = "https://www.investing.com/rates-bonds/italy-9-month-bond-yield-historical-data"
        outputDict['ITA1Y'] = "https://www.investing.com/rates-bonds/italy-1-year-bond-yield-historical-data"
        outputDict['ITA2Y'] = "https://www.investing.com/rates-bonds/italy-2-year-bond-yield-historical-data"
        outputDict['ITA3Y'] = "https://www.investing.com/rates-bonds/italy-3-year-bond-yield-historical-data"
        outputDict['ITA4Y'] = "https://www.investing.com/rates-bonds/italy-4-year-bond-yield-historical-data"
        outputDict['ITA5Y'] = "https://www.investing.com/rates-bonds/italy-5-year-bond-yield-historical-data"
        outputDict['ITA6Y'] = "https://www.investing.com/rates-bonds/italy-6-year-bond-yield-historical-data"
        outputDict['ITA7Y'] = "https://www.investing.com/rates-bonds/italy-7-year-bond-yield-historical-data"
        outputDict['ITA8Y'] = "https://www.investing.com/rates-bonds/italy-8-year-bond-yield-historical-data"
        outputDict['ITA9Y'] = "https://www.investing.com/rates-bonds/italy-9-year-bond-yield-historical-data"
        outputDict['ITA10Y'] = "https://www.investing.com/rates-bonds/italy-10-year-bond-yield-historical-data"
        outputDict['ITA15Y'] = "https://www.investing.com/rates-bonds/italy-15-year-bond-yield-historical-data"
        outputDict['ITA20Y'] = "https://www.investing.com/rates-bonds/italy-20-year-historical-data"
        outputDict['ITA30Y'] = "https://www.investing.com/rates-bonds/italy-30-year-historical-data"
        outputDict['ITA50Y'] = "https://www.investing.com/rates-bonds/italy-50-year-historical-data"


        return outputDict
elif OperatingMode == "JP":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['JPN1M'] = "https://www.investing.com/rates-bonds/japan-1-month-historical-data"
        outputDict['JPN3M'] = "https://www.investing.com/rates-bonds/japan-3-month-bond-yield-historical-data"
        outputDict['JPN6M'] = "https://www.investing.com/rates-bonds/japan-6-month-bond-yield-historical-data"
        outputDict['JPN9M'] = "https://www.investing.com/rates-bonds/japan-9-month-historical-data"
        outputDict['JPN1Y'] = "https://www.investing.com/rates-bonds/japan-1-year-bond-yield-historical-data"
        outputDict['JPN2Y'] = "https://www.investing.com/rates-bonds/japan-2-year-bond-yield-historical-data"
        outputDict['JPN3Y'] = "https://www.investing.com/rates-bonds/japan-3-year-bond-yield-historical-data"
        outputDict['JPN4Y'] = "https://www.investing.com/rates-bonds/japan-4-year-bond-yield-historical-data"
        outputDict['JPN5Y'] = "https://www.investing.com/rates-bonds/japan-5-year-bond-yield-historical-data"
        outputDict['JPN6Y'] = "https://www.investing.com/rates-bonds/japan-6-year-bond-yield-historical-data"
        outputDict['JPN7Y'] = "https://www.investing.com/rates-bonds/japan-7-year-bond-yield-historical-data"
        outputDict['JPN8Y'] = "https://www.investing.com/rates-bonds/japan-8-year-bond-yield-historical-data"
        outputDict['JPN9Y'] = "https://www.investing.com/rates-bonds/japan-9-year-bond-yield-historical-data"
        outputDict['JPN10Y'] = "https://www.investing.com/rates-bonds/japan-10-year-bond-yield-historical-data"
        outputDict['JPN15Y'] = "https://www.investing.com/rates-bonds/japan-15-year-bond-yield-historical-data"
        outputDict['JPN20Y'] = "https://www.investing.com/rates-bonds/japan-20-year-bond-yield-historical-data"
        outputDict['JPN30Y'] = "https://www.investing.com/rates-bonds/japan-30-year-bond-yield-historical-data"
        outputDict['JPN40Y'] = "https://www.investing.com/rates-bonds/japan-40-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "JO":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['JOR3M'] = "https://www.investing.com/rates-bonds/jordan-3-month-historical-data"
        outputDict['JOR6M'] = "https://www.investing.com/rates-bonds/jordan-6-month-historical-data"
        outputDict['JOR9M'] = "https://www.investing.com/rates-bonds/jordan-9-month-historical-data"
        outputDict['JOR1Y'] = "https://www.investing.com/rates-bonds/jordan-1-year-historical-data"
        outputDict['JOR2Y'] = "https://www.investing.com/rates-bonds/jordan-2-year-historical-data"
        outputDict['JOR3Y'] = "https://www.investing.com/rates-bonds/jordan-3-year-historical-data"
        outputDict['JOR5Y'] = "https://www.investing.com/rates-bonds/jordan-5-year-historical-data"
        outputDict['JOR7Y'] = "https://www.investing.com/rates-bonds/jordan-7-year-historical-data"
        outputDict['JOR10Y'] = "https://www.investing.com/rates-bonds/jordan-10-year-historical-data"


        return outputDict
elif OperatingMode == "KE":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['KENOvernight'] = "https://www.investing.com/rates-bonds/kenya-overnight-bond-yield-historical-data"
        outputDict['KEN3M'] = "https://www.investing.com/rates-bonds/kenya-3-month-bond-yield-historical-data"
        outputDict['KEN6M'] = "https://www.investing.com/rates-bonds/kenya-6-month-bond-yield-historical-data"
        outputDict['KEN1Y'] = "https://www.investing.com/rates-bonds/kenya-1-year-bond-yield-historical-data"
        outputDict['KEN2Y'] = "https://www.investing.com/rates-bonds/kenya-2-year-bond-yield-historical-data"
        outputDict['KEN3Y'] = "https://www.investing.com/rates-bonds/kenya-3-year-bond-yield-historical-data"
        outputDict['KEN4Y'] = "https://www.investing.com/rates-bonds/kenya-4-year-bond-yield-historical-data"
        outputDict['KEN5Y'] = "https://www.investing.com/rates-bonds/kenya-5-year-bond-yield-historical-data"
        outputDict['KEN6Y'] = "https://www.investing.com/rates-bonds/kenya-6-year-bond-yield-historical-data"
        outputDict['KEN7Y'] = "https://www.investing.com/rates-bonds/kenya-7-year-bond-yield-historical-data"
        outputDict['KEN8Y'] = "https://www.investing.com/rates-bonds/kenya-8-year-bond-yield-historical-data"
        outputDict['KEN9Y'] = "https://www.investing.com/rates-bonds/kenya-9-year-bond-yield-historical-data"
        outputDict['KEN10Y'] = "https://www.investing.com/rates-bonds/kenya-10-year-bond-yield-historical-data"
        outputDict['KEN12Y'] = "https://www.investing.com/rates-bonds/kenya-12-year-bond-yield-historical-data"
        outputDict['KEN15Y'] = "https://www.investing.com/rates-bonds/kenya-15-year-bond-yield-historical-data"
        outputDict['KEN20Y'] = "https://www.investing.com/rates-bonds/kenya-20-year-bond-yield-historical-data"
        outputDict['KEN25Y'] = "https://www.investing.com/rates-bonds/kenya-25-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "LV":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['LVA2Y'] = "https://www.investing.com/rates-bonds/latvia-2-years-bond-yield-historical-data"
        outputDict['LVA3Y'] = "https://www.investing.com/rates-bonds/latvia-3-year-historical-data"
        outputDict['LVA5Y'] = "https://www.investing.com/rates-bonds/latvia-5-years-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "LT":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['LTU3Y'] = "https://www.investing.com/rates-bonds/lithuania-3-years-bond-yield-historical-data"
        outputDict['LTU5Y'] = "https://www.investing.com/rates-bonds/lithuania-5-years-bond-yield-historical-data"
        outputDict['LTU10Y'] = "https://www.investing.com/rates-bonds/lithuania-10-years-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "MY":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['MYS3W'] = "https://www.investing.com/rates-bonds/malaysia-3-weeks-bond-yield-historical-data"
        outputDict['MYS3M'] = "https://www.investing.com/rates-bonds/malaysia-3-month-bond-yield-historical-data"
        outputDict['MYS7M'] = "https://www.investing.com/rates-bonds/malaysia-7-month-bond-yield-historical-data"
        outputDict['MYS1Y'] = "https://www.investing.com/rates-bonds/malaysia-1-year-bond-yield-historical-data"
        outputDict['MYS3Y'] = "https://www.investing.com/rates-bonds/malaysia-3-year-bond-yield-historical-data"
        outputDict['MYS5Y'] = "https://www.investing.com/rates-bonds/malaysia-5-year-bond-yield-historical-data"
        outputDict['MYS7Y'] = "https://www.investing.com/rates-bonds/malaysia-7-year-historical-data"
        outputDict['MYS10Y'] = "https://www.investing.com/rates-bonds/malaysia-10-year-bond-yield-historical-data"
        outputDict['MYS15Y'] = "https://www.investing.com/rates-bonds/malaysia-15-year-historical-data"
        outputDict['MYS20Y'] = "https://www.investing.com/rates-bonds/malaysia-20-year-bond-yield-historical-data"
        outputDict['MYS30Y'] = "https://www.investing.com/rates-bonds/malaysia-30-year-historical-data"


        return outputDict
elif OperatingMode == "MT":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['MLT1M'] = "https://www.investing.com/rates-bonds/malta-1-month-historical-data"
        outputDict['MLT3M'] = "https://www.investing.com/rates-bonds/malta-3-month-historical-data"
        outputDict['MLT6M'] = "https://www.investing.com/rates-bonds/malta-6-month-historical-data"
        outputDict['MLT1Y'] = "https://www.investing.com/rates-bonds/malta-1-year-historical-data"
        outputDict['MLT3Y'] = "https://www.investing.com/rates-bonds/malta-3-year-historical-data"
        outputDict['MLT5Y'] = "https://www.investing.com/rates-bonds/malta-5-year-historical-data"
        outputDict['MLT10Y'] = "https://www.investing.com/rates-bonds/malta-10-year-historical-data"
        outputDict['MLT20Y'] = "https://www.investing.com/rates-bonds/malta-20-year-historical-data"
        outputDict['MLT25Y'] = "https://www.investing.com/rates-bonds/malta-25-year-historical-data"


        return outputDict
elif OperatingMode == "MU":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['MUS2M'] = "https://www.investing.com/rates-bonds/mauritius-2-months-bond-yield-historical-data"
        outputDict['MUS4M'] = "https://www.investing.com/rates-bonds/mauritius-4-months-bond-yield-historical-data"
        outputDict['MUS6M'] = "https://www.investing.com/rates-bonds/mauritius-6-months-bond-yield-historical-data"
        outputDict['MUS8M'] = "https://www.investing.com/rates-bonds/mauritius-8-months-bond-yield-historical-data"
        outputDict['MUS1Y'] = "https://www.investing.com/rates-bonds/mauritius-1-year-bond-yield-historical-data"
        outputDict['MUS2Y'] = "https://www.investing.com/rates-bonds/mauritius-2-year-historical-data"
        outputDict['MUS3Y'] = "https://www.investing.com/rates-bonds/mauritius-3-year-historical-data"
        outputDict['MUS4Y'] = "https://www.investing.com/rates-bonds/mauritius-4-year-historical-data"
        outputDict['MUS5Y'] = "https://www.investing.com/rates-bonds/mauritius-5-year-historical-data"
        outputDict['MUS10Y'] = "https://www.investing.com/rates-bonds/mauritius-10-year-historical-data"
        outputDict['MUS15Y'] = "https://www.investing.com/rates-bonds/mauritius-15-year-historical-data"
        outputDict['MUS20Y'] = "https://www.investing.com/rates-bonds/mauritius-20-year-historical-data"


        return outputDict
elif OperatingMode == "MX":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['MEXOvernight'] = "https://www.investing.com/rates-bonds/mexico-overnight-historical-data"
        outputDict['MEX1M'] = "https://www.investing.com/rates-bonds/mexico-1-month-historical-data"
        outputDict['MEX3M'] = "https://www.investing.com/rates-bonds/mexico-3-month-historical-data"
        outputDict['MEX6M'] = "https://www.investing.com/rates-bonds/mexico-6-month-historical-data"
        outputDict['MEX9M'] = "https://www.investing.com/rates-bonds/mexico-9-month-historical-data"
        outputDict['MEX1Y'] = "https://www.investing.com/rates-bonds/mexico-1-year-historical-data"
        outputDict['MEX3Y'] = "https://www.investing.com/rates-bonds/mexico-3-year-historical-data"
        outputDict['MEX5Y'] = "https://www.investing.com/rates-bonds/mexico-5-year-historical-data"
        outputDict['MEX7Y'] = "https://www.investing.com/rates-bonds/mexico-7-year-historical-data"
        outputDict['MEX10Y'] = "https://www.investing.com/rates-bonds/mexico-10-year-historical-data"
        outputDict['MEX15Y'] = "https://www.investing.com/rates-bonds/mexico-18-year-historical-data"
        outputDict['MEX20Y'] = "https://www.investing.com/rates-bonds/mexico-20-year-historical-data"
        outputDict['MEX30Y'] = "https://www.investing.com/rates-bonds/mexico-30-year-historical-data"


        return outputDict
elif OperatingMode == "MA":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['MAR3M'] = "https://www.investing.com/rates-bonds/morocco-3-month-historical-data"
        outputDict['MAR6M'] = "https://www.investing.com/rates-bonds/morocco-6-month-historical-data"
        outputDict['MAR2Y'] = "https://www.investing.com/rates-bonds/morocco-2-year-historical-data"
        outputDict['MAR5Y'] = "https://www.investing.com/rates-bonds/morocco-5-year-historical-data"
        outputDict['MAR10Y'] = "https://www.investing.com/rates-bonds/morocco-10-year-historical-data"
        outputDict['MAR15Y'] = "https://www.investing.com/rates-bonds/morocco-15-year-historical-data"


        return outputDict
elif OperatingMode == "NA":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['NAM3M'] = "https://www.investing.com/rates-bonds/namibia-3-month-historical-data"
        outputDict['NAM6M'] = "https://www.investing.com/rates-bonds/namibia-6-month-historical-data"
        outputDict['NAM9M'] = "https://www.investing.com/rates-bonds/namibia-9-month-historical-data"
        outputDict['NAM1Y'] = "https://www.investing.com/rates-bonds/namibia-1-year-historical-data"
        outputDict['NAM3Y'] = "https://www.investing.com/rates-bonds/namibia-3-year-historical-data"
        outputDict['NAM7Y'] = "https://www.investing.com/rates-bonds/namibia-7-year-historical-data"
        outputDict['NAM10Y'] = "https://www.investing.com/rates-bonds/namibia-10-year-historical-data"
        outputDict['NAM15Y'] = "https://www.investing.com/rates-bonds/namibia-15-year-historical-data"
        outputDict['NAM20Y'] = "https://www.investing.com/rates-bonds/namibia-20-year-historical-data"


        return outputDict
elif OperatingMode == "NL":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['NLD1M'] = "https://www.investing.com/rates-bonds/netherlands-1-month-historical-data"
        outputDict['NLD3M'] = "https://www.investing.com/rates-bonds/netherlands-3-month-bond-yield-historical-data"
        outputDict['NLD6M'] = "https://www.investing.com/rates-bonds/netherlands-6-month-bond-yield-historical-data"
        outputDict['NLD2Y'] = "https://www.investing.com/rates-bonds/netherlands-2-year-bond-yield-historical-data"
        outputDict['NLD3Y'] = "https://www.investing.com/rates-bonds/netherlands-3-year-bond-yield-historical-data"
        outputDict['NLD4Y'] = "https://www.investing.com/rates-bonds/netherlands-4-year-bond-yield-historical-data"
        outputDict['NLD5Y'] = "https://www.investing.com/rates-bonds/netherlands-5-year-bond-yield-historical-data"
        outputDict['NLD6Y'] = "https://www.investing.com/rates-bonds/netherlands-6-year-bond-yield-historical-data"
        outputDict['NLD7Y'] = "https://www.investing.com/rates-bonds/netherlands-7-year-bond-yield-historical-data"
        outputDict['NLD8Y'] = "https://www.investing.com/rates-bonds/netherlands-8-year-bond-yield-historical-data"
        outputDict['NLD9Y'] = "https://www.investing.com/rates-bonds/netherlands-9-year-bond-yield-historical-data"
        outputDict['NLD10Y'] = "https://www.investing.com/rates-bonds/netherlands-10-year-bond-yield-historical-data"
        outputDict['NLD15Y'] = "https://www.investing.com/rates-bonds/netherlands-15-year-historical-data"
        outputDict['NLD20Y'] = "https://www.investing.com/rates-bonds/netherlands-20-year-bond-yield-historical-data"
        outputDict['NLD25Y'] = "https://www.investing.com/rates-bonds/netherlands-25-year-historical-data"
        outputDict['NLD30Y'] = "https://www.investing.com/rates-bonds/netherlands-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "NZ":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['NZL1M'] = "https://www.investing.com/rates-bonds/new-zealand-1-month-bond-yield-historical-data"
        outputDict['NZL2M'] = "https://www.investing.com/rates-bonds/new-zealand-2-months-bond-yield-historical-data"
        outputDict['NZL3M'] = "https://www.investing.com/rates-bonds/new-zealand-3-months-bond-yield-historical-data"
        outputDict['NZL4M'] = "https://www.investing.com/rates-bonds/new-zealand-4-months-bond-yield-historical-data"
        outputDict['NZL5M'] = "https://www.investing.com/rates-bonds/new-zealand-5-months-bond-yield-historical-data"
        outputDict['NZL6M'] = "https://www.investing.com/rates-bonds/new-zealand-6-months-bond-yield-historical-data"
        outputDict['NZL1Y'] = "https://www.investing.com/rates-bonds/new-zealand-1-year-historical-data"
        outputDict['NZL2Y'] = "https://www.investing.com/rates-bonds/new-zealand-2-years-bond-yield-historical-data"
        outputDict['NZL5Y'] = "https://www.investing.com/rates-bonds/new-zealand-5-years-bond-yield-historical-data"
        outputDict['NZL7Y'] = "https://www.investing.com/rates-bonds/new-zealand-7-years-bond-yield-historical-data"
        outputDict['NZL10Y'] = "https://www.investing.com/rates-bonds/new-zealand-10-years-bond-yield-historical-data"
        outputDict['NZL15Y'] = "https://www.investing.com/rates-bonds/new-zealand-15-year-historical-data"
        outputDict['NZL20Y'] = "https://www.investing.com/rates-bonds/new-zealand-20-year-historical-data"


        return outputDict
elif OperatingMode == "NG":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['NGA3M'] = "https://www.investing.com/rates-bonds/nigeria-3-month-historical-data"
        outputDict['NGA6M'] = "https://www.investing.com/rates-bonds/nigeria-6-month-historical-data"
        outputDict['NGA1Y'] = "https://www.investing.com/rates-bonds/nigeria-1-year-historical-data"
        outputDict['NGA2Y'] = "https://www.investing.com/rates-bonds/nigeria-2-year-historical-data"
        outputDict['NGA4Y'] = "https://www.investing.com/rates-bonds/nigeria-4-year-historical-data"
        outputDict['NGA5Y'] = "https://www.investing.com/rates-bonds/nigeria-5-year-historical-data"
        outputDict['NGA7Y'] = "https://www.investing.com/rates-bonds/nigeria-7-year-historical-data"
        outputDict['NGA10Y'] = "https://www.investing.com/rates-bonds/nigeria-10-year-historical-data"
        outputDict['NGA15Y'] = "https://www.investing.com/rates-bonds/nigeria-15-year-historical-data"
        outputDict['NGA20Y'] = "https://www.investing.com/rates-bonds/nigeria-20-year-historical-data"


        return outputDict
elif OperatingMode == "NO":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['NOR1M'] = "https://www.investing.com/rates-bonds/norway-1-month-bond-yield-historical-data"
        outputDict['NOR2M'] = "https://www.investing.com/rates-bonds/norway-2-month-bond-yield-historical-data"
        outputDict['NOR3M'] = "https://www.investing.com/rates-bonds/norway-3-month-bond-yield-historical-data"
        outputDict['NOR6M'] = "https://www.investing.com/rates-bonds/norway-6-month-bond-yield-historical-data"
        outputDict['NOR9M'] = "https://www.investing.com/rates-bonds/norway-9-month-bond-yield-historical-data"
        outputDict['NOR1Y'] = "https://www.investing.com/rates-bonds/norway-1-year-bond-yield-historical-data"
        outputDict['NOR3Y'] = "https://www.investing.com/rates-bonds/norway-3-year-bond-yield-historical-data"
        outputDict['NOR5Y'] = "https://www.investing.com/rates-bonds/norway-5-year-bond-yield-historical-data"
        outputDict['NOR10Y'] = "https://www.investing.com/rates-bonds/norway-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "PK":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['PAK3M'] = "https://www.investing.com/rates-bonds/pakistan-3-month-bond-yield-historical-data"
        outputDict['PAK6M'] = "https://www.investing.com/rates-bonds/pakistan-6-month-bond-yield-historical-data"
        outputDict['PAK1Y'] = "https://www.investing.com/rates-bonds/pakistan-1-year-bond-yield-historical-data"
        outputDict['PAK3Y'] = "https://www.investing.com/rates-bonds/pakistan-3-year-bond-yield-historical-data"
        outputDict['PAK5Y'] = "https://www.investing.com/rates-bonds/pakistan-5-year-bond-yield-historical-data"
        outputDict['PAK10Y'] = "https://www.investing.com/rates-bonds/pakistan-10-year-bond-yield-historical-data"
        outputDict['PAK14Y'] = "https://www.investing.com/rates-bonds/pakistan-15-year-bond-yield-historical-data"
        outputDict['PAK20Y'] = "https://www.investing.com/rates-bonds/pakistan-20-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "PE":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['PER5Y'] = "https://www.investing.com/rates-bonds/peru-5-year-bond-yield-historical-data"
        outputDict['PER9Y'] = "https://www.investing.com/rates-bonds/peru-9-year-bond-yield-historical-data"
        outputDict['PER15Y'] = "https://www.investing.com/rates-bonds/peru-15-year-bond-yield-historical-data"
        outputDict['PER20Y'] = "https://www.investing.com/rates-bonds/peru-20-year-bond-yield-historical-data"
        outputDict['PER30Y'] = "https://www.investing.com/rates-bonds/peru-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "PH":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['PHL1M'] = "https://www.investing.com/rates-bonds/philippines-1-month-bond-yield-historical-data"
        outputDict['PHL3M'] = "https://www.investing.com/rates-bonds/philippines-3-month-bond-yield-historical-data"
        outputDict['PHL6M'] = "https://www.investing.com/rates-bonds/philippines-6-month-bond-yield-historical-data"
        outputDict['PHL1Y'] = "https://www.investing.com/rates-bonds/philippines-1-year-bond-yield-historical-data"
        outputDict['PHL2Y'] = "https://www.investing.com/rates-bonds/philippines-2-year-bond-yield-historical-data"
        outputDict['PHL3Y'] = "https://www.investing.com/rates-bonds/philippines-3-year-bond-yield-historical-data"
        outputDict['PHL4Y'] = "https://www.investing.com/rates-bonds/philippines-4-year-bond-yield-historical-data"
        outputDict['PHL5Y'] = "https://www.investing.com/rates-bonds/philippines-5-year-bond-yield-historical-data"
        outputDict['PHL7Y'] = "https://www.investing.com/rates-bonds/philippines-7-year-bond-yield-historical-data"
        outputDict['PHL10Y'] = "https://www.investing.com/rates-bonds/philippines-10-year-bond-yield-historical-data"
        outputDict['PHL20Y'] = "https://www.investing.com/rates-bonds/philippines-20-year-bond-yield-historical-data"
        outputDict['PHL25Y'] = "https://www.investing.com/rates-bonds/philippines-25-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "PL":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['POLOvernight'] = "https://www.investing.com/rates-bonds/poland-overnight-rate-historical-data"
        outputDict['POL1M'] = "https://www.investing.com/rates-bonds/poland-1-month-bond-yield-historical-data"
        outputDict['POL2M'] = "https://www.investing.com/rates-bonds/poland-2-month-bond-yield-historical-data"
        outputDict['POL1Y'] = "https://www.investing.com/rates-bonds/poland-1-year-bond-yield-historical-data"
        outputDict['POL2Y'] = "https://www.investing.com/rates-bonds/poland-2-year-bond-yield-historical-data"
        outputDict['POL3Y'] = "https://www.investing.com/rates-bonds/poland-3-year-bond-yield-historical-data"
        outputDict['POL4Y'] = "https://www.investing.com/rates-bonds/poland-4-year-bond-yield-historical-data"
        outputDict['POL5Y'] = "https://www.investing.com/rates-bonds/poland-5-year-bond-yield-historical-data"
        outputDict['POL6Y'] = "https://www.investing.com/rates-bonds/poland-6-year-bond-yield-historical-data"
        outputDict['POL8Y'] = "https://www.investing.com/rates-bonds/poland-8-year-bond-yield-historical-data"
        outputDict['POL9Y'] = "https://www.investing.com/rates-bonds/poland-9-year-bond-yield-historical-data"
        outputDict['POL10Y'] = "https://www.investing.com/rates-bonds/poland-10-year-bond-yield-historical-data"
        outputDict['POL12Y'] = "https://www.investing.com/rates-bonds/poland-12-year-historical-data"


        return outputDict
elif OperatingMode == "PT":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['PRT3M'] = "https://www.investing.com/rates-bonds/portugal-3-month-historical-data"
        outputDict['PRT6M'] = "https://www.investing.com/rates-bonds/portugal-6-months-bond-yield-historical-data"
        outputDict['PRT1Y'] = "https://www.investing.com/rates-bonds/portugal-1-year-historical-data"
        outputDict['PRT2Y'] = "https://www.investing.com/rates-bonds/portugal-2-year-bond-yield-historical-data"
        outputDict['PRT3Y'] = "https://www.investing.com/rates-bonds/portugal-3-year-bond-yield-historical-data"
        outputDict['PRT4Y'] = "https://www.investing.com/rates-bonds/portugal-4-year-bond-yield-historical-data"
        outputDict['PRT5Y'] = "https://www.investing.com/rates-bonds/portugal-5-year-bond-yield-historical-data"
        outputDict['PRT6Y'] = "https://www.investing.com/rates-bonds/portugal-6-year-bond-yield-historical-data"
        outputDict['PRT7Y'] = "https://www.investing.com/rates-bonds/portugal-7-year-bond-yield-historical-data"
        outputDict['PRT8Y'] = "https://www.investing.com/rates-bonds/portugal-8-year-bond-yield-historical-data"
        outputDict['PRT9Y'] = "https://www.investing.com/rates-bonds/portugal-9-year-bond-yield-historical-data"
        outputDict['PRT10Y'] = "https://www.investing.com/rates-bonds/portugal-10-year-bond-yield-historical-data"
        outputDict['PRT15Y'] = "https://www.investing.com/rates-bonds/portugal-15-year-bond-yield-historical-data"
        outputDict['PRT20Y'] = "https://www.investing.com/rates-bonds/portugal-30-year-bond-yield-historical-data"
        outputDict['PRT30Y'] = "https://www.investing.com/rates-bonds/portugal-30-year-historical-data"


        return outputDict
elif OperatingMode == "QA":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['QAT5Y'] = "https://www.investing.com/rates-bonds/qatar-5-year-bond-yield-historical-data"
        outputDict['QAT10Y'] = "https://www.investing.com/rates-bonds/qatar-10-year-bond-yield-historical-data"
        outputDict['QAT15Y'] = "https://www.investing.com/rates-bonds/qatar-20-year-bond-yield-historical-data"
        outputDict['QAT30Y'] = "https://www.investing.com/rates-bonds/qatar-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "RO":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ROU6M'] = "https://www.investing.com/rates-bonds/romania-6-month-bond-yield-historical-data"
        outputDict['ROU1Y'] = "https://www.investing.com/rates-bonds/romania-1-year-bond-yield-historical-data"
        outputDict['ROU2Y'] = "https://www.investing.com/rates-bonds/romania-2-year-historical-data"
        outputDict['ROU3Y'] = "https://www.investing.com/rates-bonds/romania-3-year-bond-yield-historical-data"
        outputDict['ROU4Y'] = "https://www.investing.com/rates-bonds/romania-4-year-historical-data"
        outputDict['ROU5Y'] = "https://www.investing.com/rates-bonds/romania-5-year-bond-yield-historical-data"
        outputDict['ROU7Y'] = "https://www.investing.com/rates-bonds/romania-7-year-historical-data"
        outputDict['ROU10Y'] = "https://www.investing.com/rates-bonds/romania-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "RU":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['RUSOvernight'] = "https://www.investing.com/rates-bonds/russia-overnight-rate-historical-data"
        outputDict['RUS1W'] = "https://www.investing.com/rates-bonds/russia-1-week-bond-yield-historical-data"
        outputDict['RUS2W'] = "https://www.investing.com/rates-bonds/russia-2-week-bond-yield-historical-data"
        outputDict['RUS1M'] = "https://www.investing.com/rates-bonds/russia-1-month-bond-yield-historical-data"
        outputDict['RUS2M'] = "https://www.investing.com/rates-bonds/russia-2-month-bond-yield-historical-data"
        outputDict['RUS3M'] = "https://www.investing.com/rates-bonds/russia-3-month-bond-yield-historical-data"
        outputDict['RUS6M'] = "https://www.investing.com/rates-bonds/russia-6-month-bond-yield-historical-data"
        outputDict['RUS1Y'] = "https://www.investing.com/rates-bonds/russia-1-year-bond-yield-historical-data"
        outputDict['RUS2Y'] = "https://www.investing.com/rates-bonds/russia-2-year-bond-yield-historical-data"
        outputDict['RUS3Y'] = "https://www.investing.com/rates-bonds/russia-3-year-bond-yield-historical-data"
        outputDict['RUS5Y'] = "https://www.investing.com/rates-bonds/russia-5-year-bond-yield-historical-data"
        outputDict['RUS7Y'] = "https://www.investing.com/rates-bonds/russia-7-year-historical-data"
        outputDict['RUS10Y'] = "https://www.investing.com/rates-bonds/russia-10-year-bond-yield-historical-data"
        outputDict['RUS15Y'] = "https://www.investing.com/rates-bonds/russia-15-year-bond-yield-historical-data"
        outputDict['RUS20Y'] = "https://www.investing.com/rates-bonds/russia-25-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "RS":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['SRB1Y'] = "https://www.investing.com/rates-bonds/serbia-1-year-historical-data"
        outputDict['SRB2Y'] = "https://www.investing.com/rates-bonds/serbia-2-year-historical-data"
        outputDict['SRB4Y'] = "https://www.investing.com/rates-bonds/serbia-4-year-historical-data"
        outputDict['SRB5Y'] = "https://www.investing.com/rates-bonds/serbia-5-year-historical-data"
        outputDict['SRB6Y'] = "https://www.investing.com/rates-bonds/serbia-6-year-historical-data"
        outputDict['SRB7Y'] = "https://www.investing.com/rates-bonds/serbia-7-year-historical-data"


        return outputDict
elif OperatingMode == "SG":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['SGP1M'] = "https://www.investing.com/rates-bonds/singapore-1-month-bond-yield-historical-data"
        outputDict['SGP3M'] = "https://www.investing.com/rates-bonds/singapore-3-month-bond-yield-historical-data"
        outputDict['SGP6M'] = "https://www.investing.com/rates-bonds/singapore-6-month-historical-data"
        outputDict['SGP1Y'] = "https://www.investing.com/rates-bonds/singapore-1-year-bond-yield-historical-data"
        outputDict['SGP2Y'] = "https://www.investing.com/rates-bonds/singapore-2-year-bond-yield-historical-data"
        outputDict['SGP5Y'] = "https://www.investing.com/rates-bonds/singapore-5-year-bond-yield-historical-data"
        outputDict['SGP10Y'] = "https://www.investing.com/rates-bonds/singapore-10-year-bond-yield-historical-data"
        outputDict['SGP15Y'] = "https://www.investing.com/rates-bonds/singapore-15-year-bond-yield-historical-data"
        outputDict['SGP20Y'] = "https://www.investing.com/rates-bonds/singapore-20-year-bond-yield-historical-data"
        outputDict['SGP30Y'] = "https://www.investing.com/rates-bonds/singapore-30-year-historical-data"


        return outputDict
elif OperatingMode == "SK":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['SVK1Y'] = "https://www.investing.com/rates-bonds/slovakia-1-year-bond-yield-historical-data"
        outputDict['SVK2Y'] = "https://www.investing.com/rates-bonds/slovakia-2-year-bond-yield-historical-data"
        outputDict['SVK3Y'] = "https://www.investing.com/rates-bonds/slovakia-3-year-historical-data"
        outputDict['SVK5Y'] = "https://www.investing.com/rates-bonds/slovakia-5-year-bond-yield-historical-data"
        outputDict['SVK6Y'] = "https://www.investing.com/rates-bonds/slovakia-6-year-historical-data"
        outputDict['SVK7Y'] = "https://www.investing.com/rates-bonds/slovakia-7-year-bond-yield-historical-data"
        outputDict['SVK8Y'] = "https://www.investing.com/rates-bonds/slovakia-8-year-bond-yield-historical-data"
        outputDict['SVK9Y'] = "https://www.investing.com/rates-bonds/slovakia-9-year-historical-data"
        outputDict['SVK10Y'] = "https://www.investing.com/rates-bonds/slovakia-10-year-historical-data"
        outputDict['SVK12Y'] = "https://www.investing.com/rates-bonds/slovakia-12-year-historical-data"
        outputDict['SVK14Y'] = "https://www.investing.com/rates-bonds/slovakia-14-year-bond-yield-historical-data"
        outputDict['SVK20Y'] = "https://www.investing.com/rates-bonds/slovakia-20-year-historical-data"


        return outputDict
elif OperatingMode == "SI":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['SVN1Y'] = "https://www.investing.com/rates-bonds/slovenia-1-year-historical-data"
        outputDict['SVN2Y'] = "https://www.investing.com/rates-bonds/slovenia-2-year-bond-yield-historical-data"
        outputDict['SVN5Y'] = "https://www.investing.com/rates-bonds/slovenia-5-year-bond-yield-historical-data"
        outputDict['SVN7Y'] = "https://www.investing.com/rates-bonds/slovenia-7-year-historical-data"
        outputDict['SVN9Y'] = "https://www.investing.com/rates-bonds/slovenia-9-year-historical-data"
        outputDict['SVN10Y'] = "https://www.investing.com/rates-bonds/slovenia-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "ZA":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ZAF3M'] = "https://www.investing.com/rates-bonds/south-africa-3-month-bond-yield-historical-data"
        outputDict['ZAF2Y'] = "https://www.investing.com/rates-bonds/south-africa-2-year-historical-data"
        outputDict['ZAF3Y'] = "https://www.investing.com/rates-bonds/south-africa-3-year-bond-yield-historical-data"
        outputDict['ZAF5Y'] = "https://www.investing.com/rates-bonds/south-africa-5-year-bond-yield-historical-data"
        outputDict['ZAF6Y'] = "https://www.investing.com/rates-bonds/south-africa-6-year-historical-data"
        outputDict['ZAF10Y'] = "https://www.investing.com/rates-bonds/south-africa-10-year-bond-yield-historical-data"
        outputDict['ZAF15Y'] = "https://www.investing.com/rates-bonds/south-africa-15-year-bond-yield-historical-data"
        outputDict['ZAF20Y'] = "https://www.investing.com/rates-bonds/south-africa-20-year-bond-yield-historical-data"
        outputDict['ZAF25Y'] = "https://www.investing.com/rates-bonds/south-africa-25-year-historical-data"
        outputDict['ZAF30Y'] = "https://www.investing.com/rates-bonds/south-africa-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "KR":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['KOR1Y'] = "https://www.investing.com/rates-bonds/south-korea-1-year-bond-yield-historical-data"
        outputDict['KOR2Y'] = "https://www.investing.com/rates-bonds/south-korea-2-year-bond-yield-historical-data"
        outputDict['KOR3Y'] = "https://www.investing.com/rates-bonds/south-korea-3-year-bond-yield-historical-data"
        outputDict['KOR4Y'] = "https://www.investing.com/rates-bonds/south-korea-4-year-bond-yield-historical-data"
        outputDict['KOR5Y'] = "https://www.investing.com/rates-bonds/south-korea-5-year-bond-yield-historical-data"
        outputDict['KOR10Y'] = "https://www.investing.com/rates-bonds/south-korea-10-year-bond-yield-historical-data"
        outputDict['KOR20Y'] = "https://www.investing.com/rates-bonds/south-korea-20-year-bond-yield-historical-data"
        outputDict['KOR30Y'] = "https://www.investing.com/rates-bonds/south-korea-30-year-historical-data"
        outputDict['KOR50Y'] = "https://www.investing.com/rates-bonds/south-korea-50-year-historical-data"


        return outputDict
elif OperatingMode == "ES":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['ESP1M'] = "https://www.investing.com/rates-bonds/spain-1-month-historical-data"
        outputDict['ESP3M'] = "https://www.investing.com/rates-bonds/spain-3-month-bond-yield-historical-data"
        outputDict['ESP6M'] = "https://www.investing.com/rates-bonds/spain-6-month-bond-yield-historical-data"
        outputDict['ESP9M'] = "https://www.investing.com/rates-bonds/spain-9-month-historical-data"
        outputDict['ESP1Y'] = "https://www.investing.com/rates-bonds/spain-1-year-bond-yield-historical-data"
        outputDict['ESP2Y'] = "https://www.investing.com/rates-bonds/spain-2-year-bond-yield-historical-data"
        outputDict['ESP3Y'] = "https://www.investing.com/rates-bonds/spain-3-year-bond-yield-historical-data"
        outputDict['ESP4Y'] = "https://www.investing.com/rates-bonds/spain-4-year-bond-yield-historical-data"
        outputDict['ESP5Y'] = "https://www.investing.com/rates-bonds/spain-5-year-bond-yield-historical-data"
        outputDict['ESP6Y'] = "https://www.investing.com/rates-bonds/spain-6-year-bond-yield-historical-data"
        outputDict['ESP7Y'] = "https://www.investing.com/rates-bonds/spain-7-year-bond-yield-historical-data"
        outputDict['ESP8Y'] = "https://www.investing.com/rates-bonds/spain-8-year-bond-yield-historical-data"
        outputDict['ESP9Y'] = "https://www.investing.com/rates-bonds/spain-9-year-bond-yield-historical-data"
        outputDict['ESP10Y'] = "https://www.investing.com/rates-bonds/spain-10-year-bond-yield-historical-data"
        outputDict['ESP15Y'] = "https://www.investing.com/rates-bonds/spain-15-year-bond-yield-historical-data"
        outputDict['ESP20Y'] = "https://www.investing.com/rates-bonds/spain-20-year-bond-yield-historical-data"
        outputDict['ESP25Y'] = "https://www.investing.com/rates-bonds/spain-25-year-historical-data"
        outputDict['ESP30Y'] = "https://www.investing.com/rates-bonds/spain-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "LK":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['LKA3M'] = "https://www.investing.com/rates-bonds/sri-lanka-3-month-bond-yield-historical-data"
        outputDict['LKA6M'] = "https://www.investing.com/rates-bonds/sri-lanka-6-month-bond-yield-historical-data"
        outputDict['LKA1Y'] = "https://www.investing.com/rates-bonds/sri-lanka-1-year-bond-yield-historical-data"
        outputDict['LKA2Y'] = "https://www.investing.com/rates-bonds/sri-lanka-2-year-bond-yield-historical-data"
        outputDict['LKA3Y'] = "https://www.investing.com/rates-bonds/sri-lanka-3-year-bond-yield-historical-data"
        outputDict['LKA4Y'] = "https://www.investing.com/rates-bonds/sri-lanka-4-year-bond-yield-historical-data"
        outputDict['LKA5Y'] = "https://www.investing.com/rates-bonds/sri-lanka-5-year-bond-yield-historical-data"
        outputDict['LKA6Y'] = "https://www.investing.com/rates-bonds/sri-lanka-6-year-historical-data"
        outputDict['LKA7Y'] = "https://www.investing.com/rates-bonds/sri-lanka-7-year-historical-data"
        outputDict['LKA8Y'] = "https://www.investing.com/rates-bonds/sri-lanka-8-year-historical-data"
        outputDict['LKA9Y'] = "https://www.investing.com/rates-bonds/sri-lanka-9-year-historical-data"
        outputDict['LKA10Y'] = "https://www.investing.com/rates-bonds/sri-lanka-10-year-historical-data"
        outputDict['LKA15Y'] = "https://www.investing.com/rates-bonds/sri-lanka-15-year-historical-data"


        return outputDict
elif OperatingMode == "SE":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['SWE1M'] = "https://www.investing.com/rates-bonds/sweden-1-month-bond-yield-historical-data"
        outputDict['SWE2M'] = "https://www.investing.com/rates-bonds/sweden-2-month-bond-yield-historical-data"
        outputDict['SWE3M'] = "https://www.investing.com/rates-bonds/sweden-3-month-bond-yield-historical-data"
        outputDict['SWE6M'] = "https://www.investing.com/rates-bonds/sweden-6-month-bond-yield-historical-data"
        outputDict['SWE2Y'] = "https://www.investing.com/rates-bonds/sweden-2-year-bond-yield-historical-data"
        outputDict['SWE5Y'] = "https://www.investing.com/rates-bonds/sweden-5-year-bond-yield-historical-data"
        outputDict['SWE7Y'] = "https://www.investing.com/rates-bonds/sweden-7-year-historical-data"
        outputDict['SWE10Y'] = "https://www.investing.com/rates-bonds/sweden-10-year-bond-yield-historical-data"
        outputDict['SWE15Y'] = "https://www.investing.com/rates-bonds/sweden-15-year-historical-data"
        outputDict['SWE20Y'] = "https://www.investing.com/rates-bonds/sweden-6-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "CH":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['CHEOvernight'] = "https://www.investing.com/rates-bonds/switzerland-overnight-rate-historical-data"
        outputDict['CHE1W'] = "https://www.investing.com/rates-bonds/switzerland-1-week-bond-yield-historical-data"
        outputDict['CHE1M'] = "https://www.investing.com/rates-bonds/switzerland-1-month-bond-yield-historical-data"
        outputDict['CHE2M'] = "https://www.investing.com/rates-bonds/switzerland-2-month-bond-yield-historical-data"
        outputDict['CHE3M'] = "https://www.investing.com/rates-bonds/switzerland-3-month-bond-yield-historical-data"
        outputDict['CHE6M'] = "https://www.investing.com/rates-bonds/switzerland-6-month-bond-yield-historical-data"
        outputDict['CHE1Y'] = "https://www.investing.com/rates-bonds/switzerland-1-year-bond-yield-historical-data"
        outputDict['CHE2Y'] = "https://www.investing.com/rates-bonds/switzerland-2-year-bond-yield-historical-data"
        outputDict['CHE3Y'] = "https://www.investing.com/rates-bonds/switzerland-3-year-bond-yield-historical-data"
        outputDict['CHE4Y'] = "https://www.investing.com/rates-bonds/switzerland-4-year-bond-yield-historical-data"
        outputDict['CHE5Y'] = "https://www.investing.com/rates-bonds/switzerland-5-year-bond-yield-historical-data"
        outputDict['CHE6Y'] = "https://www.investing.com/rates-bonds/switzerland-6-year-bond-yield-historical-data"
        outputDict['CHE7Y'] = "https://www.investing.com/rates-bonds/switzerland-7-year-bond-yield-historical-data"
        outputDict['CHE8Y'] = "https://www.investing.com/rates-bonds/switzerland-8-year-bond-yield-historical-data"
        outputDict['CHE9Y'] = "https://www.investing.com/rates-bonds/switzerland-9-year-bond-yield-historical-data"
        outputDict['CHE10Y'] = "https://www.investing.com/rates-bonds/switzerland-10-year-bond-yield-historical-data"
        outputDict['CHE15Y'] = "https://www.investing.com/rates-bonds/switzerland-15-year-bond-yield-historical-data"
        outputDict['CHE20Y'] = "https://www.investing.com/rates-bonds/switzerland-20-year-bond-yield-historical-data"
        outputDict['CHE30Y'] = "https://www.investing.com/rates-bonds/switzerland-30-year-bond-yield-historical-data"
        outputDict['CHE50Y'] = "https://www.investing.com/rates-bonds/switzerland-50-year-historical-data"


        return outputDict
elif OperatingMode == "TW":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['TWN2Y'] = "https://www.investing.com/rates-bonds/taiwan-2-year-bond-yield-historical-data"
        outputDict['TWN5Y'] = "https://www.investing.com/rates-bonds/taiwan-5-year-bond-yield-historical-data"
        outputDict['TWN10Y'] = "https://www.investing.com/rates-bonds/taiwan-10-year-bond-yield-historical-data"
        outputDict['TWN20Y'] = "https://www.investing.com/rates-bonds/taiwan-20-year-bond-yield-historical-data"
        outputDict['TWN30Y'] = "https://www.investing.com/rates-bonds/taiwan-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "TH":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['THA1Y'] = "https://www.investing.com/rates-bonds/thailand-1-year-bond-yield-historical-data"
        outputDict['THA2Y'] = "https://www.investing.com/rates-bonds/thailand-2-year-bond-yield-historical-data"
        outputDict['THA3Y'] = "https://www.investing.com/rates-bonds/thailand-3-year-historical-data"
        outputDict['THA5Y'] = "https://www.investing.com/rates-bonds/thailand-5-year-bond-yield-historical-data"
        outputDict['THA7Y'] = "https://www.investing.com/rates-bonds/thailand-7-year-bond-yield-historical-data"
        outputDict['THA10Y'] = "https://www.investing.com/rates-bonds/thailand-10-year-bond-yield-historical-data"
        outputDict['THA12Y'] = "https://www.investing.com/rates-bonds/thailand-12-year-bond-yield-historical-data"
        outputDict['THA14Y'] = "https://www.investing.com/rates-bonds/thailand-14-year-bond-yield-historical-data"
        outputDict['THA15Y'] = "https://www.investing.com/rates-bonds/thailand-15-year-historical-data"
        outputDict['THA16Y'] = "https://www.investing.com/rates-bonds/thailand-16-year-bond-yield-historical-data"
        outputDict['THA20Y'] = "https://www.investing.com/rates-bonds/thailand-20-year-historical-data"


        return outputDict
elif OperatingMode == "TR":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['TUR1Y'] = "https://www.investing.com/rates-bonds/turkey-1-year-bond-yield-historical-data"
        outputDict['TUR2Y'] = "https://www.investing.com/rates-bonds/turkey-2-year-bond-yield-historical-data"
        outputDict['TUR3Y'] = "https://www.investing.com/rates-bonds/turkey-3-year-bond-yield-historical-data"
        outputDict['TUR5Y'] = "https://www.investing.com/rates-bonds/turkey-5-year-bond-yield-historical-data"
        outputDict['TUR10Y'] = "https://www.investing.com/rates-bonds/turkey-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "UG":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['UGA3M'] = "https://www.investing.com/rates-bonds/uganda-3-months-bond-yield-historical-data"
        outputDict['UGA6M'] = "https://www.investing.com/rates-bonds/uganda-6-months-bond-yield-historical-data"
        outputDict['UGA1Y'] = "https://www.investing.com/rates-bonds/uganda-1-year-bond-yield-historical-data"
        outputDict['UGA2Y'] = "https://www.investing.com/rates-bonds/uganda-2-years-bond-yield-historical-data"
        outputDict['UGA3Y'] = "https://www.investing.com/rates-bonds/uganda-3-years-bond-yield-historical-data"
        outputDict['UGA4Y'] = "https://www.investing.com/rates-bonds/uganda-4-years-bond-yield-historical-data"
        outputDict['UGA5Y'] = "https://www.investing.com/rates-bonds/uganda-5-years-bond-yield-historical-data"
        outputDict['UGA10Y'] = "https://www.investing.com/rates-bonds/uganda-10-years-bond-yield-historical-data"
        outputDict['UGA15Y'] = "https://www.investing.com/rates-bonds/uganda-15-year-historical-data"


        return outputDict
elif OperatingMode == "UA":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['UKR1Y'] = "https://www.investing.com/rates-bonds/ukraine-1-year-bond-yield-historical-data"
        outputDict['UKR2Y'] = "https://www.investing.com/rates-bonds/ukraine-2-year-bond-yield-historical-data"
        outputDict['UKR3Y'] = "https://www.investing.com/rates-bonds/ukraine-3-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "GB":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['GBR1M'] = "https://www.investing.com/rates-bonds/uk-1-month-bond-yield-historical-data"
        outputDict['GBR3M'] = "https://www.investing.com/rates-bonds/uk-3-month-bond-yield-historical-data"
        outputDict['GBR6M'] = "https://www.investing.com/rates-bonds/uk-6-month-bond-yield-historical-data"
        outputDict['GBR1Y'] = "https://www.investing.com/rates-bonds/uk-1-year-bond-yield-historical-data"
        outputDict['GBR2Y'] = "https://www.investing.com/rates-bonds/uk-2-year-bond-yield-historical-data"
        outputDict['GBR3Y'] = "https://www.investing.com/rates-bonds/uk-3-year-bond-yield-historical-data"
        outputDict['GBR4Y'] = "https://www.investing.com/rates-bonds/uk-4-year-bond-yield-historical-data"
        outputDict['GBR5Y'] = "https://www.investing.com/rates-bonds/uk-5-year-bond-yield-historical-data"
        outputDict['GBR6Y'] = "https://www.investing.com/rates-bonds/uk-6-year-bond-yield-historical-data"
        outputDict['GBR7Y'] = "https://www.investing.com/rates-bonds/uk-7-year-bond-yield-historical-data"
        outputDict['GBR8Y'] = "https://www.investing.com/rates-bonds/uk-8-year-bond-yield-historical-data"
        outputDict['GBR9Y'] = "https://www.investing.com/rates-bonds/uk-9-year-bond-yield-historical-data"
        outputDict['GBR10Y'] = "https://www.investing.com/rates-bonds/uk-10-year-bond-yield-historical-data"
        outputDict['GBR12Y'] = "https://www.investing.com/rates-bonds/uk-12-year-historical-data"
        outputDict['GBR15Y'] = "https://www.investing.com/rates-bonds/uk-15-year-bond-yield-historical-data"
        outputDict['GBR20Y'] = "https://www.investing.com/rates-bonds/uk-20-year-bond-yield-historical-data"
        outputDict['GBR25Y'] = "https://www.investing.com/rates-bonds/uk-25-year-bond-yield-historical-data"
        outputDict['GBR30Y'] = "https://www.investing.com/rates-bonds/uk-30-year-bond-yield-historical-data"
        outputDict['GBR40Y'] = "https://www.investing.com/rates-bonds/uk-40-year-bond-yield-historical-data"
        outputDict['GBR50Y'] = "https://www.investing.com/rates-bonds/uk-50-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "US":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['USA1M'] = "https://www.investing.com/rates-bonds/u.s.-1-month-bond-yield-historical-data"
        outputDict['USA3M'] = "https://www.investing.com/rates-bonds/u.s.-3-month-bond-yield-historical-data"
        outputDict['USA6M'] = "https://www.investing.com/rates-bonds/u.s.-6-month-bond-yield-historical-data"
        outputDict['USA1Y'] = "https://www.investing.com/rates-bonds/u.s.-1-year-bond-yield-historical-data"
        outputDict['USA2Y'] = "https://www.investing.com/rates-bonds/u.s.-2-year-bond-yield-historical-data"
        outputDict['USA3Y'] = "https://www.investing.com/rates-bonds/u.s.-3-year-bond-yield-historical-data"
        outputDict['USA5Y'] = "https://www.investing.com/rates-bonds/u.s.-5-year-bond-yield-historical-data"
        outputDict['USA7Y'] = "https://www.investing.com/rates-bonds/u.s.-7-year-bond-yield-historical-data"
        outputDict['USA10Y'] = "https://www.investing.com/rates-bonds/u.s.-10-year-bond-yield-historical-data"
        outputDict['USA30Y'] = "https://www.investing.com/rates-bonds/u.s.-30-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "VE":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['VEN2Y'] = "https://www.investing.com/rates-bonds/venezuela-2-year-bond-yield-historical-data"
        outputDict['VEN5Y'] = "https://www.investing.com/rates-bonds/venezuela-4-year-bond-yield-historical-data"
        outputDict['VEN15Y'] = "https://www.investing.com/rates-bonds/venezuela-15-year-bond-yield-historical-data"
        outputDict['VEN20Y'] = "https://www.investing.com/rates-bonds/venezuela-20-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "VN":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        outputDict['VNM1Y'] = "https://www.investing.com/rates-bonds/vietnam-1-year-bond-yield-historical-data"
        outputDict['VNM2Y'] = "https://www.investing.com/rates-bonds/vietnam-2-year-bond-yield-historical-data"
        outputDict['VNM3Y'] = "https://www.investing.com/rates-bonds/vietnam-3-year-bond-yield-historical-data"
        outputDict['VNM5Y'] = "https://www.investing.com/rates-bonds/vietnam-5-year-bond-yield-historical-data"
        outputDict['VNM7Y'] = "https://www.investing.com/rates-bonds/vietnam-7-year-bond-yield-historical-data"
        outputDict['VNM10Y'] = "https://www.investing.com/rates-bonds/vietnam-10-year-bond-yield-historical-data"


        return outputDict
elif OperatingMode == "Indices":
    def GetURLMap():
        #Instantiate OutputDictionary
        outputDict = {}
        #Add URLS to outputDictionary where Key=filename, value=url
        #Names of instruments go here
        # United States -----------------------------------------------------------------
        outputDict['DJIA'] = "https://www.investing.com/indices/us-30-historical-data"
        outputDict['SPX'] = "https://www.investing.com/indices/us-spx-500-historical-data"
        outputDict['IXIC'] = "https://www.investing.com/indices/nasdaq-composite-historical-data"
        outputDict['RUT'] = "https://www.investing.com/indices/smallcap-2000-historical-data"
        outputDict['VIX'] = "https://www.investing.com/indices/volatility-s-p-500-historical-data"
        # Canada -------------------------------------------------------------------------
        outputDict['GSPTSE'] = "https://www.investing.com/indices/s-p-tsx-composite-historical-data"
        # Brazil -------------------------------------------------------------------------
        outputDict['BVSP'] = "https://www.investing.com/indices/bovespa-historical-data"
        # Mexico -------------------------------------------------------------------------
        outputDict['MXX'] = "https://www.investing.com/indices/ipc-historical-data"
        # Germany ------------------------------------------------------------------------
        outputDict['GDAXI'] = "https://www.investing.com/indices/germany-30-historical-data"
        # United Kingdom -----------------------------------------------------------------
        outputDict['FTSE'] = "https://www.investing.com/indices/uk-100-historical-data"
        # France -------------------------------------------------------------------------
        outputDict['FCHI'] = "https://www.investing.com/indices/france-40-historical-data"
        # Europe -------------------------------------------------------------------------
        outputDict['STOXX50E'] = "https://www.investing.com/indices/eu-stoxx50-historical-data"
        # Netherlands --------------------------------------------------------------------
        outputDict['AEX'] = "https://www.investing.com/indices/netherlands-25-historical-data"
        # Spain --------------------------------------------------------------------------
        outputDict['IBEX'] = "https://www.investing.com/indices/spain-35-historical-data"
        # Italy --------------------------------------------------------------------------
        outputDict['FTSEMIB'] = "https://www.investing.com/indices/it-mib-40-historical-data"
        # Switzerland --------------------------------------------------------------------
        outputDict['SSMI'] = "https://www.investing.com/indices/switzerland-20-historical-data"
        # Portugal -----------------------------------------------------------------------
        outputDict['PSI20'] = "https://www.investing.com/indices/psi-20-historical-data"
        # Belgium ------------------------------------------------------------------------
        outputDict['BFX'] = "https://www.investing.com/indices/bel-20-historical-data"
        # Austria ------------------------------------------------------------------------
        outputDict['ATX'] = "https://www.investing.com/indices/atx-historical-data"
        # Sweden -------------------------------------------------------------------------
        outputDict['OMX'] = "https://www.investing.com/indices/omx-stockholm-30-historical-data"
        # Denmark ------------------------------------------------------------------------
        outputDict['OMXC25'] = "https://www.investing.com/indices/omx-copenhagen-25-historical-data"
        # Russia -------------------------------------------------------------------------
        outputDict['MOEX'] = "https://www.investing.com/indices/mcx-historical-data"
        outputDict['RTSI'] = "https://www.investing.com/indices/rtsi-historical-data"
        # Poland -------------------------------------------------------------------------
        outputDict['WIG20'] = "https://www.investing.com/indices/wig-20-historical-data"
        # Hungary ------------------------------------------------------------------------
        outputDict['BUX'] = "https://www.investing.com/indices/hungary-stock-market-historical-data"
        # Turkey -------------------------------------------------------------------------
        outputDict['XU100'] = "https://www.investing.com/indices/ise-100-historical-data"
        # Israel -------------------------------------------------------------------------
        outputDict['TA35'] = "https://www.investing.com/indices/ta25-historical-data"
        # Saudi Arabia -------------------------------------------------------------------
        outputDict['SASEIDX'] = "https://www.investing.com/indices/tasi-historical-data"
        # Japan --------------------------------------------------------------------------
        outputDict['NKY'] = "https://www.investing.com/indices/japan-ni225-historical-data"
        # Australia ----------------------------------------------------------------------
        outputDict['AS51'] = "https://www.investing.com/indices/aus-200-historical-data"
        # New Zealand --------------------------------------------------------------------
        outputDict['NZDOW'] = "https://www.investing.com/indices/dow-jones-new-zealand-historical-data"
        # China --------------------------------------------------------------------------
        outputDict['SHCOMP'] = "https://www.investing.com/indices/shanghai-composite-historical-data"
        outputDict['SICOM'] = "https://www.investing.com/indices/szse-component-historical-data"
        outputDict['TXIN9'] = "https://www.investing.com/indices/ftse-china-a50-historical-data"
        outputDict['DJSH'] = "https://www.investing.com/indices/dj-shanghai-historical-data"
        # Hong Kong ----------------------------------------------------------------------
        outputDict['HSI'] = "https://www.investing.com/indices/hang-sen-40-historical-data"
        # Taiwan -------------------------------------------------------------------------
        outputDict['TWSE'] = "https://www.investing.com/indices/taiwan-weighted-historical-data"
        # Thailand -----------------------------------------------------------------------
        outputDict['SET'] = "https://www.investing.com/indices/thailand-set-historical-data"
        # Korea --------------------------------------------------------------------------
        outputDict['KOSPI'] = "https://www.investing.com/indices/kospi-historical-data"
        # Indonesia ----------------------------------------------------------------------
        outputDict['JCI'] = "https://www.investing.com/indices/idx-composite-historical-data"
        # India --------------------------------------------------------------------------
        outputDict['NIFTY'] = "https://www.investing.com/indices/s-p-cnx-nifty-historical-data"
        outputDict['SENSEX'] = "https://www.investing.com/indices/sensex-historical-data"
        # Philippines --------------------------------------------------------------------
        outputDict['PCOMP'] = "https://www.investing.com/indices/psei-composite-historical-data"
        # Singapore ----------------------------------------------------------------------
        outputDict['FSSTI'] = "https://www.investing.com/indices/singapore-straits-time-historical-data"
        # Pakistan -----------------------------------------------------------------------
        outputDict['KSE100'] = "https://www.investing.com/indices/karachi-100-historical-data"
        # Vietnam ------------------------------------------------------------------------
        outputDict['HNX30'] = "https://www.investing.com/indices/hnx-30-historical-data"
        # Sri Lanka ----------------------------------------------------------------------
        outputDict['CSEALL'] = "https://www.investing.com/indices/cse-all-share-historical-data"
        # --------------------------------------------------------------------------------


        return outputDict
#-------------------------------------------------------------------------------
# GetHistoricalData: Step 4
#-------------------------------------------------------------------------------
def GetHistoricalData(browser, url, startDateString, endDateString):
    #Navigate to Page
    browser.get(url)
    #Wait sleeptime seconds for page to load
    time.sleep(sleeptime)

    #Get Date Range Element
    dateRange = browser.find_element_by_id('widgetFieldDateRange')
    #Click Date Range Element
    dateRange.click()
    #Wait sleeptime seconds for popup to show
    time.sleep(sleeptime)

    #Get StartDate Element
    startDate = browser.find_element_by_id('startDate')
    #Clear StartDate
    startDate.clear()
    #Send startDateString
    startDate.send_keys(startDateString)
    #Wait sleeptime seconds to finish sending keys
    time.sleep(sleeptime)

    #Get EndDate Element
    endDate = browser.find_element_by_id('endDate')
    #Clear EndDate
    endDate.clear()
    #Send endDateString
    endDate.send_keys(endDateString)
    #Wait sleeptime seconds to finish sending keys
    time.sleep(sleeptime)

    #Get Apply Button
    applyBTN = browser.find_element_by_id('applyBtn')
    #Click Apply Button
    applyBTN.click()
    #Wait 2 seconds for processing
    time.sleep(sleeptime)

    #Get Download data button
    downloadData = browser.find_element_by_css_selector('#column-content > .float_lang_base_2 > .float_lang_base_2 > a')
    #Click download Data Button
    downloadData.click()
    #Wait 5 seconds for file to download
    time.sleep(5)
    return True
#-------------------------------------------------------------------------------
# RenameLatestFile: Step 5: Uses GetFiles and renames newest file
#-------------------------------------------------------------------------------
def RenameLatestFile(path, newFilename):
    latest_file = max(GetFiles(path), key=os.path.getmtime)
    #Get Path to new file
    newPath = os.path.join(path, newFilename)
    #Rename File
    os.rename(latest_file,newPath)
    #Notify User
    print('Renamed: ' + latest_file)
    print("To: " + newPath)
    return True
#-------------------------------------------------------------------------------
# GetFiles: Step 6: Creates Generator Object for iterating through only once
#-------------------------------------------------------------------------------
def GetFiles(path):
    for cur_path, dirnames, filenames in os.walk(path):
        for filename in filenames:
            yield os.path.join(cur_path,filename)
#-------------------------------------------------------------------------------
# Standard boilerplate to call the main() function to begin the program.
#-------------------------------------------------------------------------------
if __name__ == '__main__':
  main()
  sys.exit(0)
#-------------------------------------------------------------------------------
