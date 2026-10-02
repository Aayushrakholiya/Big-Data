#  
#  FILE          : extract_data.py
#  PROJECT       : Assignment #6 
#  PROGRAMMER    : Ayushkumar rakholiya and darsh patel
#  FIRST VERSION : 2026-04-03 
#  DESCRIPTION   : 
#    this script wiil extract the data from the xml files and save it in a csv file. 
#

import xml.etree.ElementTree as ET
import csv
from collections import defaultdict
from pathlib import Path

# this is a file that extracts the data from the xml files and saves it in a csv file.
structureFile = "Structure_99-012-X2011033.xml"
genericFile = "Generic_99-012-X2011033.xml"
outputFile = "output/Data.csv"

namespaces = {
    'str': 'http://www.SDMX.org/resources/SDMXML/schemas/v2_0/structure',
    'generic': 'http://www.SDMX.org/resources/SDMXML/schemas/v2_0/generic',
}

# valid codes for filtering
validProvinces = {'01','10','11','12','13','24','35','46','47','48','59','60','61','62'}
validAges = {'2','5','6','12','13'}
validNocs = {'2','74','147','227','277','331','375','457','564','603'}

codeMappings = {'GEO': {}, 'NOC2011': {}, 'AGEGR5': {}}

# this function will parse the structure file.
def parseStructure():
    root = ET.parse(structureFile).getroot()
    codeListMap = {'CL_GEO': 'GEO', 'CL_NOC2011': 'NOC2011', 'CL_AGEGR5': 'AGEGR5'}

    for codeList in root.findall('.//str:CodeList', namespaces):
        dimension = codeListMap.get(codeList.get('id'))
        if not dimension:
            continue

        for code in codeList.findall('str:Code', namespaces):
            codeMappings[dimension][code.get('value')] = (
                code.findtext('str:Description', default=code.get('value'), namespaces=namespaces)
            )

# this function will stream the generic file and aggregate the data based on the dimensions.
def streamAndAggregate():
    aggregatedData = defaultdict(int)

    for _, element in ET.iterparse(genericFile, events=('end',)):
        if element.tag != f"{{{namespaces['generic']}}}Series":
            continue

        seriesKey = element.find(f"{{{namespaces['generic']}}}SeriesKey")
        if seriesKey is None:
            element.clear()
            continue

        dimensions = {
            value.get('concept'): value.get('value')
            for value in seriesKey.findall(f"{{{namespaces['generic']}}}Value")
        }

        geo = dimensions.get('GEO')
        noc = dimensions.get('NOC2011')
        age = dimensions.get('AGEGR5')

        if geo not in validProvinces or noc not in validNocs or age not in validAges:
            element.clear()
            continue

        obsValue = element.find(f".//{{{namespaces['generic']}}}ObsValue")
        if obsValue is not None:
            try:
                aggregatedData[(geo, noc, age)] += float(obsValue.get('value', 0))
            except:
                pass

        element.clear()

    return aggregatedData

# this function will save the aggregated data to a csv file.
def saveData(aggregatedData):
    Path("output").mkdir(exist_ok=True)

    with open(outputFile, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Province_Name', 'Occupation', 'Age_Group', 'Count'])

        for (geo, noc, age), count in aggregatedData.items():
            writer.writerow([codeMappings['GEO'].get(geo, 'Unknown'),codeMappings['NOC2011'].get(noc, 'Unknown'),codeMappings['AGEGR5'].get(age, 'Unknown'),int(count)])

def main():
    parseStructure()
    saveData(streamAndAggregate())

if __name__ == "__main__":
    main()