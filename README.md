# SteamFreeGamePublicList
An Python-based program get latest Steam free game and redeem through ASF automatically  
Free Game infomation from [SteamDB.info][3]

# Requirement
- Python 3
- PHP > 7.0
- MySQL
```
pip3 install request requests json chardet bs4 MySQLdb re
```

# How to Use
- Follow the instruction of [ArchiSteamFarm][1] installation
- Enable IPC and Headless mode in ASF
- Improt [steamdb.sql][2] into your database
- Change the db and ASF info in main.py and index.php
- run main.py manually or set it in crontab

[1]:https://github.com/JustArchiNET/ArchiSteamFarm
[2]:https://github.com/Masterain98/SteamFreeGamePublicList/blob/master/steamdb.sql
[3]:https://steamdb.info/upcoming/free