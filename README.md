# Zero (voice assistant and connected home)

*Zero* is a voice assistant running on Raspberry Pi 3B+ and developed in Python 3.5. It integrates:
- A *hotword detection* module using a Python 3 binding library of [Snowboy](https://github.com/Kitt-AI/snowboy/tree/master/lib)
- A *speech-to-text* module using the Google Speech-to-Text API
- An *music player* module using the Youtube Data API and VLC for on-device offline playlists, Youtube music and radio stations
- A *note* module to write notes using the Google Sheets API
- A *Django web application* to access the main controls from any devices in the home network
- A *Leap Motion library* module to control *Zero* via hand gestures using the [Leap Motion](https://www.leapmotion.com/) infrared sensor


Simply say **Ok Zero**.

## I. Hardware list
- Raspberry Pi 3B+ (with power adapter)
- Micro SD card and a micro SD to SD adapter
- Ethernet cable
- Jabra SPEAK 510 USB (microphone+speaker for the voice assistant)
- Speaker (3.5 mm jack for the music player)
- Leap Motion infrared sensor (optional)

## II. Setup

This version of *Zero* has been tested with Raspbian Stretch (Desktop version 2018-06-27 release). The steps described below correspond to the headless installation mode (without screen) with an ethernet connection to your home network. The Raspbian OS is flashed on the mirco SD card from a Windows computer with internet connection and micro SD card reader. To use the different modules base on Google APIs, you should have a Google account.

### Install Raspbian, setup SSH and VNC

- Download Raspbian [here](https://www.raspberrypi.org/downloads/raspbian/).
- Extract to a new folder, you will have a single **.img** image file.
- Download and install Etcher [here](https://www.balena.io/etcher/). We use it to flash the image file on the micro SD card.
- Launch Etcher, select the Raspbian image file, select the SD card and flash the OS on it.
- In the boot partition, simply add a file named **ssh** to enable SSH connections to our raspberry.
- Insert the micro SD card into the Raspberry Pi, connect the power adapter and connect to the home network via ethernet.
- Open a web browser and connect to your router (e.g., go to `fritz.box` for FRITZ!Box users) to find the IP address of your Raspberry.
- Download Putty and SSH to your Raspberry. the default username is **pi** and password is **raspberry**.
- Enable VNC with `sudo raspi-config`, **Interfacing Options** > **VNC** > **Yes**

### Setup the shared folder

- From the command line `sudo apt-get update` and `sudo apt-get install samba`
- Create the folder `/home/pi/share`
- Edit the Samba configuration file `/etc/samba/smb.conf`, change the line `workgroup = WORKGROUP` to match the Windows workgroup (the default workgroup in Windows 10 is **WORKGROUP**, so no changes are needed), uncomment and change the line `wins support = no` to `wins support = yes`. Finally, append the following lines at the end of the file:
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
- Restart Samba `sudo service smbd restart` and you should be able to access it from Windows under `\\RASPBERRYPI\pishare`

### Install the dependencies and clone the repository

- Install Python 3.5 `sudo apt-get install python3.5` and Virtualenv `sudo pip3 install virtualenv`
- Create the virtual environment in the shared folder with `cd ~/share` and `virtualenv zenv` and activate it `source ~/share/zenv/bin/activate`
- Create the folder `~/share/app` and clone the git repository in it `git clone https://github.com/jahsue78/zero.git`
- Install the packages `sudo apt-get install vlc portaudio19-dev libatlas-base-dev pulseaudio libttspico-utils sox`
- Install the Pip requirements `pip install -r ./zero/requirements.txt`

### Add the Google credentials

- Create the folder `~/share/app/cred`
- For each of the Google APIs, follow the steps to obtain the API private key as a JSON file:
   - Go to the [Google Speech-to-Text API](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) page and click on **SET UP A PROJECT** and get your private key
   - Go to the [Youtube Data API](https://developers.google.com/youtube/v3/getting-started) page and get your private key
   - Go to the [Google Sheets API](https://developers.google.com/sheets/api/quickstart/python) page, click on **ENABLE THE GOOGLE SHEETS API** and get your private key
- Add the 3 JSON files to the folder `~/share/app/cred`

### Configure and start *Zero*
- Configure PulseAudio `mkdir ~/.config/pulse`, `cp ~/share/app/zero/config/daemon.conf ~/.config/pulse`
- Rename `config_example.ini` to `config.ini` and modify it to match your configuration
   - Modify the **IP** parameter to match the Raspberry IP address in your home network
   - Modify the fields **KEY_GSPEECH** (Google Speech-to-Text API),  **KEY_GYTB** (Youtube Data API), **KEY_GSHEET** (Google Sheets API) to match the JSON file name of your private keys in `~/share/app/cred`
   - Modify the field **SHEET_ID** put a valid spreadsheet ID from your drive
   - Execute `python ~/share/app/zero/modules/util/audio.py` to display the audio configuration, you should see something similar to this (if not try to restart your Raspberry Pi with `sudo reboot`, do not forget to re-activate your environment after that):
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
- Open a VNC session, open a shell, go to the *Zero* root folder `cd ~/share/app/zero`, activate your environment `source activate.sh` and launch *Zero* `./main.sh`. This will open the default web browser and will ask for your Google account credentials (only the first time).

## III. Usage

To wake up *Zero*, simply say the hotword **Ok Zero** and wait for her response before saying your voice command.

### Offline music

- The music files should be in the music library folder `~/share/player/lib`
- The playlists are defined in `~/share/player/list`
- Copy the examplary playlists `cp ~/share/app/zero/config/examples/defaut.json ~/share/player/list` and `cp ~/share/app/zero/config/examples/test.json ~/share/player/list`
- In a playlist file, the tracks are defined relatively to the music library folder `~/share/player/lib`
- The default playlist `defaut.json` is played with the voice command **Musique**

### Voice commands

The following examples are French voice commands:
- **Musique**: Play the default playlist `defaut.json` (see **Offline music** section)
- **Musique "test"**: Play the playlist `test.json` (see **Offline music** section)
- **YouTube "Amélie Poulain"**: Play the music found on YouTube with the search keywords "Amélie Poulain"
- **Radio "Nova"**: Play radio "Nova" (other radios are "RTL", "France Inter", "Europe 1", "TSF Jazz", "FIP", "France Culture", "France Info", "OUI FM")
- **Volume +10**: Increase the volume by 10
- **Volume -5**: Decrease the volume by 5
- **Volume 15**: Set the volume to 15
- **Pause**: Pause music
- **Continue**: Resume music
- **Précédent**: Previous track
- **Suivant**: Next track
- **Note "Notre-Dame de Paris est en feu"**: Add the new line "Notre-Dame de Paris est en feu" to your spreadsheet

### Web application

The web application allows to control With a device connected to the home network, go to the following URL: `http://<IP>:<PORT>/gui/dashboard`. You can see different push buttons:
- **Listen and Write**: *Zero* listens and write the text in the **Results** section
- **Listen and Do**: Trigger hotword detection, i.e., *Zero* listens and do the specified action
- **Activate**: Enable or disable hotword detection

## IV. Hand gesture control

The Javascript library is included in the web application. The Leap motion controller is connected to a Windows computer.

### Setup 

- Download the Leap Motion Orion 3.2.1 SDK installer [here](https://developer.leapmotion.com/releases) 
- Follow the installation steps
- If the Leap Motion does not work, you can try to restart the service, look for `Services` in the Windows search bar.

### Usage

All the *hand* gestures correspond to open hand gesture whereas *pinch* gestures correspond to gestures with thumb and index fingers touching each others.

- *Hand up* gesture: Play music
- *Hand down* gesture: Pause music
- *Hand right* gesture: Next track
- *Hand left* gesture: Previous track
- *Hand clockwise circle* gesture: Volume up
- *Hand anti-clockwise circle* gesture: Volume down
- *Pinch clockwise circle* gesture: Trigger hotword detection, equivalent to say **Ok Zero**

## V. Tips

### Change the language

- Modify the `action.py`, `gspeech.py` and `speak.py` modules. [Currently working on the English version]

## VI. Todos

- Support other languages
- Detail references

## VII. References

[Work in progress]
- Google APIs
- Snowboy
- Django
- Leap Motion



