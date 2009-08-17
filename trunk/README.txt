Getting started

Edit ~/.bashrc and add

export PYTHONPATH=$PYTHONPATH:/<path to pynappl>/src

You can then apply these changes to your current shell session by executing 

source ~/.bashrc

Run the unit tests from the /tests directory:

python all_tests.py
