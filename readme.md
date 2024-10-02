
#My first flask app#

Here all all the important concepts to learn 

to create venv (Virtual Environment)-
python -m venv venv

To activate virtual environment-
.\venv\Scripts\activate

to run flask app-
flask run 

To let the server refresh everytime a change is encountered ensure this-
pip install python-dotenv
make a file called .flaskenv
FLASK_APP=app
FLASK_DEBUG=1
flask run

starting with @ , decorator

to not let pycache files to be build _pycache_ files -
PYTHONDONTWRITEBYTECODE=1

MVC Architecture
Model View Controller 


from package/filename import required_entity

To make any folder a package - 
make a file named 
__init__.py
in it write 
__all__ = [] ---> all files name inside the package
or write 
__all__=[os.path.basename(f)[:-3] for f in glob.glob(os.path.dirname(__file__) + "/*.py")] --->it just adds all .py files in the package in the list

or you can just manually import -
from package import file name

in the files do add the app(global app.py)-
from app import app

to import a class from a package's some file - 
from package import file.class

SQL Database
pip install mysql-connector-python