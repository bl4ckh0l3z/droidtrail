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

DroidTrail is a modular python tool intended to serve as a framework for executing 
an automatic and lightweight vetting of malicious/legit android apps; 
for each analyzed app it produces a digital footprint which is composed by more 
than 20 descriptive trails (e.g. package, permissions, activities, services, receivers, digital 
certificate summary, file descriptors, etc); each trails-set is summarized and uniquely
identified by a fingerprint. Fingerprints and trails can be extracted in short/long mode
and saved in different file format (i.e. JSON, CSV and XML).  

This is an example of digital footprint extracted for the ZitMo (Zeus-in-the-mobile) mobile malware:

``{"trails": [  
        {  
            "app_trails": {  
                "app_activities_names": "com.android.security.MainActivity",  
                "app_version": "4.3",  
                "app_name": "Android Security Suite Premium",  
                "app_target_sdk": 16,  
                "app_package_name": "com.android.security",  
                "app_permissions": "android.permission.SEND_SMS|android.permission.BROADCAST_STICKY|android.permission.SYSTEM_ALERT_WINDOW|android.permission.INTERNAL_SYSTEM_WINDOW|android.permission.ADD_SYSTEM_SERVICE|android.permission.VIBRATE|android.permission.REORDER_TASKS|android.permission.CHANGE_CONFIGURATION|android.permission.WAKE_LOCK|android.permission.STATUS_BAR|android.permission.ACCESS_WIFI_STATE|android.permission.READ_PHONE_STATE|android.permission.MODIFY_PHONE_STATE|android.permission.DEVICE_POWER|android.permission.DISABLE_KEYGUARD|android.permission.INTERNET|android.permission.WRITE_APN_SETTINGS|android.permission.WRITE_SMS|android.permission.BROADCAST_WAP_PUSH|android.permission.CHANGE_WIFI_STATE|android.permission.ACCESS_NETWORK_STATE|android.permission.CHANGE_NETWORK_STATE|android.permission.RECEIVE_BOOT_COMPLETED|android.permission.READ_SMS|android.permission.RECEIVE_SMS|android.permission.BROADCAST_SMS|android.permission.WRITE_SETTINGS|android.permission.ACCESS_WIFI_STATE|android.permission.UPDATE_DEVICE_STATS|android.permission.CHANGE_WIFI_STATE|android.permission.WAKE_LOCK|android.permission.READ_PHONE_STATE|android.permission.WRITE_SECURE|android.permission.WRITE_SECURE_SETTINGS|android.permission.WRITE_EXTERNAL_STORAGE|android.permission.PROCESS_OUTGOING_CALLS",  
                "app_max_sdk": 19,  
                "app_libraries_names": "None",  
                "app_main_activity_name": "com.android.security.MainActivity",  
                "app_receivers_names": "com.android.security.SecurityReceiver",  
                "app_min_sdk": "7",  
                "app_services_names": "com.android.security.SecurityService"  
            },  
            "cert_trails": {  
                "cert_finger_sha1": "E2D22CA65F8F2FEBB19493BC9B72369A6216A1FB",  
                "cert_subject": "Subject: C=US, CN=Android Debug, DN=C=US, O=Android, CN=Android Debug, E=, L=, O=Android, OU=, S=",  
                "cert_serial_number": "4ED0AC83",  
                "cert_issuer": "Issuer: C=US, CN=Android Debug, DN=C=US, O=Android, CN=Android Debug, E=, L=, O=Android, OU=, S="  
            },
            "file_trails": {
                "file_name": "d1cf8ab0987a16c80cea4fc29aa64b56.apk",  
                "file_sha256_sum": "302c060432907e506643d39b7981df16a61c61b84981bcec379fa8c5b2ec6a99",  
                "file_dimension": 207489,  
                "file_md5_sum": "d1cf8ab0987a16c80cea4fc29aa64b56"  
            }  
        }  
    ]}``

The following elements are expressed by single-pipe separated values: *app_activities_names,
app_services_names, app_receivers_names, app_libraries_names, and app_permissions;*  

The trails-set reported above can be summarized and uniquely identified by DroidTrail 
through this fingerprint:

``{  
    "fingerprints": [  
        {  
            "index": "27ce9cf737d01b0bdd5fd6645bce8a06",  
            "elem": "bbfdf3f1eb959ecd0c46786fbf7508923e9cf837dcb41204dce6096fa8106e94"  
        }  
    ]  
}``


## Configuration and Installation

``$ sudo chmod 700 configure.sh``  
``$ configure.sh``


## Running

``$ sudo chmod 700 run_droidtrail.sh``  
``$ run_droidtrail.sh -h``  
``$ run_droidtrail.sh -t -f -m long -o csv``


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
      - **trails**: *the components for the extraction of digital trails;*  
      - **run.py**: *the main python script.;*  
  - **droidtrail.env**: *the python virtual environment dedicated to this project;*  
  - **in**: *the input folder;*  
  - **out**: *the output folder;*  
  - **lib**: *the external libraries needed by DroidTrail;*  
  - **logs**: *the log file that contains detailed information for the execution of this framework;*  
  - **run_droidtrail.sh**: *the bash script which automatise the execution of the
                       framework inside the virtual environment.*


## Todo-list

  - Improve strings encode/decode  
  - Develop stats components
  - Update package composition
Please see the TODO tag disseminated in the source code;  
some grep will help you! :)


## Licensing

Please see the file called LICENSE.


## Contacts

bl4ckh0l3  
*bl4ckh0l3z at gmail.com*
