# LSB-music
installation steps:
+Windows:(run with admin cmd)  
    pip install virtualenv  
    virtualenv -p "C:\Program Files (x86)\Python36-32\python.exe" env (inside the project folder)  
    env\Scripts\activate.bat (to activate virtualenv)  
    python manage.py runserver (in djangosettings)  
    install google clientapi: pip install --upgrade google-api-python-client (note install when env is activated)
+Mac:  
    pip install virtualenv  
    virtualenv -p /Library/Frameworks/Python.framework/Versions/3.6/bin/python3 envmac  
    source envmac/bin/activate  
    python3 manage.py runserver (in djangosettings)  

run steps:  
    activate env (or envmac)  
    if first time with DB then run "py manage.py makemigrations" follow with "py manage.py migrate"  
    if change DB (suggest that delete sqlite and migration in migration folder note: do not delete __init__.py)  
    then just run makemigrations and migrate again  