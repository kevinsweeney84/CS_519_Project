# CS_519_Project
Dash app using VTK Toolkit to visualise a Delaunay mesh for 2D/3D data

# To run

- Set up Python virtual environment
    - In terminal: navigate to folder `.../CS_519_Project/`
    - Install a virtual environment:  `virtualenv -p python3 venv` *[NOTE: Only needs to be performed on first run]*
    - Activate virtual environment: `source venv/bin/activate` (Mac) `.\venv\Scripts\activate` (Windows)
    - Install all required packages: `pip install -r requirements.txt -v`

- Run Dash App
    - Open a terminal: navigate to folder `.../CS_519_Project/`)
    - Activate virtual environment: `source venv/bin/activate` (Mac) `.\venv\Scripts\activate` (Windows)
    - Run `python app.py`
    - The terminal output will specify where the dash app is running: probably `http://127.0.0.1:8050/`
