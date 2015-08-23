sudo apt-get install python-avahi python-dev supervisor avahi-daemon python-liblo libao4 libev4 autoconf libudev-dev libev-dev mpg123 vim
pip install -r requirements.txt
git submodule init

cd amcp-rpi; ./setup.py build --build-platlib=.
