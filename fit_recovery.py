#!/usr/bin/env python3
"""
FIT GPS Recovery Tool - Command Line Version

Extracts GPS and training data from FIT files that Strava rejects
due to proprietary message types.

Usage:
    python fit_recovery.py <input_fit_file> [output_gpx_file]

Example:
    python fit_recovery.py data/ride.fit enhanced_ride.gpx
"""

import sys
import os
import fitparse
import pandas as pd
from datetime import datetime

def semicircle_to_degrees(semicircle_value):
    """Convert Garmin semicircle coordinates to decimal degrees"""
    if semicircle_value is None:
        return None
    return semicircle_value * (180 / 2**31)

def extract_fit_data(fit_file_path):
    """Extract GPS and training data from FIT file"""
    print(f"📂 Reading FIT file: {fit_file_path}")
    
    fitfile = fitparse.FitFile(fit_file_path)
    records = list(fitfile.get_messages('record'))
    
    print(f"📊 Found {len(records):,} data records")
    
    # Extract GPS and training data
    gps_data = []
    for record in records:
        lat_raw = record.get_value('position_lat')
        lon_raw = record.get_value('position_long')
        
        if lat_raw is not None and lon_raw is not None:
            gps_data.append({
                'timestamp': record.get_value('timestamp'),
                'lat': semicircle_to_degrees(lat_raw),
                'lon': semicircle_to_degrees(lon_raw),
                'altitude': record.get_value('altitude'),
                'power': record.get_value('power'),
                'heart_rate': record.get_value('heart_rate'),
                'cadence': record.get_value('cadence'),
                'temperature': record.get_value('temperature')
            })
    
    df = pd.DataFrame(gps_data)
    print(f"📍 Extracted {len(df):,} GPS points")
    
    return df

def create_enhanced_gpx(df, output_filename):
    """Create GPX file with training data extensions"""
    print(f"📝 Creating enhanced GPX: {output_filename}")
    
    # GPX header
    gpx_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="FIT GPS Recovery Tool" 
     xmlns="http://www.topografix.com/GPX/1/1"
     xmlns:gpxtpx="http://www.garmin.com/xmlschemas/TrackPointExtension/v1"
     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
     xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd
                         http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd">
  <metadata>
    <name>Recovered Ride with Training Data</name>
    <desc>GPS track recovered from FIT file</desc>
    <time>{df['timestamp'].iloc[0].strftime('%Y-%m-%dT%H:%M:%SZ')}</time>
  </metadata>
  <trk>
    <name>Bike Ride</name>
    <type>cycling</type>
    <trkseg>
'''
    
    # Add GPS points with training data
    for _, row in df.iterrows():
        lat = row['lat']
        lon = row['lon']
        timestamp = row['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')
        elevation = row['altitude'] if pd.notna(row['altitude']) else 0
        
        point_xml = f'      <trkpt lat="{lat:.6f}" lon="{lon:.6f}">\\n'
        point_xml += f'        <ele>{elevation:.1f}</ele>\\n'
        point_xml += f'        <time>{timestamp}</time>\\n'
        
        # Add training data extensions
        extensions = []
        if pd.notna(row['heart_rate']) and row['heart_rate'] > 0:
            extensions.append(f'          <gpxtpx:hr>{int(row["heart_rate"])}</gpxtpx:hr>')
        if pd.notna(row['power']) and row['power'] > 0:
            extensions.append(f'          <gpxtpx:power>{int(row["power"])}</gpxtpx:power>')
        if pd.notna(row['cadence']) and row['cadence'] > 0:
            extensions.append(f'          <gpxtpx:cad>{int(row["cadence"])}</gpxtpx:cad>')
        if pd.notna(row['temperature']):
            extensions.append(f'          <gpxtpx:atemp>{int(row["temperature"])}</gpxtpx:atemp>')
        
        if extensions:
            point_xml += '        <extensions>\\n          <gpxtpx:TrackPointExtension>\\n'
            point_xml += '\\n'.join(extensions)
            point_xml += '\\n          </gpxtpx:TrackPointExtension>\\n        </extensions>\\n'
        
        point_xml += '      </trkpt>\\n'
        gpx_content += point_xml
    
    # Close GPX
    gpx_content += '''    </trkseg>
  </trk>
</gpx>'''
    
    # Write file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(gpx_content)
    
    file_size_mb = os.path.getsize(output_filename) / (1024*1024)
    print(f"✅ GPX file created: {file_size_mb:.1f} MB")
    
    return len(df)

def main():
    if len(sys.argv) < 2:
        print("Usage: python fit_recovery.py <input_fit_file> [output_gpx_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "enhanced_ride_with_power.gpx"
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        sys.exit(1)
    
    print("🚴 FIT GPS Recovery Tool")
    print("=" * 40)
    
    try:
        # Extract data from FIT file
        df = extract_fit_data(input_file)
        
        if len(df) == 0:
            print("❌ No GPS data found in FIT file")
            sys.exit(1)
        
        # Show data summary
        power_coverage = df['power'].notna().sum() / len(df) * 100
        hr_coverage = df['heart_rate'].notna().sum() / len(df) * 100
        
        print(f"⚡ Power data: {power_coverage:.1f}% coverage")
        print(f"❤️  Heart rate: {hr_coverage:.1f}% coverage")
        
        # Create enhanced GPX
        points = create_enhanced_gpx(df, output_file)
        
        print("\\n🎉 SUCCESS!")
        print(f"📁 Output file: {output_file}")
        print(f"📊 GPS points: {points:,}")
        print("📤 Ready to upload to Strava!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
