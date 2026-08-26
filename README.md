# Wake
This is my wake project and the goal is to make a web dashboard that I can use to manage my different servers remotely when it comes to startup, rebooting, and shutdown.

Wake is currently constructed as a Django website that a mediating or "lead" server can host to allow remote control of all the other servers in the network.

## Major Stipulations
The major stipulations to this functioning is that the mediating server needs to be on the same main network as the rest of the servers for the wake on lan functionality and that all the servers that you want to be part of the network need to support wakeonlan in the first place.

## Major Hurdles
- Need to make the on server portion to respond to shutdown/reboot requests.
- Make user login to make sure that only people who log in and have permission can interact with the server controls.
- Track uptime outside of its control? (ie know when I physically shut a server off)

## NOTE ON SECRETS
My secrets are currently stored in a file called variables.py that is not shared to the repository, so if you would like to take some of this code and iterate on it you will need to either do the same with your own secrets or replace my approach with your own for how to handle your secrets.
