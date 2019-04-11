# Zero Connected Home

## Hardware list
- Raspberry Pi 3B+ (with power adapter)
- Micro SD card and a micro SD to SD adapter
- Ethernet cable

## Setup

It is assumed you have a Windows computer with internet connection and micro SD card reader.

### Install Raspbian and SSH to your Raspberry

We want to flash the Raspbian OS on the mirco SD card. This version of *Zero* has been tested with Raspbian Stretch (Desktop version 2018-06-27 release). The steps described below correspond to the headless installation mode (without screen) with ethernet connection to your home network.

- Download Raspbian [here](https://www.raspberrypi.org/downloads/raspbian/).
- Extract to a new folder, you will have a single `.img` image file.
- Download and install Etcher [here](https://www.balena.io/etcher/). We use it to flash the image file on the micro SD card.
- Launch Etcher, select the Raspbian image file, select the SD card and flash the OS on it.
- In the boot partition, simply add a file named `ssh`. We are enabling ssh connections to our raspberry.
- Insert the micro SD card into the Raspberry Pi, connect the power adapter and connect to the home network via ethernet.
- Open a web browser and connect to your router (e.g., go to [fritz.box](fritz.box) for FRITZ!Box users) to find the IP address of your Raspberry.
- Download Putty and connect to your Raspberry. the default username is `pi` and password is `raspberry`.

### Setup the shared folder

- From the command line `sudo apt-get install`, `sudo apt-get install vim` and `sudo apt-get install samba`
- Create the folder `/home/pi/share`
- Edit the Samba configuration file `sudo vim /etc/samba/smb.conf`, change the line `workgroup = WORKGROUP` to match the Windows workgroup (default in Windows 10 is `WORKGROUP`, so no changes are needed), uncomment and change the line `wins support = no` to `wins support = yes`. Finally, append the following lines:
```
[pishare]
 comment=Raspberry Pi Shared Folder
 path=/home/pi/share
 browseable=Yes
 writeable=Yes
 only guest=no
 create mask=0770
 directory mask=0770
 public=yes
 force user = pi
 force guest = pi
 security = share
```
- You should be able to access it from Windows explorer under `\\RASPBERRYPI\pishare`

### Install Python, Pip and Virtualenv and clone the repository

- Install Python `sudo apt-get install python3.5`
- Install Virtualenv `sudo pip3 install virtualenv``
- Create virtual environment `virtualenv zenv` and activate it `source ~/share/zenv/bin/activate`
- Create the folder `~/share/app` and clone the git repository in it `git clone https://github.com/jahsue78/zero.git`
- Install vlc `sudo apt-get install vlc`
- Install requirements `pip install -r requirements.txt`





