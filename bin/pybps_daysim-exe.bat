::Batch file created for DAYSIM 3.1b (beta)
::Date: April 2, 2012 6:12:38 PM CEST

@echo off
if "%1" == "" goto error
rem - process each of the named files
goto end
:error
echo missing argument!
echo usage  pybps_daysim-exe file1.hea
EXIT /B
:end

set "DAYSIMPATH=C:\DAYSIM\bin_windows\"
set "CURRDIR=%cd%"
set "FILENAME=%1"

::Calculate Daylight Coefficients File(s)(*.dc)
::=============================================
:: Files are stored under res/*.dc
%DAYSIMPATH%gen_dc %FILENAME%

::Generate Illuminance File (*.ill)
::=================================
:: Files are stored under res/*.ill
%DAYSIMPATH%ds_illum %FILENAME%

::Generate Glare Profile (*.dir)
::==============================
:: Files are stored under res/*.dir
%DAYSIMPATH%gen_directsunlight %FILENAME%

::Generate Daylight Autonomy (*.da)
::=================================
:: Files are stored under res/*.da
%DAYSIMPATH%ds_autonomy %FILENAME%

::Generate Daylight Factor (*.df)
::===============================
:: Files are stored under res/*.df
%DAYSIMPATH%ds_dayfactor %FILENAME%

::Generate Electric Light Illuminance Profiles (*.df)
::===================================================
:: Files are stored under res/*.el.htm
%DAYSIMPATH%ds_el_lighting %FILENAME%

::Daylight Glare Probability profile(s) are not calculated.