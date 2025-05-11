PowerHour
=========

Monitor and switch the power on a Sequent Microsystems relay using a Synology Chat slash commands
and/or outgoing web hooks.

![image](https://github.com/user-attachments/assets/0041eaf2-961a-482d-b13b-fafade825092)

# Supported Slash Commands
* Get the current power state `/power status`
* Turn the power on `/power on`
* Turn the power off `/power off`

# Supported Outgoing Webooks
Same as the slash commands just without the leading slash.

# Building
This project is built with Docker.  The following command will build all of the dependencies
and the final application image `powerhour`.

```
$ sudo docker build -t powerhour .
.
.
.
Step 16/16 : CMD python3 powerhour.py
 ---> Running in 8fc5627b12e8
Removing intermediate container 8fc5627b12e8
 ---> 24be93e51b6f
Successfully built 24be93e51b6f
Successfully tagged powerhour:latest
```
# Running
The first step is to go and set up a Synology Chat Integration.  Follow the instructions here: 

https://github.com/bitcanon/synochat/tree/main?tab=readme-ov-file#settings for slash commands.
If you want to add the webhook support too you will need to creat an outgoing webhook integration.

Copy the token and create a file in this director called `env.sh` and with contents:

```
SLASH_TOKEN=<copied-token-from-synology-chat>
WEBHOOK_TOKEN=<copied-token-from-synology-chat>
```

I have defaults set for my environment with a single 3 port relay where I am only using the middle
relay for my needs.  These are in the code but can be overriden via by adding environment variables to
env.sh:

* `DEVICE` - The device on the modbus bus you wish to connect to.  If using i2c it will be 0.  Default is 0.
* `RELAY` - The specific relay you wish to control on the device.  Values 1,2,3 are valid.  Default is 2.

The `./run.sh` script can be used to launch a docker container from your image.

```
$ ./run.sh 
2ac336bb1e51ec1360c12f47cd2d9b93397a9731d92923842582c98678269447
$
```

The script can be modified to pull the prebuilt image from dockerhub `cameronbrunner/powerhour` if you chose to
skip the building steps.

# Why
My specific use case is remotely controlling the power of a device.  I have one of Sequent's relays
connected to a RaspberryPi Zero running Tailscale at a remote location and a DS-218+ running Tailscale and 
Synology chat at my house.  Any device in my home or on my Tailnet can connect to Synology chat and
control the remote device using chat commands.

# Core Dependencies
* [Sequent Microsystems Relay Python Library](https://github.com/SequentMicrosystems/3relind-rpi)
* [Synochat Python Library](https://github.com/bitcanon/synochat)

