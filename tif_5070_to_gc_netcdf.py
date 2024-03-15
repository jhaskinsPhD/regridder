import rioxarray
import xesmf as xe
import numpy as np
from osgeo import gdal
import xarray as xr

def _rescale_resolution(input_file:str, output_file:str, scaling_factor:float):
    """_summary_

    Args:
        input_file (str): name of the file you want to rescale
        output_file (str): name of file and location you want to rescale the file too
        scaling_factor (float): a parameter that determines how much to scale down the input file by
                                example :   0.5 will make tiffs length and width half as man pixels rounded down
                                            1 will result in the output tiff being the exact same as the input
    """
    
    #open input file
    ds = gdal.Open(input_file)

    # Calculate the new dimensions
    new_width = int(ds.RasterXSize * scaling_factor)
    new_height = int(ds.RasterYSize * scaling_factor)

    # set options
    options = gdal.WarpOptions(
        format="GTiff",
        outputType = gdal.GDT_Float32, #outputType= gdal.GDT_Int64, this needs to be changed based on what is going to be done with the data for salt I am using a float because the data may have been fractionalized when being warped.
        width=new_width,
        height=new_height,
        resampleAlg=gdal.GRA_Average,  # You can change the resampling method as needed
    )
    
    #transfor,
    gdal.Warp(output_file, ds, options=options)

    ds = None  # Close the input file

def _transform_5070_to_4326(tif_path_5070:str, tif_path_4326:str):
    """
    takes tiff input in 5070 and transforms it to 432

    Args:
        tif_path_5070 (str): path to input 5070 tif file.
        tif_path_4326 (str): path to output 4326 tif file
    """
    input_ds = gdal.Open(tif_path_5070)
    
        # set options
    options = gdal.WarpOptions(
        format="GTiff",
        outputType = gdal.GDT_Float32,
        srcSRS = "EPSG:5070", 
        dstSRS ="EPSG:4326",
        resampleAlg = gdal.GRA_Average
    )
    
    #use gdal to regrid
    gdal.Warp(tif_path_4326, input_ds, options = options) # goes from srcSRS to dstSRS
    input_ds = None #close the data set

def _convert_to_geochem_nc(tif_file_path:str, nc_output_path:str, template_ds:xr.DataArray, resampling_method):
    """creates a netcdf file from a tiff input file that is gridded in a lat/lon format

    Args:
        tif_file_path (str):path to the tif file that will be regridded and saved as a netcdf file
        nc_output_path (str): the location that the netcdf file should be saved
        template_ds (xr.array): an xarry object that represents a geo-chem compatible netcdf file
        sum_or_average (str, optional): determines wether the resulting netcdf file should be regridded based on a sum or average of the input data if input is True output will regrid based on sum if it is False the regridder will regrid based on average resampling w. Defaults to True.
    """
    if (resampling_method != "sum" and resampling_method != "average"):
        raise Exception("resampling_method must be a string representing either 'sum' or 'average' and it is ", resampling_method)

    #open file as xarray object using rioxarray
    input_ds = rioxarray.open_rasterio(tif_file_path)
    
    # I am using this with statement to try to ensure that rioxarray files are closed 
    with rioxarray.open_rasterio(tif_file_path) as input_ds:
        
        # Ensure there are no nan-values and replace all possible null values
        input_ds = input_ds.where(input_ds != input_ds._FillValue, 0) #remove fill values
        input_ds = input_ds.where(input_ds.notnull(),0) #remove Nan, None, or NaT
        
        #convert to data set
        input_ds = input_ds.to_dataset(name = "output")
    
        #rename axes so data will work with regridder
        input_ds = input_ds.rename({'x':'lon','y':'lat'})
    
        #create regrid object
        regridder = xe.Regridder(input_ds, template_ds, "conservative")
        # suggested method to fix Latitude outside of [-90,90] can be found @ https://stackoverflow.com/questions/66177931/how-do-i-resample-a-high-resolution-grib-grid-to-a-coarser-resolution-using-xesm
            
        #regrid xarray object
        regrided_ds = regridder(input_ds) 
        
        if (resampling_method == 'sum'):
            # Converting to sum like this only works because the input data is in kg on a 1 km^2 grid.
            # Because of this, when the average is taken it effectively gives the average units of kg/km^2.
            # All that needs to be done to convert from kg/km^2 to kg is to multiply each cell by its area.
            regrided_ds = regrided_ds * template_ds["AREA"] / 1e6 # the 1e6 is to convert from m^2 to km^2
        
        regrided_ds.to_netcdf(nc_output_path)
        
def tif_5070_to_gc_netcdf(fulrez_4326_path:str, lowrez_4326_path:str, output_nc_path:str, tif_5070_path:str,  template_path:str, resampling_method = "average", scaling_factor:float = 0.1):
    """
    Converts a TIFF file to a NetCDF file using a given template.

    Args:
        fulres_4326_path (str): The path to where the intermediate full-resolution TIFF will be stored in EPSG:4326 projection.
        lowres_4326_path (str): The path to where the intermediate low-resolution TIFF will be stored file in EPSG:4326 projection.
        output_nc_path (str): The path to save the output NetCDF file.
        tif_5070_path (str): The path to the input TIFF file in EPSG:5070 projection is stored.
        template_path (str): The path to the template NetCDF file.
        scaling_factor (float, optional): The scaling factor to apply during the resolution rescaling. Defaults to 0.01

    Returns:
        None

    Examples:
        tif_to_nc('fulres.tif', 'lowres.tif', 'result.nc', 'tif_5070.tif', 'template.nc', scaling_factor=0.1)
    """

    #open template
    template_ds=xr.open_dataset(template_path)
    print(f"{template_ds}")
    
    #run methods
    _transform_5070_to_4326(tif_5070_path, fulrez_4326_path)
    _rescale_resolution(fulrez_4326_path, lowrez_4326_path, scaling_factor)
    _convert_to_geochem_nc(lowrez_4326_path, output_nc_path, template_ds, resampling_method = resampling_method)

def create_mask_values_above(input_file:str, output_file:str, threshold:float):
    """
    creates mask with ones representing values over a threshold and zeros for values under and equal to the threshold
    Parameters

    Args:
        input_file (str): location of file you want to make mask of
        location that you want to save the mask to
        minimum value to be set at one
    """
    
    ds = gdal.Open(input_file)

    # convert to numpy array to minipulate
    data = ds.ReadAsArray()

    # Create a binary mask based on the threshold
    mask = (data > threshold).astype(np.uint8)

    # package array backinto a dataset
    mask_driver = gdal.GetDriverByName('GTiff')
    mask_ds = mask_driver.Create(output_file, ds.RasterXSize, ds.RasterYSize, 1, gdal.GDT_Byte)
    mask_ds.GetRasterBand(1).WriteArray(mask)

    # Set the geo referencing information for the mask
    mask_ds.SetProjection(ds.GetProjection())
    mask_ds.SetGeoTransform(ds.GetGeoTransform())

    ds = None  # Close the input file
    mask_ds = None  # Close the mask file