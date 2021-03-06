sudo apt-get update
sudo apt-get install -y build-essential python-dev python-pip python-avahi python-dev avahi-daemon python-liblo libao4 libev4 autoconf libudev-dev libev-dev vim supervisor

sudo pip install -r requirements.txt
git submodule update

cd amcp-rpi; ./setup.py build --build-platlib=.
cd ..
sudo cp config/etc/network/interfaces /etc/network/interfaces

sudo rm -f etc/supervisor/conf.d/*
sudo cp supervisor/* /etc/supervisor/conf.d/

cp touchosc/iphone5layout.touchosc osc-server/knifefire_template.touchosc
