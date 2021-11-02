import os
import shutil
import xml.etree.ElementTree as ET
from pyspark.sql import SparkSession
from pyspark.sql.types import (StructType, StructField, StringType, IntegerType)

# Define columns for the DataFrame
col_names = ['LINK_ID', 'REGION', 'ROAD_TYPE', 'ROAD_SATURATION_LEVEL', 'TRAFFIC_SPEED', 'CAPTURE_DATE']
elements = [col for col in col_names]

def set_schema():
    schema_list = []
    for col in col_names:
        if col == 'TRAFFIC_SPEED':
            schema_list.append(StructField(col, IntegerType(), True))
        else:
            schema_list.append(StructField(col, StringType(), True))

    return StructType(schema_list)

def parse_xml(rdd):
    results = []
    try:
        # Define namespace
        ns = {'ns': 'http://data.one.gov.hk/td'}

        root = ET.fromstring(rdd[0])
        for speedmap in root.findall('ns:jtis_speedmap', ns):
            record = []
            for element in elements:
                if speedmap.find('ns:{0}'.format(element), ns) is None:
                    record.append(None)
                    continue
                value = speedmap.find('ns:{0}'.format(element), ns).text
                if element == 'TRAFFIC_SPEED':
                    value = int(value)
                record.append(value)
            results.append(record)
    except:
        return results
    return results

def convert_xml_to_parquet(date):
    path = 'output/{0}'.format(date)
    if os.path.exists(path):
        shutil.rmtree(path)
    # Init builder
    spark = SparkSession.builder.getOrCreate()
    # Define schema
    schema = set_schema()
    # Read all xml file and then convert to RDD
    file_rdd = spark.read.text('data/{0}-*.xml'.format(date), wholetext=True).rdd
    records_rdd = file_rdd.flatMap(parse_xml)
    # Convert RDDs to DataFrame with the pre-defined schema
    df = records_rdd.toDF(schema)
    # Write to parquet
    df.repartition(1).write.parquet(path, 'overwrite')

    return path

if __name__ == '__main__':
    convert_xml_to_parquet(date)