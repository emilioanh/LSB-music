# LSB-music
installation steps:
+Windows:(run with admin cmd)  
    pip install virtualenv  
    virtualenv -p "C:\Program Files (x86)\Python36-32\python.exe" env (inside the project folder)  
    env\Scripts\activate.bat (to activate virtualenv)  
    python manage.py runserver (in djangosettings)  
+Mac:  
    pip install virtualenv  
    virtualenv -p /Library/Frameworks/Python.framework/Versions/3.6/bin/python3 envmac  
    source envmac/bin/activate  
    python3 manage.py runserver (in djangosettings)  
    
