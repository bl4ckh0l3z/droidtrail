# DroidTrail - Changelog

## 0.3 (Apr 20, 2015)

###Features

  - Extract a fingerprint for each analyzed app
  - Store the trails extracted for earch analyzed app in a JSON file named trails_list.json  
  - Store the fingerprint extracted for earch analyzed app in a JSON file named fingerprints_list.json

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