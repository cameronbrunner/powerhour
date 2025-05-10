PowerHour
=========

Monitor and switch the power on a Sequent Microsystems relay using a Synology Chat slash command.

Leverages: 
* Docker for hosting the slash command bot.
* [Sequent Microsystems Relay Python Library][(https://github.com/SequentMicrosystems/3relind-rpi)
* [Synochat Python Library](https://github.com/bitcanon/synochat)


# Supported Commands
* Get the current power state `/power status`
* Turn the power on `/power on`
* Turn the power off `power off`

# Why
My specific use case is remotely controlling the power of a device.  I have one of Sequent's relays
connected to a RaspberryPi Zero running Tailscale at a remote location and a DS-218+ running Tailscale and 
Synology chat at my house.  Any device in my home or on my Tailnet can connect to Synology chat and
control the remote device using chat commands.
