Create a virtual environment with "python -m venv venv" then activate the venv via "venv/Scripts/activate. 

Download all pips from the requirements.txt with "pip install -r requirements.txt" (must be in backend directory). 

Initialize the database with "flask db init" then migrate and update with "flask db migrate -m "initial migration" and "flask db upgrade". 

Run "flask run" or "python app.py" to run the backend.
