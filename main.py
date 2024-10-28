import pymap3d as pm
from astropy.time import Time
from influxdb_client import InfluxDBClient
from influxdb_client.client.write.point import Point
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB connection parameters
url = "http://localhost:8086"
token = "0f48ad9a1c4a43af9643a3c77f6dc4b42df38ffe0d0368551629082a567e5587"
org = "tai"
bucket = "trick"
measurement = "galacsim_lla"  # New measurement for LLA coordinates

# Connect to InfluxDB
client = InfluxDBClient(url=url, token=token)
query_api = client.query_api()
write_api = client.write_api(write_options=SYNCHRONOUS)

# Define a function to convert R_ECI to ECEF
def eci_to_ecef(eci_x, eci_y, eci_z, time_utc):
    eci_x = eci_x * 1000
    eci_y = eci_y * 1000
    eci_z = eci_z * 1000
    ecef = pm.eci2ecef(eci_x, eci_y, eci_z,time_utc)
    return ecef

# Define a function to convert ECEF to LLA
def ecef_to_lla(ecef):
    lla = pm.ecef2geodetic(ecef[0], ecef[1], ecef[2])
    return lla

try:
    while True:
        # Query ECI_X, ECI_Y, ECI_Z coordinates from InfluxDB
        query_eci_x = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "galacsim") |> filter(fn: (r) => r["_field"] == "satelliteSO.SATELLITE_Y.R_ECI[0]") |> aggregateWindow(every: 100ms, fn: mean, createEmpty: false) |> last()'
        query_eci_y = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "galacsim") |> filter(fn: (r) => r["_field"] == "satelliteSO.SATELLITE_Y.R_ECI[1]") |> aggregateWindow(every: 100ms, fn: mean, createEmpty: false) |> last()'
        query_eci_z = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "galacsim") |> filter(fn: (r) => r["_field"] == "satelliteSO.SATELLITE_Y.R_ECI[2]") |> aggregateWindow(every: 100ms, fn: mean, createEmpty: false) |> last()'
        query_jd_time = f'from(bucket: "{bucket}") |> range(start: -1h) |> filter(fn: (r) => r["_measurement"] == "galacsim") |> filter(fn: (r) => r["_field"] == "satelliteSO.SATELLITE_Y.JD") |> aggregateWindow(every: 100ms, fn: last, createEmpty: false) |> last()'

        result_eci_x = query_api.query(query_eci_x, org=org)
        result_eci_y = query_api.query(query_eci_y, org=org)
        result_eci_z = query_api.query(query_eci_z, org=org)
        result_jd_time = query_api.query(query_jd_time, org=org)


        # Process the data (example: print and write to InfluxDB)
        for table_x, table_y, table_z,table_jd in zip(result_eci_x, result_eci_y, result_eci_z,result_jd_time):
            for record_x, record_y, record_z,record_jd in zip(table_x.records, table_y.records, table_z.records,table_jd.records):
                # Extract values from the records
                eci_x = record_x.values["_value"]
                eci_y = record_y.values["_value"]
                eci_z = record_z.values["_value"]
                jd_time = record_jd.values["_value"]
                time_utc = Time(jd_time, format="jd", scale="utc").datetime
                # time_utc = record_x.get_time()  # Assume all records have the same timestamp

                # Combine ECI_X, ECI_Y, ECI_Z
                r_eci = [eci_x, eci_y, eci_z]
                print(f"R_ECI Values: X={r_eci[0]}, Y={r_eci[1]}, Z={r_eci[2]}, Time={time_utc}")


                # Convert ECI to ECEF
                ecef = eci_to_ecef(r_eci[0], r_eci[1], r_eci[2],time_utc)
                print(f"ecef Values: X={ecef[0]},6 Y={ecef[1]}, Z={ecef[2]}")

                # Convert ECEF to LLA
                lla = ecef_to_lla(ecef)
                
                # Print LLA coordinates to terminal
                print(f"LLA Coordinates: Latitude={lla[0]}, Longitude={lla[1]}, Altitude={lla[2]}, Time={time_utc}")

                # Create a new Point for the LLA coordinates
                point = Point(measurement)
                point.field("latitude", lla[0]).field("longitude", lla[1]).field("altitude", lla[2])

                # Write the Point to InfluxDB
                write_api.write(bucket=bucket, org=org, record=point)

except KeyboardInterrupt:
    pass
finally:
    client.close()
