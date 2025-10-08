# Activate the virtual environment
venv/scripts/activate

# Install dependencies
pip install -r requirements.txt

# Make migrations and migrate the database
python manage.py makemigrations
python manage.py migrate

# Run the development server
python manage.py runserver