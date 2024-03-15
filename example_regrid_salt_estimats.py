from tif_5070_to_gc_netcdf import tif_5070_to_gc_netcdf

fulrez_4326_path = r"examples/example_data/regrid_salt_intermediate_data/fulrez_4326.tif"
lowrez_4326_path = r"examples/example_data/regrid_salt_intermediate_data/lowrez_4326.tif"
output_nc_path = r"examples/example_data/regrid_salt_output_data/output_nc.tif"
input_tif_5070_path = r"examples/example_data/1992_salt_estimate.tif"
template_path = r"examples/example_data/dust_emissions_05.20210906.nc"
scaling_factor = 1

tif_5070_to_gc_netcdf(fulrez_4326_path, lowrez_4326_path, output_nc_path, input_tif_5070_path, template_path, scaling_factor=scaling_factor)