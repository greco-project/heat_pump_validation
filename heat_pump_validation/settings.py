def init():
    path_to_server = '/home/sabine/rl-institut'
    path_to_data_server = '/home/sabine/Daten_flexibel_01'

# raw data
global path_era5_netcdf, open_FRED_pkl, era5_path
    path_era5_netcdf = path_to_data_server + '/Wetterdaten/ERA5/'
    open_FRED_pkl = path_to_data_server + '/open_FRED_Wetterdaten_pkl/'
    era5_path = path_to_server + '/04_Projekte/163_Open_FRED/03-Projektinhalte/AP7 Community/paper_data/weather_data/'