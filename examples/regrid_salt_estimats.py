from tif_5070_to_gc_netcdf import tif_5070_to_gc_netcdf

#############################################################################################
#Make it so all of these can be input to one folder
#@Jhaskins phd PyTUV util
save_path = r"examples/example_data"
fulrez_4326_path = r"examples/example_data/regrid_salt_intermediate_data/fulrez_4326.tif"
lowrez_4326_path = r"examples/example_data/regrid_salt_intermediate_data/lowrez_4326.tif"
output_nc_path = r"examples/example_data/regrid_salt_output_data/output_nc.tif"
##############################################################################################

# output_dict = create_output_dir(path_to_output_folder) #put inside of tif_to_nc

# add before and after plot function see make todd figs see make todd figs
        #will be difficult to run on on 

# test how much memory that it needs to run

# create function to show total error

input_tif_5070_path = r"examples/example_data/1992_salt_estimate.tif"
template_path = r"examples/example_data/dust_emissions_05.20210906.nc"
scaling_factor = 1

#output_dir tif_to_nc(output_dict, )

tif_to_nc(fulres_4326_path, lowres_4326_path, output_nc_path, input_tif_5070_path, template_path, scaling_factor=scaling_factor)