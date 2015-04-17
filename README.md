    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    $$$$$$$$$$$$$$$$$_$$$$$$$$$$$$$$$$_$$$$$$$$$$$$$$$
    $$$$$$$$$$$$$$$$$__$$$$$$$$$$$$$$_$$$$$$$$$$$$$$$$
    $$$$$$$$$$$$$$$$$$_______________$$$$$$$$$$$$$$$$$
    $$$$$$$$$$$$$$$$___________________$$$$$$$$$$$$$$$
    $$$$$$$$$$$$$$____$$$_________$$$____$$$$$$$$$$$$$
    $$$$$$$$$$$$$_____$$$_________$$$_____$$$$$$$$$$$$
    $$$$$$$$$$$$___________________________$$$$$$$$$$$
    $$$$$$$$$$$$___________________________$$$$$$$$$$$
    $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
    $$$$_____$$$____________________________$$$____$$$
          _           _     _ _             _ _
       __| |_ __ ___ (_) __| | |_ _ __ __ _(_) |
      / _` | '__/ _ \| |/ _` | __| '__/ _` | | |
     | (_| | | | (_) | | (_| | |_| | | (_| | | |
      \__,_|_|  \___/|_|\__,_|\__|_|  \__,_|_|_|


# DroidTrail

## What is it?

Droidtrail is a python tool for executing an automatic and lightweight
vetting of malicious/legit mobile apps; for each examined app it
produces a digital footprint which is composed by these digital trails:

``<< app_title, app_version, app_package_name, app_activities_names,
     apps_services_names, apps_broadcast_receivers_names,
     app_permissions, app_min_sdk, app_target_sdk, file_name, 
     file_md5_sum, file_sha256_sum, file_dimension, CA_owner, 
     CA_issuer, CA_serial_number, CA_finger_md5, CA_finger_sha1, 
     dummy_1, dummy_2, dummy_3 >>``

The following elements are
  - expressed by single-pipe separated values:  
      *app_activities_names, apps_services_names,
      apps_broadcast_receivers_names and app_permissions;*
  - for future evolutions:  
      *dummy_1, dummy_2 and dummy_3.*


## Configuration and Installation

``$ sudo chmod 700 configure.sh``  
``$ configure.sh``


## Running

``$ sudo chmod 700 run_droidtrail.sh``  
``$ run_droidtrail.sh``


## Package composition

The package is composed by:  
  - **droidtrail**  
      - **config**: *the components that configure the entire project through a configuration file;*  
      - **dependencies**: *the components that identifies project dependencies
                      and checks if they are satisfied;*  
      - **extract**: *the components for the extraction of archives of malicious apps;*  
      - **fingerprint**: *the components for the fingerprinting of mobile apps;*  
      - **persistence**: *the components for managing the persistence of the results;*  
      - **utils**: *the collections of useful and reusable functions and methods;*  
      - **run.py**: *the main python script.;*  
  - **droidtrail.env**: *the python virtual environment dedicated to this project;*  
  - **in**: *the input folder;*  
  - **out**: *the output folder;*  
  - **lib**: *the external libraries needed by DroidTrail;*  
  - **logs**: *the log file that contains detailed information for the execution of this framework;*  
  - **run_droidtrail.sh**: *the bash script which automatise the execution of the
                       framework inside the virtual environment.*


## Todo-list

Please see the <TODO> tag disseminated in the source code;  
some grep will help you! :)


## Wish-list

t.b.d.


## Licensing

Please see the file called LICENSE.


## Contacts

bl4ckh0l3  
*bl4ckh0l3z at gmail.com*
