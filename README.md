# wename

# Use either Python 3.6.2 or Python 3.7.
# Make sure pip3 and python 3 are installed on your machine

python3 -m pip install --user --upgrade pip
python3 -m pip install --user virtualenv

# to create the virtual env with the name .env
python3 -m virtualenv .env

# to enter the virtual env
source .env/bin/activate

# to install 3rd party dependencies
pip install -r requirements.txt

# to update 3rd party dependencies
pip freeze > requirements.txt

# to leave the virtual env
deactivate