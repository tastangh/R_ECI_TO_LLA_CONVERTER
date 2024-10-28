# R_ECI_TO_LLA_CONVERTER

## Name
R_ECI_TO_LLA_CONVERTER

## Description
This repository contains a Python script for extracting satellite position data in Earth-Centered Inertial (ECI) coordinates from InfluxDB, converting them to Earth-Centered Earth-Fixed (ECEF) and then to Latitude-Longitude-Altitude (LLA) coordinates. The resulting LLA coordinates are written back to InfluxDB. The script uses the PyMap3D library for coordinate conversions, Astropy for time handling, and the InfluxDB client for communication with the InfluxDB database.

The setup also includes integration with Grafana for visualizing the satellite's trajectory and AOCS (Attitude and Orbit Control System) Trick simulation for generating the satellite position data.

## Prerequisites
Python 3.x
Required Python packages: pymap3d, astropy, influxdb-client

## InfluxDB, Grafana, and AOCS Trick Integration
```
 1. InfluxDB Setup:
     A.Install and configure InfluxDB.
     B.Create a new bucket for storing satellite position data.
     C.Update the InfluxDB connection parameters in the script:
         a.url: InfluxDB server URL
         b.token: InfluxDB authentication token
         c.org: InfluxDB organization
         d.bucket: InfluxDB bucket
         e.measurement: Measurement name for LLA coordinates
```



```
2.Grafana Setup:
    A.Install and configure Grafana.
    B.Connect Grafana to the InfluxDB instance.
    C.Import a dashboard for visualizing the satellite's trajectory.
```


```
3.AOCS Trick Simulation:
    A.Set up the AOCS Trick simulation environment.
    B.Ensure that the simulation generates satellite position data in the specified InfluxDB bucket.
```


## Setup
```
1.Install the required Python packages:
    pip install pymap3d astropy influxdb-client
```


```
2.Update the InfluxDB connection parameters in the script:
url: InfluxDB server URL
token: InfluxDB authentication token
org: InfluxDB organization
bucket: InfluxDB bucket
measurement: Measurement name for LLA coordinates
```


```
3.Run the script:
python main.py
```

## Grafana Dashboard
Import the provided Grafana dashboard (dashboard.json) to visualize the satellite's trajectory. Customize the dashboard as needed.

## Script Details
The script continuously queries satellite position data (ECI coordinates) from InfluxDB, performs the necessary conversions, and writes the resulting LLA coordinates back to InfluxDB.

The ECI to ECEF conversion is handled by the eci_to_ecef function, and the ECEF to LLA conversion is done by the ecef_to_lla function.

The extracted data and converted coordinates are printed to the terminal.

## InfluxDB Queries
The script uses InfluxDB queries to retrieve ECI coordinates and Julian Date (JD) time from the specified InfluxDB bucket.

## Handling KeyboardInterrupt and Closing the InfluxDB Connection
The script can be interrupted gracefully using a KeyboardInterrupt (Ctrl+C), ensuring proper closure of the InfluxDB client.
The InfluxDB client connection is closed in the finally block to ensure a clean exit.

## Support
Contact Mehmet Taştan
