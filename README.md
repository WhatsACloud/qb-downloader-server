# About

This repo is the codebase of the server of the QB project. It is used in conjunction with qb-data-downloader-2000.
This repo is placed on the server-side, and the qb-data-downloader-2000 (on client-side) queries it.

# How to set up this project

## 1. Setting up virtual environment

### Windows
```
py -m venv env # creates virtual environment
.\env\Scripts\activate # enters virtual environment
```

### linux / mac
```
python3 -m venv env # creates virtual environment
source env/bin/activate # enters virtual environment
```

## 2. installing dependencies

```
pip3 install -r requirements.txt
```

## 3. start this project

### Windows
```
py manage.py runserver
```

### linux / mac
```
python3 manage.py runserver
```


## 4. exiting virtual envrionment
```
deactivate
```

# Useful tutorials

Set up django application on CPanel - https://www.youtube.com/watch?v=h2w8oNw_W80