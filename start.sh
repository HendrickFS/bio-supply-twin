# create a virtual environment
python -m venv venv
venv/scripts/activate
# then install dependencies
pip install -r requirements.txt
# run migrations
python manage.py migrate
# create a superuser
python manage.py createsuperuser
# run the development server
python manage.py runserver