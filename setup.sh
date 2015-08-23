sudo apt-get install python-avahi python-dev avahi-daemon python-liblo libao4 libev4 autoconf libudev-dev libev-dev vim supervisor
pip install -r requirements.txt
git submodule init

cd amcp-rpi; ./setup.py build --build-platlib=.
cd ..
sudo cp config/etc/network/interfaces /etc/network/interfaces
