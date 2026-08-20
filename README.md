# Wake
This is my wake project and the goal is to make a web dashboard that I can use to manage my different servers remotely when it comes to startup, rebooting, and shutdown.

Wake is currently constructed as a Django website that a mediating or "lead" server can host to allow remote control of all the other servers in the network.

## Major Stipulations
The major stipulations to this functioning is that the mediating server needs to be on the same main network as the rest of the servers for the wake on lan functionality and that all the servers that you want to be part of the network need to support wakeonlan in the first place.

## Major Hurdles
- How do we make it easy to add or remove devices from the network? (ie. automatically add endpoints, buttons, etc).
- Need to make the on server portion to respond to shutdown/reboot requests.
- POSSIBLY: Make user login to make sure that only people who log in and have permission can interact with the server controls.
- POSSIBLY: Track uptime outside of its control? (ie know when I physically shut a server off)