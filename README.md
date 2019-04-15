# Zero Connected Home

Snowboy + Google Speech Streaming API.

## Hardware list
- Raspberry Pi 3B+ (with power adapter)
- Micro SD card and a micro SD to SD adapter
- Ethernet cable
- Jabra SPEAK 510 USB (microphone+speaker for the smart assistant)
- Speaker (3.5 mm jack for the music)

## Setup

This version of *Zero* has been tested with Raspbian Stretch (Desktop version 2018-06-27 release). The steps described below correspond to the headless installation mode (without screen) with ethernet connection to your home network. The Raspbian OS is flashed on the mirco SD card from a Windows computer with internet connection and micro SD card reader.

### Install Raspbian, setup SSH and VNC

- Download Raspbian [here](https://www.raspberrypi.org/downloads/raspbian/).
- Extract to a new folder, you will have a single **.img** image file.
- Download and install Etcher [here](https://www.balena.io/etcher/). We use it to flash the image file on the micro SD card.
- Launch Etcher, select the Raspbian image file, select the SD card and flash the OS on it.
- In the boot partition, simply add a file named **ssh**. We are enabling ssh connections to our raspberry.
- Insert the micro SD card into the Raspberry Pi, connect the power adapter and connect to the home network via ethernet.
- Open a web browser and connect to your router (e.g., go to [fritz.box](fritz.box) for FRITZ!Box users) to find the IP address of your Raspberry.
- Download Putty and connect to your Raspberry. the default username is **pi** and password is **raspberry**.
- Enable VNC `sudo raspi-config`, **Interfacing Options** > **VNC** > **Yes**

### Setup the shared folder

- From the command line `sudo apt-get update` and `sudo apt-get install samba`
- Create the folder `/home/pi/share`
- Edit the Samba configuration file `sudo vim /etc/samba/smb.conf`, change the line `workgroup = WORKGROUP` to match the Windows workgroup (default in Windows 10 is **WORKGROUP**, so no changes are needed), uncomment and change the line `wins support = no` to `wins support = yes`. Finally, append the following lines:
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
- You should be able to access it from Windows under **\\RASPBERRYPI\pishare**

### Install the dependencies and clone the repository

- Install Python `sudo apt-get install python3.5` and Virtualenv `sudo pip3 install virtualenv`
- Create virtual environment `virtualenv zenv` and activate it `source ~/share/zenv/bin/activate`
- Create the folder `~/share/app` and clone the git repository in it `git clone https://github.com/jahsue78/zero.git`
- Install packages `sudo apt-get install vlc portaudio19-dev libatlas-base-dev pulseaudio libttspico-utils sox`
- Install the Pip requirements `pip install -r requirements.txt`

### Add the Google credentials

- Create the folder `~/share/app/cred`
- For each of the following links, follow the steps until you got your private key:
      - Go to the [Google Speech-to-Text API](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) page, click on **SET UP A PROJECT** and follow the steps until you got your private key as a  JSON file
      - Go to the Youtube Data API [here](https://developers.google.com/youtube/v3/getting-started) page and follow the steps until you got your private key as a JSON file
      - Go to the [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) page, click on **ENABLE THE GOOGLE SHEETS API** and follow the steps until you got your private key as a  JSON file
- Add the 3 JSON files to the folder `~/share/app/cred`

### Configure and start *Zero*
- Configure Pulse Audio `mkdir ~/.config/pulse`, `cp ~/share/app/zero/config/daemon.conf ~/.config/pulse`
- Rename `config_example.ini` to `config.ini` and modify it to match your configuration
   - Modify the **IP** parameter to match the Raspberry IP address in your home network
   - Modify the fields **KEY_GSPEECH** (Google Speech-to-Text API),  **KEY_GYTB** (Youtube Data API), **KEY_GSHEET** (Google Sheets API) to match the file names of your private keys in `~/share/app/cred`
   - Execute `python ~/share/app/zero/modules/util.audio.py`, you should see something similar to this:
   ```
   ==============================================
   >>> Speech configuration:
   (0, 'bcm2835 ALSA: - (hw:0,0)', 0)
   (1, 'bcm2835 ALSA: IEC958/HDMI (hw:0,1)', 0)
   (2, 'Jabra SPEAK 510 USB: Audio (hw:1,0)', 1)
   (3, 'sysdefault', 0)
   (4, 'dmix', 0)
   (5, 'default', 32)
   ==============================================
   >>> Player configuration:
   (0, 'alsa_output.platform-soc_audio.analog-stereo', 'hw:0,0')
   (1, 'alsa_output.usb-0b0e_Jabra_SPEAK_510_USB_745C4B89B3ED021900-00.analog-stereo', 'hw:1,0')
   ```
   - Modify the *Speech* device ID **SPEECH_DEVICE** with the one corresponding to your device (e.g., the *Jabra SPEAK 510* device has the ID 2)
   - Modify the *Player* device ID **PLAYER_DEVICE** with the one corresponding to your device (e.g., the *alsa_output.platform-soc_audio.analog-stereo* device has ID 0)
   - The devices should be different, the first one is used as microphone and speaker for the voice assistant and the second one as speaker for the music player
- From a shell opened with through a VNC session `cd ~/share/app/zero` and launch *Zero* `./main.sh`. This will open the default web browser and will ask for your Google account credentials (only the first time).

## Web application

[Work in progress]

## Install LeapMotion

[Work in progress]

## Todos

- Description to set up the offline music folders
- Summary of the voice commands that are currently supported

## References

[Work in progress]
- Google APIs
- Snowboy
- Django



