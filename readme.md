python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
python manage.py collectstatic
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

и запускается на localhost:8000