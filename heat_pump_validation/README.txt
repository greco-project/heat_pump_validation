Oemof Version für calc_eer_zeroDivision (which is not used anymore):
5b1857c8ee60f02c82a956e45c04dc52e364dba0

Instead of the data, which has originally been used for the validation, dummy data has been provided.
It is located in the directory "raw_data". Running the scripts will generate results in the directory
"results". Please note the order of execution under "Usage order for validation of Chiller_ / HP_".

Script used to calculate the RMSE:
feedin_germany - validation_tools.py
bias corrected = False
normalized = False

Script used to calculate COP/EER:
oemof - compression_heatpumps_and_chillers.py
Oemof version: 26fe678b2a702b35160e8afb0a7f8d71314b16c2
Path:src/oemof/thermal/compression_heatpumps_and_chillers.py


Usage order for validation of Chiller_ / HP_:
1. pre_processing: Cleans data if integral fan or compressor shuts down and if naming not consistent
2. calc_cop: Resamples data if necessary and calculates COP
3. Temphub: Calculates the temperature hub and saves final data to csv
4. Residuals: Calculates and plots the residuals
5. Linear_Regression: Plots linear regression
6. Histogram: Plots histogram of residuals
7. RMSE: Calculated root mean square error
