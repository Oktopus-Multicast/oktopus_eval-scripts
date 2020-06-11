#  Oktopus' Performance Evaluation
In the current directory, there is a script, "ramese_script.sh", to run service chain app in ramses. The script will generate the dataset, run the application, and plot the charts. 
Before running the script, there are a couple variables to be set in the script. 

TEST_DIR - The directory where the dataset will be generated.

CSV_FILENAME - The name of the csv file, where the data will be logged.

CHART_DIR - The directory where the charts will be generated.

After the setting the variables, run:

    ./ramses_script.sh
    
To configure the control parameters, change the following variables in the "parallel_run_distributed.py" file.

EXP_MCAST_SESSIONS - the array of the number of sessions.

PER_SESSIONS_WITH_SFC - the array of the percentage of sessions with the service chain.

LENGTH_SER_CHAIN - the array of the length of the service chain.

ORD_TYPE - the array of the order type of service chain.

AUXILIARY_SER_AVAIL_P - the array of the percentage of auxiliary service function deployed.

## Create Evaluation Plot

The create_plot file creates the plots from the csv files and the data files.

    python create_plot.py sc --csv <csv_file> --dir <dir> [-o <output_dir>] 

  -- csv (CSV File): The CSV log file.
  --dir (Data directory): The data directory is where the logs are created.
  -o (Output directory): The directory that the plots will be created.
  
 ### Allocation Experiments
Change the REPRE_SAMPLE variable in create_plot file to the following.

    REPRE_SAMPLE = {'num_sessions':{'num_sessions': True, 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'service_chain_len':{'num_sessions': [4000], 
                            'service_chain_len': True, 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'percentage_sessions_with_services':{'num_sessions': [4000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':True, 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'chain_order_type':{'num_sessions': [4000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':True, 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'receivers_per':{'num_sessions': [4000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':True, 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'bandwidth_per':{'num_sessions': [4000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':True, 
                            'aux_ser_avail_p':[0.25]},
                    'aux_ser_avail_p':{'num_sessions': [4000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':True},
    }
    
Run the following command:

    python create_plot.py sc --csv output/iptv_all.csv --dir /NSL/nsl-data/carlosl_data/oktopus/iptv/ -o <output_dir>
    
 - /NSL/nsl-data/carlosl_data/oktopus/iptv/ is the location of the data in the NSL storage.
 - <output_dir> is the location where the plots are generated.


 ### Objective Optimization Experiments
Change the REPRE_SAMPLE variable in create_plot file to the following.

    REPRE_SAMPLE = {'num_sessions':{'num_sessions': True, 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'service_chain_len':{'num_sessions': [1000], 
                            'service_chain_len': True, 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'percentage_sessions_with_services':{'num_sessions': [1000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':True, 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'chain_order_type':{'num_sessions': [1000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':True, 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'receivers_per':{'num_sessions': [1000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':True, 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':[0.25]},
                    'bandwidth_per':{'num_sessions': [1000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':True, 
                            'aux_ser_avail_p':[0.25]},
                    'aux_ser_avail_p':{'num_sessions': [1000], 
                            'service_chain_len': ['variable'], 
                            'percentage_sessions_with_services':[100], 
                            'chain_order_type':[1], 
                            'receivers_per':['variable'], 
                            'bandwidth_per':['variable'], 
                            'aux_ser_avail_p':True},
    }
    
Run the following command:

    python create_plot.py sc --csv output/vod.csv --dir /NSL/nsl-data/carlosl_data/oktopus/vod/ -o <output_dir>
    
 - /NSL/nsl-data/carlosl_data/oktopus/vod/ is the location of the data in the NSL storage.
 - <output_dir> is the location where the plots are generated.
 
