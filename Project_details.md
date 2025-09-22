## Overview
I'm creating a new project to salavage a .fit file from a big 200 mile ride I did, the problem is that my computer didn't save gps data. However I rode with other people who i can get their gpx files from. So here's my plan:

**UPDATE**: After investigation, discovered the FIT file DID contain GPS data! The issue was proprietary message types that Strava couldn't parse.
 
 ### Original Workflow Plan (No Longer Needed)
 - Combine Ride to Ride.gpx - scout_ride.gpx - Ride From Ride.gpx
    - Scout started from a different place, so clip his ride at the closest end point gps from Ride to Ride and append to Ride to Ride
    - Clip the end of his ride at the closest gps point to the start of Ride From Ride and append Ride From Ride to the combined gpx file
    - This combined GPX file should more-or-less match my ride in a gpx sense
- Figure out a best way to match up the speed - time - elevation data that we can pull from the .fit file and infer which GPS locations we can determine from those data points (i.e. c9ould we make an algorithim to 'ride' the route)
    - There are small discrepancies throughout the ride where i went in different places than him, help me reconcile this, maybe elevation is a good ground truth (if there's a mis-match help me shift my ride to conform to the elevation)

### Final Solution (Sept 20-22, 2025)
- **DISCOVERY**: FIT file contains complete GPS data (98.9% coverage) + all training metrics
- **ROOT CAUSE**: Wahoo ELEMNT devices include proprietary message types (unknown_65280-65285) that Strava rejects
- **SOLUTION**: Extract data to standard GPX format with TrackPointExtensions
- **RESULT**: Successfully recovered 209-mile ride with GPS + Power + Heart Rate + Cadence data

### Final Workflow (Implemented)
1. ✅ Analyze FIT file and identify unknown message types causing Strava rejection
2. ✅ Extract GPS coordinates (semicircle to decimal degrees conversion)
3. ✅ Extract training data (power, heart rate, cadence, temperature)
4. ✅ Create enhanced GPX with standard TrackPointExtensions
5. ✅ Generate Strava-compatible file preserving all essential training data

### Tools Created
- `fit_gps_recovery.ipynb` - Clean, reusable notebook for analysis and conversion
- `fit_recovery.py` - Command-line script for batch processing
- `README.md` - Complete documentation and troubleshooting guide

### Coding practices
- Write everything we can in python, create a readme.txt
- Give me some suggestions of frameworks to work in that allows for some interactive visualizations of the resutls and to visualize and shift any mis-matched data (maybe just a python notebook, maybe a streamlit app, i'm not sure what's best)
- Give me any other suggestions of things I hadn't considered

### Required Python Libraries
- `gpxpy` - for parsing and manipulating GPX files
- `fitparse` or `python-fitparse` - for reading FIT files
- `pandas` - for data manipulation and analysis
- `numpy` - for numerical computations
- `folium` or `plotly` - for interactive map visualizations
- `matplotlib/seaborn` - for plotting elevation profiles and data analysis
- `scikit-learn` - for potential matching algorithms
- `geopy` - for distance calculations between GPS points

### Technical Considerations
- **Time synchronization**: How to align timestamps between different riders' data
- **Sampling rate differences**: GPX files may have different recording intervals
- **Elevation data quality**: Some GPS devices have better barometric altimeters
- **Route deviation handling**: Algorithm to determine when you took a different path vs. GPS noise
- **Data interpolation**: How to fill gaps or smooth inconsistent data points
- **Validation metrics**: How to measure the quality of the merged result

### Visualization Framework Recommendation
**Jupyter Notebook + Plotly/Folium** is recommended because:
- Interactive development and iteration
- Easy to visualize GPS tracks on maps
- Can create interactive plots for elevation profiles
- Good for data exploration and debugging
- Can export final results or create a simple Streamlit app later if needed

### Additional Data Sources to Consider
- Weather data for the ride date (wind direction/speed could explain route choices)
- Official route/course GPX if this was an organized ride
- Strava segments or other riders' data for validation