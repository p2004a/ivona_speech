IVONA TTS reader
================

Simple python3 application that reads aloud every line you type in STDIN using
IVONA Speech Cloud. It also provides a simple spelling fixer using aspell.

I tested it under Python 3.5. It works fine for English, Polish and should
also work for many other languages (but I didn't tested).

Why?
----

I was ill (and bored) and I couldn't speak because of a problem with vocal
cords so I created this simple application to help me communicate more easily
with people around me in home. I tried to use eSpeak but I wasn't satisfied
with the quality of a generated sound.

Setup
-----

You need to install gstreamer python3 bindings in your system.
The spelling fixer requires libaspell installed.
For example in Ubuntu or debian you can install them with:

    $ sudo apt install python3-gst-1.0 libaspell-dev

Then set up python3 virtual env and install dependencies.

    $ python3 -m venv --system-site-packages env
    $ source env/bin/activate
    (env) $ pip install -r requirements.txt

Usage
-----

First you need to create IVONA developer account, generate credentials and and
set them in environment variables:

    $ export IVONA_SECRET_KEY="secretsecretsecretsecretsecret"
    $ export IVONA_ACCESS_KEY="asdasdasdasdasdasdasd"

You can also set nearest region by setting `IVONA_REGION` env variable.
Available ones:

  - `eu-west-1`: EU, Dublin (default one)
  - `us-east-1`: US East, N. Virginia
  - `us-west-2`: US West, Oregon

Then in the virtual env run

    (env) $ python3 ivona_speech.py --help

to get all runtime options.

### Tips

 - By placing `!` at the beginning of line you disable spelling fixer for that line.

### Example

    (env) $ python ivona_speech.py -l pl-PL
    0 Voice(name='Agnieszka', language='pl-PL', gender='Female')
    1 Voice(name='Jacek', language='pl-PL', gender='Male')
    2 Voice(name='Ewa', language='pl-PL', gender='Female')
    3 Voice(name='Jan', language='pl-PL', gender='Male')
    4 Voice(name='Maja', language='pl-PL', gender='Female')
    voice number> 2
    Selected voice: Voice(name='Ewa', language='pl-PL', gender='Female')
    Cześć, nazywam się Ewa
    bład
    fixed: błąd
    ! bład      
    .q
