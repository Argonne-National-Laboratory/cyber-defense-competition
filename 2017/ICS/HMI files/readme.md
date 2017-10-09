The water HMI specifically is:
PyOPC-Clients-Servers/clients/wtc_ui   <---- the frontend GUI PyOPC-Clients-Servers/server/wtc       <---- The team CIMORE server and virtual Control Systems.  

The Virtual Control Systems are built with busybox using the
configuration:
PyOPC-Clients-Servers/servers/cpscdc

The folder PyOPC is the actual PyOPC lib.  

There is a bug in the HMI during the SubscriptionPollRefresh that causes it to hang.  I think the problem may actually be in the PyOPC library, I'm still trying to hunt it down.

-Paul
