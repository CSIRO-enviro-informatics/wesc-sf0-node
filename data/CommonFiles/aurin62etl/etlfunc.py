import csv, sys, locale, os, calendar, pandas
from string import Template
from datetime import date
import json


#globals
wescmlDomain = "http://wescml.org"
POLYGON_FIELD = 'PolyCoords'


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

YearType = enum('financial', 'calendar')

#class defs
class Dataset:
    def __init__(self, aggregationName, orgId, orgName, commodityType, unitsLabel, unitsURI, keyInit, inputFileName, spatialIndexColName, vocabMap, dataMappings, yearType=YearType.calendar):
        self.aggregationName = aggregationName
        self.orgId = orgId
        self.orgName = orgName
        self.commodityType = commodityType
        self.unitsLabel = unitsLabel
        self.unitsURI = unitsURI
        self.keyInit = keyInit
        self.inputFileName = inputFileName
        self.spatialIndexColName = spatialIndexColName
        self.wescmlDomain = wescmlDomain
        self.vocabMap = vocabMap
        self.dataMappings = dataMappings
        self.yearType = yearType 

    def getAggregationId(self, key):
        aggregationID = wescmlDomain + self.aggregationName + str(key)
        return  aggregationID

#geoclassification = vicmap_postcode, vicmap_locality, abs_poa, etc.
#geometry_data_type = polygon, centroids
#spatialIndex is a index - each object in the index is a key-value-pair for each spatial object - e.g. polygon, points, names
def getGeometry(geoclassification, geometry_data_type):
    #csv.field_size_limit(2147483647/ 100)
    spatialIndex = {}

    if geoclassification == 'vicmap_locality' and geometry_data_type == 'polygon' :
        with open('../CommonFiles/vicmap_localities/data7877410474856273325.json') as f:
            for line in f:

                j = json.loads(line)
                json_items_count = len(j['features'])
                print json_items_count

                for item_num in range (0, json_items_count ):

                    #print j['features'][0]['geometry']
                    #print j['features'][item_num]['properties']['LOCALITY_NAME']
                    locality_name = str(j['features'][item_num]['properties']['LOCALITY_NAME'])
                    vicnames_id = str(j['features'][item_num]['properties']['VICNAMES_ID'])
                    print "Processing " + locality_name

                    #print j['features'][item_num]['geometry']['type']
                    poly_type = str(j['features'][item_num]['geometry']['type'])
                    #print j['features'][item_num]['geometry']['coordinates']
                    poly_coords = str(j['features'][item_num]['geometry']['coordinates'])
                    poly_coords = poly_coords.replace("[[[","(((")
                    poly_coords = poly_coords.replace("]]]",")))")
                    poly_coords = poly_coords.replace(", "," ")
                    poly_coords = poly_coords.replace("] [", ", ")
                    poly_coords = poly_coords.replace("]","")
                    poly_coords = poly_coords.replace("[","")
                    #print j['features'][item_num]['properties']['boundedBy']
                    bounded_by = str(j['features'][item_num]['properties']['boundedBy'])
                    #spatialPolygonPoints.append(json.loads(line))

                    spatialIndex[locality_name] = {POLYGON_FIELD: poly_type + " " + poly_coords, 'VICNAMES_ID': vicnames_id}

    elif geoclassification == 'vicmap_locality' and geometry_data_type == 'centroid':
        # Loads the csv exported from QGIS into a collection and turns it into a dictionary
        localityCsv = open('../CommonFiles/VicMapLocality.csv', 'r')
        spatialData = csv.DictReader(localityCsv)

        # for each line imported from the csv, a record is made that is the locality name, vicnames_id and bounding box coords
        for row in spatialData:
            CentX = (float(row['boundedBy1']) + float(row['boundedBy3']) ) /2
            CentY = (float(row['boundedBy2']) + float(row['boundedBy4']) ) /2
            spatialIndex[row['LOCALITY_NAME']] = {'VICNAMES_ID': row['VICNAMES_ID'], POLYGON_FIELD: str(CentX) + ' ' + str(CentY)}

    elif(geoclassification == 'vicmap_postcode' and geometry_data_type == 'polygon'):
    	try:
		vicmapPolygons = open('../CommonFiles/vicmap_postcode_polygon/vicmap_postcode_wkt.csv')
	except:
		vicmapPolygons = open('../../CommonFiles/vicmap_postcode_polygon/vicmap_postcode_wkt.csv')
        spatialPolygonData = csv.DictReader(vicmapPolygons, delimiter='\t')

        # for each line imported from the polygons csv, a record is made that is the postcode and the polygon points
        #maxInt = int(sys.maxsize)
        csv.field_size_limit(2147483647/ 100)
        for row in spatialPolygonData:
            postcode = row[spatialPolygonData.fieldnames[2]]
            spatialIndex[postcode] = {POLYGON_FIELD: row[spatialPolygonData.fieldnames[0]].replace("'",""),
                                                                   'postcode_id' : postcode
                                                                   }
    
    elif(geoclassification == 'abs_ausmap_postcode' and geometry_data_type == 'polygon'):
        poamapPolygons = open('../CommonFiles/poa_2011_aust_boundaries/poa_2011_aust_boundaries_wkt.csv')
        spatialPolygonData = csv.DictReader(poamapPolygons)

        # for each line imported from the polygons csv, a record is made that is the postcode and the polygon points
        #maxInt = int(sys.maxsize)
        csv.field_size_limit(2147483647/ 100)
        for row in spatialPolygonData:
            postcode = row[spatialPolygonData.fieldnames[2]]
            spatialIndex[postcode] = {POLYGON_FIELD: row[spatialPolygonData.fieldnames[0]].replace("'",""),
                                                                   'postcode_id' : postcode
                                                                   }
    elif(geoclassification == 'psma_act_postcode' and geometry_data_type == 'polygon'):
        poamapID = open('../CommonFiles/psma_postcode_geoms/ACT_POSTCODE_shp.csv')
        poamapPolygons = open('../CommonFiles/psma_postcode_geoms/ACT_POSTCODE_POLYGON_shp.csv')

        poamapIDData = csv.DictReader(poamapID, delimiter='\t')
        idPostcode = {row["PC_PID"]: row["POSTCODE"] for row in poamapIDData}
        spatialPolygonData = csv.DictReader(poamapPolygons, delimiter='\t')

        # for each line imported from the polygons csv, a record is made that is the postcode and the polygon points
        #maxInt = int(sys.maxsize)
        csv.field_size_limit(2147483647/ 100)
        for row in spatialPolygonData:
            postcodeID = row[spatialPolygonData.fieldnames[4]]
            postcode = idPostcode[postcodeID]
            spatialIndex[postcode] = {POLYGON_FIELD: row[spatialPolygonData.fieldnames[0]].replace("'",""),
                                                                   'postcode_id' : postcode
                                                                   }
    elif(geoclassification == 'psma_act_locality' and geometry_data_type == 'polygon'):
        poamapPolygons = open('../CommonFiles/PSMA+Localities - cbr/psma_localities_cbr.wkt')
        spatialPolygonData = csv.DictReader(poamapPolygons, delimiter='\t')

        # for each line imported from the polygons csv, a record is made that is the postcode and the polygon points
        #maxInt = int(sys.maxsize)
        csv.field_size_limit(2147483647/ 100)
        for row in spatialPolygonData:
            locality = row[spatialPolygonData.fieldnames[4]]
            spatialIndex[locality] = {POLYGON_FIELD: row[spatialPolygonData.fieldnames[0]].replace("'",""),
                                                                   'loccl_code' : locality
                                                                   }
    elif(geoclassification == 'psma_qld_postcode' and geometry_data_type == 'polygon'):
        poamapID = open('../CommonFiles/psma_postcode_geoms/QLD_POSTCODE_shp.csv')
        poamapPolygons = open('../CommonFiles/psma_postcode_geoms/QLD_POSTCODE_POLYGON_shp.csv')

        poamapIDData = csv.DictReader(poamapID, delimiter='\t')
        idPostcode = {row["PC_PID"]: row["POSTCODE"] for row in poamapIDData}

        spatialPolygonData = csv.DictReader(poamapPolygons, delimiter='\t')

        # for each line imported from the polygons csv, a record is made that is the postcode and the polygon points
        #maxInt = int(sys.maxsize)
        csv.field_size_limit(2147483647/ 100)
        for row in spatialPolygonData:
            postcodeID = row[spatialPolygonData.fieldnames[4]]
            postcode = idPostcode[postcodeID]
            spatialIndex[postcode] = {POLYGON_FIELD: row[spatialPolygonData.fieldnames[0]].replace("'",""),
                                                                   'postcode_id' : postcode
                                                                   }
    elif(geoclassification == 'qld_locality' and geometry_data_type == 'polygon'):
        poamapPolygons = open('../CommonFiles/PSMA+Localities-brisbane/psma_localities_brisbane_wkt.csv')
        spatialPolygonData = csv.DictReader(poamapPolygons)

        # for each line imported from the polygons csv, a record is made that is the postcode and the polygon points
        #maxInt = int(sys.maxsize)
        csv.field_size_limit(2147483647/ 100)
        for row in spatialPolygonData:
            locality = row[spatialPolygonData.fieldnames[4]]
            spatialIndex[locality] = {POLYGON_FIELD: row[spatialPolygonData.fieldnames[0]].replace("'",""),
                                                                   'locality_name' : locality 
                                                                   }

    return spatialIndex

#Exports a dataset as defined in the dataset parameter to the combinedMeterReadingsSqlFile 
#csv_dataset is a dictionary where the key is a field name and the value is a list of row values for the corresponding csv column in the original csv file
def exportDatasetToCsvAndSql(dataset, csv_dataset, combinedMeterReadingsSqlFile, spatialIndex, isMonthly=False):
    # Write the header record to sql file
    combinedMeterReadingsSqlFile.write("BEGIN;\n")
    combinedMeterReadingsSqlFile.write(
        "DELETE FROM CombinedMeterReadings WHERE \"combinedMeterReadingsID\" BETWEEN " + str(dataset.keyInit) + " AND " + str(dataset.keyInit + 999999) + ";\n")

    key = dataset.keyInit
	    
    for row in csv_dataset:
        ##try:
            spatialIdentifier = row[dataset.dataMappings['spatialId']].upper()
            period = row[dataset.dataMappings['period']]

            if spatialIdentifier in spatialIndex:
                spatialIndex[spatialIdentifier]  # This is a check. It'll throw exception if area cannot be found.

                createCombinedMeterReadingsSql(key, dataset, spatialIdentifier, period,
                                               row[dataset.dataMappings['propertyType']],
                                               row[dataset.dataMappings['numOfMeters']],
                                               row[dataset.dataMappings['resultTotal']],
                                               combinedMeterReadingsSqlFile, spatialIndex, yearType=dataset.yearType, isMonthly = isMonthly 
                                               )
                print "Created SQL statement for " + spatialIdentifier

                key += 1

            else:
                print "SKIPPED Consumption data for [%s]-[%s] not exported" % (spatialIdentifier, period)
        ##except:
        ##    print "ERROR Consumption data for [%s]-[%s] not exported" % (area, period)

    # Write the footer record to sql file
    combinedMeterReadingsSqlFile.write("COMMIT;\n")
    print "Done"

#dataset is of the Dataset class
def exportDataToCsvAndSql(dataset, combinedMeterReadingsSqlFile, spatialIndex, isMonthly = "FALSE"):
    print "Exporting data to CSV and SQL files..."
    inputcsv = open(dataset.inputFileName, 'r')
    csv_dataset = csv.DictReader(inputcsv)
    exportDatasetToCsvAndSql(dataset, csv_dataset, combinedMeterReadingsSqlFile, spatialIndex, isMonthly)


#spatialIdentifier - e.g. locality name, postcode, abs sa2 id
def createCombinedMeterReadingsSql(key, dataset, spatialIdentifier, period, propType, numberOfMeters, total, combinedMeterReadingsSqlFile, spatialIndex, numberOfReadings='NULL', resultMedian='NULL', resultProcedure='NULL', yearType=YearType.calendar, isMonthly = "FALSE"):
    # Prepare data for writing to file

    if isMonthly == "TRUE":
        yearInStr = period[:4]
        startMonth = int(period[4:])
        endMonth = int(period[4:])
        numDaysEndMonth = calendar.monthrange(int(yearInStr), endMonth)[1]
        aggregationStartDateTime = str(startMonth) + "/01/" + yearInStr + " 00:00:00"
        aggregationEndDateTime = str(endMonth) + "/" + str(numDaysEndMonth) + "/" + yearInStr + " 11:59:59"
    else:
        if yearType == YearType.calendar:
            p = pandas.Period(period, 'Q-DEC')
        elif yearType == YearType.financial:
            p = pandas.Period(period, 'Q-JUN')
        aggregationStartDateTime = p.to_timestamp('D', how='s')
        aggregationEndDateTime = p.to_timestamp('D', how='e') 

    utilityID =  dataset.orgId
    utilityName = dataset.orgName
    aggregationID = dataset.getAggregationId(key)
    

    timeName = period
    resultTotal = total

    #some checks to avoid errors when numberOfMeters is 0 or missing
    if numberOfMeters == '0'.strip() or numberOfMeters == 'NULL' or numberOfMeters == '':
        resultAverage = '0'
        numberOfMeters = '0'
    else:
        resultAverage = str(float(total) / int(numberOfMeters))

    propertyTypeLabel = propType.lower()
    
    if dataset.vocabMap.has_key(propertyTypeLabel):
        propertyTypeURI = wescmlDomain + "/def/" + dataset.vocabMap[propertyTypeLabel]
    else:
        propertyTypeURI = propertyTypeLabel
        
    geometryID = spatialIndex[spatialIdentifier][dataset.spatialIndexColName]
    #a fix for "'" in place names which ruins the sql structure
    if geometryID.find('\'') > -1:
        #geometryID = geometryID[:geometryID.find("'")] + '\\' +  geometryID[spatialIdentifier.find("'"):]
        geometryID = geometryID.replace("'","''")

    combinedMeterReadingsGeom = spatialIndex[spatialIdentifier][POLYGON_FIELD]
    #spatialRepPoints[area]["BoundingBox"]
    combinedMeterReadingsID = str(key)


    # Construct the record
    sql = Template(
        'INSERT INTO CombinedMeterReadings (\"aggregationID\", \"utilityID\", \"utilityName\", \"commodityType\", \"aggregationStartDateTime\", \"aggregationEndDateTime\", \"timeName\", \"numberOfMeters\", \"numberOfReadings\", \"resultTotal\", \"resultAverage\", \"resultMedian\", \"unitsLabel\", \"unitsURI\", \"resultProcedure\", \"propertyType\", \"propertyTypeURI\", \"geometryID\", \"spatialRepresentation\", \"combinedMeterReadingsID\") VALUES (\'$agID\', \'$utID\', \'$utName\', \'$cType\', \'$agStartDt\', \'$agEndDt\', \'$timeName\', $numMeters, $numReadings, $resultTot, $resultAvg, $resultMed, \'$unitsLbl\', \'$unitsURI\', $resultProc, \'$propTypeLbl\', \'$propTypeURI\', \'$geomID\', ST_GeomFromText(\'$combinedMtrReadGeom\',4283), $combinedMtrReadsID);')
    record = sql.substitute(agID=aggregationID, utID=utilityID, utName=utilityName, cType=dataset.commodityType,
                            agStartDt=aggregationStartDateTime, agEndDt=aggregationEndDateTime, timeName=timeName,
                            numMeters=numberOfMeters, numReadings=numberOfReadings, resultTot=resultTotal,
                            resultAvg=resultAverage, resultMed=resultMedian, unitsLbl=dataset.unitsLabel, unitsURI=dataset.unitsURI,
                            resultProc=resultProcedure, propTypeLbl=propertyTypeLabel, propTypeURI=propertyTypeURI,
                            geomID=geometryID, combinedMtrReadGeom=combinedMeterReadingsGeom,
                            combinedMtrReadsID=combinedMeterReadingsID) + "\n"

    # Write the record to file
    combinedMeterReadingsSqlFile.write(record)
