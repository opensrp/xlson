---------------------
Contributing to xlson
---------------------

Use the latest python 3 release, preferably python 3.6+.

Install required packages:

   pip install pip-tools
   pip-sync
   pre-commit install

Before submitting a pull request, run tests:

   python setup.py test

Whether fixing a bug or adding a new feature always add a test, make sure the test confirms fixing the bug or validates the feature being developed.
