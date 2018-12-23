pip install -r requirements.txt
set FLASK_ENV=development
set FLASK_DEBUG=1
set TEMPLATES_AUTO_RELOAD=True
set FLASK_APP=main.py
python -m flask run --host=0.0.0.0
pause