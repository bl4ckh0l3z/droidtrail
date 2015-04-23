# DroidTrail - Changelog

## 0.4 (Apr 21, 2015)

###Features

  - Store the trails extracted for each analyzed app in a CSV file 
    trails_list.csv, located in the out directory  
  - Store the fingerprint extracted for each analyzed app in a CSV file 
    fingerprints_list.csv, located in the out directory
  - Store the trails extracted for each analyzed app in a XML file 
    trails_list.xml, located in the out directory  
  - Store the fingerprint extracted for each analyzed app in a XML file 
    fingerprints_list.xml, located in the out directory    
  - Added cmd line option for the selection of (i) trails extraction, 
   (ii) fingerprints extraction, (iii) mode for trails/fingerprints extraction
   (i.e. long, short) and (iv) output format (i.e. json, csv, xml)

###Fixes

  - Fixed null-return value for APK functions  
  - Fixed null-return value for get_max_sdk_version, get_min_sdk_version and get_target_sdk_version  
  - Fixed duplicate trails problem  
  - Fixed duplicate fingerprints problem

## 0.3 (Apr 20, 2015)

###Features

  - Extract a fingerprint for each analyzed app
  - Store the trails extracted for earch analyzed app in a JSON file 
    trails_list.json, stored in the out directory  
  - Store the fingerprint extracted for earch analyzed app in a JSON file 
    fingerprints_list.json, stored in the out directory

## 0.2 (Apr 19, 2015)

###Features

  - Extract trails for each analyzed app  

## 0.1 (Apr 17, 2015)

###Features

  - Extract mobile apps (*.apk) from compressed archives (i.e. zip, 7z,
    rar, tar, tar.gz) protected with or without a common password
    (i.e. infected, infected666, infected666<last-digit-before-extension>).
  - Scrapes out APK files thanks to an efficient composite heuristic
    by mean of checking magic number and the existence of apk well-known
    resources; non-matching files are removed before analyzing their
    digital trails.
  - Save every extracted mobile app in the out folder; each file is renamed
    to its md5 hash.