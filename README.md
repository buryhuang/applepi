# applepi

```
#####################################################
apt-get install supervisor

#####################################################
http://www.elinux.org/RPI-Wireless-Hotspot

#####################################################
/etc/hostapd/hostapd.conf

#####################################################
root@raspberrypi:/etc# cat /etc/init.d/hostapd 
#!/bin/sh

### BEGIN INIT INFO
# Provides:		hostapd
# Required-Start:	$remote_fs
# Required-Stop:	$remote_fs
# Should-Start:		$network
# Should-Stop:
# Default-Start:	2 3 4 5
# Default-Stop:		0 1 6
# Short-Description:	Advanced IEEE 802.11 management daemon
# Description:		Userspace IEEE 802.11 AP and IEEE 802.1X/WPA/WPA2/EAP
#			Authenticator
### END INIT INFO

PATH=/sbin:/bin:/usr/sbin:/usr/bin
DAEMON_SBIN=/usr/sbin/hostapd
DAEMON_DEFS=/etc/default/hostapd
DAEMON_CONF=
NAME=hostapd
DESC="advanced IEEE 802.11 management"
PIDFILE=/run/hostapd.pid

[ -x "$DAEMON_SBIN" ] || exit 0
[ -s "$DAEMON_DEFS" ] && . /etc/default/hostapd
[ -n "$DAEMON_CONF" ] || exit 0

DAEMON_OPTS="-B -P $PIDFILE $DAEMON_OPTS $DAEMON_CONF"
echo ${DAEMON_OPTS}

. /lib/lsb/init-functions

case "$1" in
start)
log_daemon_msg "Starting $DESC" "$NAME"
#start-stop-daemon --start --oknodo --quiet --exec "$DAEMON_SBIN" \
--pidfile "$PIDFILE" -- $DAEMON_OPTS >/dev/null
${DAEMON_SBIN} ${DAEMON_OPTS}
log_end_msg "$?"
;;
stop)
log_daemon_msg "Stopping $DESC" "$NAME"
start-stop-daemon --stop --oknodo --quiet --exec "$DAEMON_SBIN" \
--pidfile "$PIDFILE"
log_end_msg "$?"
;;
reload)
log_daemon_msg "Reloading $DESC" "$NAME"
start-stop-daemon --stop --signal HUP --exec "$DAEMON_SBIN" \
--pidfile "$PIDFILE"
log_end_msg "$?"
;;
restart|force-reload)
$0 stop
sleep 8
$0 start
;;
status)
status_of_proc "$DAEMON_SBIN" "$NAME"
exit $?
;;
*)
N=/etc/init.d/$NAME
echo "Usage: $N {start|stop|restart|force-reload|reload|status}" >&2
exit 1
;;
esac

exit 0


#####################################################
root@raspberrypi:/etc# cat /etc/network/interfaces.pub
# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

iface eth0 inet manual

allow-hotplug wlan0
iface wlan0 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

allow-hotplug wlan1
iface wlan1 inet manual
    wpa-conf /etc/wpa_supplicant/wpa_supplicant.conf

#####################################################
root@raspberrypi:/etc# cat /etc/network/interfaces.pri 
# interfaces(5) file used by ifup(8) and ifdown(8)

# Please note that this file is written to be used with dhcpcd
# For static IP, consult /etc/dhcpcd.conf and 'man dhcpcd.conf'

# Include files from /etc/network/interfaces.d:
source-directory /etc/network/interfaces.d

auto lo
iface lo inet loopback

iface eth0 inet manual

allow-hotplug wlan0
iface wlan0 inet static
address 192.168.42.1
netmask 255.255.255.0

up iptables-restore < /etc/iptables.ipv4.nat

#####################################################
root@raspberrypi:/etc# cat /etc/iptables.ipv4.nat
# Generated by iptables-save v1.4.21 on Sun Jun 11 23:39:45 2017
*filter
:INPUT ACCEPT [40:16129]
:FORWARD ACCEPT [0:0]
:OUTPUT ACCEPT [0:0]
-A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
-A FORWARD -i wlan0 -o eth0 -j ACCEPT
COMMIT
# Completed on Sun Jun 11 23:39:45 2017
# Generated by iptables-save v1.4.21 on Sun Jun 11 23:39:45 2017
*nat
:PREROUTING ACCEPT [6:1928]
:INPUT ACCEPT [2:1120]
:OUTPUT ACCEPT [0:0]
:POSTROUTING ACCEPT [0:0]
-A POSTROUTING -o eth0 -j MASQUERADE
COMMIT
# Completed on Sun Jun 11 23:39:45 2017
root@raspberrypi:/etc# 

#####################################################
root@raspberrypi:/etc# cat /etc/wpa_supplicant/wpa_supplicant.conf
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
	ssid="hyrub2.4-2f"
	psk="danhuang"
	key_mgmt=WPA-PSK
}

#####################################################
```