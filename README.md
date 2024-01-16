# Current Data Flow to Prepair gSSURGO Data for Geos-Chem
1. Download Data from the gSSURGO Database 
    1. Data Download Source: **[https://www.nrcs.usda.gov/](https://www.nrcs.usda.gov/resources/data-and-reports/gridded-soil-survey-geographic-gssurgo-database)**
        1. The data is separated into States/CONUS (continental US) it is probably ok to use CONUS because the resolution is high enough. CONUS data @ **https://nrcs.app.box.com/v/soils/folder/233395259341**
2. Open Raw Files in ArcMap 
    1. Follow instructions in the gSSURGO Guide for Creating Soil Maps and Rasters. See section 2 "Creating Soil Map" in the PDF hosted by USDA **https://www.nrcs.usda.gov/sites/default/files/2022-08/gSSURGO_Mapping_DetailedGuide.pdf**
    2. Export the map made in ArcMAP as a GeoTIFF file.
        1. Expect this file to be about 10-15Gb
        2. The file should ONLY contain the soil data you selected while following the gSSURGO guid.
        3. This exported file is no longer in a polygon format but is gridded as a raster in CRS ESPG5070 (ESPG5070 is gridded in meters, and is only accurate over the United States).
3. Convert .tif File to .nc File by Running tif_to_nc.py
    1. This file can be found in this GitHub repository
    2. For this file to run, you must change at least one parameter: 
        1. The file paths on lines 151 -  156. Changing these will change what tiff you are rescaling and where output files will be saved.
    3. Additionally, you may change 3 more parameters:
        1. The template file path (a file stored in this repository). Changing this variable will change what grid the input data is gridded to.
        2. The threshold on line 163. Changing this value will set the minimum EC to be included final .nc file.
        3. The scaling_factor on line 164. Changing this value will adjust the resolution of the intermediate tiff file created before data is saved to the final output .nc file.
             1. This value should be kept as close to 1 as possible while still allowing the program to run. If the value is too high, sometimes the script will crash depending on the sizes of the input files.
    4. tif_to_nc.py runs in four steps
        1. First, tif_to_nc.py creates a tiff file that is a binary mask. This binary mask contains 1 for locations that have an EC over the threshold and 0 for locations that have EC at or below the threshold
        2. Second, tif_to_nc.py creates a tiff file stored in the same coordinate reference system (crs) that goeschem uses. 
        3. Third, tif_to_nc.py scales down the data based on the scaling factor so it can be gridded without crashing. It saves a lower-resolution mask.
        4. Fourth, tif_to_nc.py re-grids the data to the same scale that the template file is in.
