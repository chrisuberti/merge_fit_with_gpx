@echo off
echo FIT GPS Recovery Tool - Windows Batch Version
echo ============================================
echo.

if "%1"=="" (
    echo Usage: fit_recovery.bat [input_fit_file] [output_gpx_file]
    echo Example: fit_recovery.bat data\ride.fit enhanced_ride.gpx
    echo.
    echo If no arguments provided, will look for FIT files in data\ folder
    pause
    exit /b 1
)

set INPUT_FILE=%1
set OUTPUT_FILE=%2

if "%OUTPUT_FILE%"=="" (
    set OUTPUT_FILE=enhanced_ride_with_power.gpx
)

echo Input: %INPUT_FILE%
echo Output: %OUTPUT_FILE%
echo.

python fit_recovery.py "%INPUT_FILE%" "%OUTPUT_FILE%"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ SUCCESS! GPX file created: %OUTPUT_FILE%
    echo 📤 Ready to upload to Strava!
) else (
    echo.
    echo ❌ Error occurred during processing
)

echo.
pause
