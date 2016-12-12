IVONA speech
============

Python3 speech synthesis using IVONA.

Setup
-----

You need to install gstreamer python3 bindings in your system.
The spelling fixer requires libaspell installed.
For example in Ubuntu or debian you can install them with:

    $ sudo apt install python3-gst-1.0 libaspell-dev

Set up python3 virtual env and install dependencies.

    $ python3 -m venv --system-site-packages env
    $ source env/bin/activate
    $ pip install -r requirements.txt
