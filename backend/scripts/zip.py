import os

os.system('cd .venv/lib/python3.11/site-packages && zip -r ../../../../deployment-package.zip . -x __pycache__\*')
os.system('zip -r deployment-package.zip . -i *.py app\*.py .env')
os.system('mv deployment-package.zip volume/')