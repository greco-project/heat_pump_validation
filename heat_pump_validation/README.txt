Oemof Version für calc_eer_zeroDivision (which is not used anymore):
5b1857c8ee60f02c82a956e45c04dc52e364dba0


script used to calculate the RMSE:
feedin_germany - validation_tools.py
bias corrected = False
normalized = False

script used to calculate COP/EER:
oemof - compression_heatpumps_and_chillers.py
Oemof version: 26fe678b2a702b35160e8afb0a7f8d71314b16c2
Path:src/oemof/thermal/compression_heatpumps_and_chillers.py


1. pre_processing: If integral fan or compressor shuts down
2. calc_cop: resamples data if necessary and calculates COP
3. temphub: optional
4. Plots and Linear_Regression: Calculates temphub if needed as well as residuals
