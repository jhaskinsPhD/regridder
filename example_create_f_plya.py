from tif_5070_to_gc_netcdf import tif_5070_to_gc_netcdf
from tif_5070_to_gc_netcdf import create_mask_values_above

fulrez_4326_path = r"examples/example_data/create_f_plya_intermediate_data/fulrez_4326.tif"
lowrez_4326_path = r"examples/example_data/create_f_plya_intermediate_data/lowrez_4326.tif"
output_nc_path = r"examples/example_data/create_f_plya_output_data/output_nc.tif"
input_tif_5070_path = r"examples/example_data/1992_salt_estimate.tif"
template_path = r"examples/example_data/dust_emissions_05.20210906.nc"
scaling_factor = 0.01

mask_5070 = r'examples/example_data/create_f_plya_intermediate_data/mask_5070.tif'

threshold = 10
create_mask_values_above(input_tif_5070_path, mask_5070, threshold)

tif_5070_to_gc_netcdf(fulrez_4326_path, lowrez_4326_path, output_nc_path,
                      mask_5070, template_path, resampling_method="average", scaling_factor=scaling_factor)