import csv, sys, locale, os, calendar
from string import Template
from datetime import date


delim = ";"

#combinedMeterReadingsFile = open('combinedmeterreadings-sydney-lga.csv', 'w')
combinedMeterReadingsSqlFile = open('combinedmeterreadings-sydney-lga.sql', 'w')
wescmlDomain = "http://wescml.org"
aggregationPrefix = wescmlDomain + "/sydney-example/combined-meter-readings/" 
utilityID = wescmlDomain + "/id/organisation/nonexistent-sydney-utility"
utilityName = "Non-existent Sydney Co."
commodityType = "water"
quarterMap = {1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3, 10: 4, 11: 4, 12: 4}
wescVocabMap = {'single dwelling': 'SingleDwellingProperty', 'nonresidential': 'MixedLandUse',
                'multi dwelling': 'MultiDwellingResProperty'}
# Dictionary below is manually derived by using 'State Suburbs ASGS Non ABS Structures Ed 2011 Digital Boundaries 
# in ESRI Shapefile Format' http://www.abs.gov.au/AUSSTATS/abs@.nsf/DetailsPage/1270.0.55.003July%202011?OpenDocument
# spatialRepPoints = { 'camberwell': { 'ssc_code':'20237', 'centroid_coords':'145.074017 -37.838442' }, 'ringwood': { 'ssc_code':'21144', 'centroid_coords':'145.23338 -37.811412' }, 'bundoora': { 'ssc_code':'20212', 'centroid_coords':'145.059671 -37.698249' } }

# Loads the csv exported from QGIS into a collection and turns it into a dictionary
spatialRepPoints = {}
sydneywaterLGAGeoCsv = open('../CommonFiles/spatial/abs/LGA_NSW_FromGeolayer.csv', 'r')
spatialData = csv.DictReader(sydneywaterLGAGeoCsv)

# for each line imported from the csv, a record is mad that is the locality name, vicnames_id and bounding box coords
for row in spatialData:
    spatialRepPoints[row['LGA_NAME_2011']] = {'LGA_CODE_2011': row['LGA_CODE_2011'],
                                              'Centroid': row['CENTX'] + " " + row['CENTY']}


if os.name == 'nt':
    locale.setlocale(locale.LC_ALL, 'english_AUS')
else:
    locale.setlocale(locale.LC_ALL, 'en_AU.utf8')


def exportDataToCsvAndSql():
    print "Exporting data to SQL files...."
    csvdata = open('ExampleWaterConsumptionSydneyLGA.csv', 'r')
    dataset = csv.DictReader(csvdata)

    # Running number for CombinedMeterReadings table
    key = 4000000

    # Write the header record to sql file
    combinedMeterReadingsSqlFile.write("BEGIN;\n")
    combinedMeterReadingsSqlFile.write(
        "DELETE FROM CombinedMeterReadings WHERE \"combinedMeterReadingsID\" BETWEEN " + str(key) + " AND " + str(key + 999999) + ";\n")
    for row in dataset:
        try:
            area = row["LGA"].upper()
            period = row["Read End Fiscal Quarter Code"]
            if area in spatialRepPoints:
                spatialRepPoints[area]  # This is a check. It'll throw exception if area cannot be found.
                #createCombinedMeterReadingsCsv(key, area, period, row["Premise Type Attribute"], row["Dwelling Count"],
                #                               row["Apportioned Consumption kl"])
                createCombinedMeterReadingsSql(key, area, period, row["Premise Type Attribute"], row["Dwelling Count"],
                                               row["Apportioned Consumption kl"])
                key += 1
            else:
                print "SKIPPED Consumption data for [%s]-[%s] not exported" % (area, period)
        except:
            print "ERROR Consumption data for [%s]-[%s] not exported" % (area, period)

    # Write the footer record to sql file
    combinedMeterReadingsSqlFile.write("COMMIT;\n")
    print "Done"


def createCombinedMeterReadingsCsv(key, area, period, propType, numMeters, total):
    # Prepare data for writing to file  
    startMonth = startMonthOfQuarter(period[5:])
    endMonth = endMonthOfQuarter(period[5:])
    yearInStr = period[:4]
    numDaysEndMonth = calendar.monthrange(int(yearInStr), endMonth)[1]
    numDaysInQtr = (date(int(yearInStr), endMonth, numDaysEndMonth) - date(int(yearInStr), startMonth, 1)).days + 1

    aggregationID = aggregationPrefix + str(key)
    aggregationStartDateTime = str(startMonth) + "/01/" + yearInStr + " 00:00:00"
    aggregationEndDateTime = str(endMonth) + "/" + str(numDaysEndMonth) + "/" + yearInStr + " 11:59:59"
    timeName = period
    numberOfMeters = numMeters
    numberOfReadings = ""
    resultTotal = str(total)
    if numMeters == '0'.strip():
        resultAverage = '0'
    else:
        resultAverage = str(float(total) / int(numMeters))
    resultMedian = ""
    unitsLabel = "kl"
    unitsURI = "http://www.wurvoc.org/vocabularies/om-1.8/kilolitre"
    resultProcedure = ""
    propertyTypeLabel = propType.lower()
    propertyTypeURI = wescmlDomain + "/def/" + wescVocabMap[propertyTypeLabel]
    geometryID = spatialRepPoints[area]["LGA_CODE_2011"]
    combinedMeterReadingsPoints = spatialRepPoints[area]["Centroid"]
    combinedMeterReadingsID = str(key)

    # Construct the record
    record = aggregationID + delim + utilityID + delim + \
             utilityName + delim + commodityType + delim + aggregationStartDateTime + delim + \
             aggregationEndDateTime + delim + timeName + delim + numberOfMeters + delim + \
             numberOfReadings + delim + resultTotal + delim + resultAverage + delim + \
             resultMedian + delim + unitsLabel + delim + unitsURI + delim + \
             resultProcedure + delim + propertyTypeLabel + delim + propertyTypeURI + delim + \
             geometryID + delim + combinedMeterReadingsPoints + delim + combinedMeterReadingsID + "\n"

    # Write the record to file
    combinedMeterReadingsFile.write(record)


def createCombinedMeterReadingsSql(key, area, period, propType, numMeters, total):
    # Prepare data for writing to file  
    startMonth = startMonthOfQuarter(period[5:])
    endMonth = endMonthOfQuarter(period[5:])
    if startMonth == 7 or startMonth == 10:
        yearInStr = str(int(period[:4]) - 1)
    else:
        yearInStr = period[:4]
    numDaysEndMonth = calendar.monthrange(int(yearInStr), endMonth)[1]
    numDaysInQtr = (date(int(yearInStr), endMonth, numDaysEndMonth) - date(int(yearInStr), startMonth, 1)).days + 1

    aggregationID = aggregationPrefix + str(key)
    aggregationStartDateTime = str(startMonth) + "/01/" + yearInStr + " 00:00:00"
    aggregationEndDateTime = str(endMonth) + "/" + str(numDaysEndMonth) + "/" + yearInStr + " 11:59:59"
    timeName = period
    numberOfMeters = numMeters
    numberOfReadings = "NULL"
    resultTotal = total
    if numMeters == '0'.strip():
        resultAverage = '0'
    else:
        resultAverage = str(float(total) / int(numMeters))
    resultMedian = "NULL"
    unitsLabel = "kl"
    unitsURI = "http://www.wurvoc.org/vocabularies/om-1.8/kilolitre"
    resultProcedure = "NULL"
    propertyTypeLabel = propType.lower()
    propertyTypeURI = wescmlDomain + "/def/" + wescVocabMap[propertyTypeLabel]
    geometryID = spatialRepPoints[area]["LGA_CODE_2011"]
    combinedMeterReadingsPoints = spatialRepPoints[area]["Centroid"]
    combinedMeterReadingsID = key

    # Construct the record
    sql = Template(
        'INSERT INTO CombinedMeterReadings (\"aggregationID\", \"utilityID\", \"utilityName\", \"commodityType\", \"aggregationStartDateTime\", \"aggregationEndDateTime\", \"timeName\", \"numberOfMeters\", \"numberOfReadings\", \"resultTotal\", \"resultAverage\", \"resultMedian\", \"unitsLabel\", \"unitsURI\", \"resultProcedure\", \"propertyType\", \"propertyTypeURI\", \"geometryID\", \"spatialRepresentation\", \"combinedMeterReadingsID\") VALUES (\'$agID\', \'$utID\', \'$utName\', \'$cType\', \'$agStartDt\', \'$agEndDt\', \'$timeName\', $numMeters, $numReadings, $resultTot, $resultAvg, $resultMed, \'$unitsLbl\', \'$unitsURI\', $resultProc, \'$propTypeLbl\', \'$propTypeURI\', \'$geomID\', ST_GeomFromText(\'POINT($combinedMtrReadsPoints)\',4283), $combinedMtrReadsID);')
    record = sql.substitute(agID=aggregationID, utID=utilityID, utName=utilityName, cType=commodityType,
                            agStartDt=aggregationStartDateTime, agEndDt=aggregationEndDateTime, timeName=timeName,
                            numMeters=numberOfMeters, numReadings=numberOfReadings, resultTot=resultTotal,
                            resultAvg=resultAverage, resultMed=resultMedian, unitsLbl=unitsLabel, unitsURI=unitsURI,
                            resultProc=resultProcedure, propTypeLbl=propertyTypeLabel, propTypeURI=propertyTypeURI,
                            geomID=geometryID, combinedMtrReadsPoints=combinedMeterReadingsPoints,
                            combinedMtrReadsID=combinedMeterReadingsID) + "\n"

    # Write the record to file
    combinedMeterReadingsSqlFile.write(record)


def startMonthOfQuarter(qtrInNum):
    #return {'1': 1, '2': 4, '3': 7, '4': 10}[qtrInNum]
    return {'1': 7, '2': 10, '3': 1, '4': 4}[qtrInNum]


def endMonthOfQuarter(qtrInNum):
    #return {'1': 3, '2': 6, '3': 9, '4': 12}[qtrInNum]
    return {'1': 9, '2': 12, '3': 3, '4': 6}[qtrInNum]


def main():
    exportDataToCsvAndSql()


__name__ == '__main__' and main()
