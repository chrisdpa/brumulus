#! /bin/sh
ping -c4 192.168.0.1 > /dev/null

if [ $? != 0 ]
then
  echo "No network connection, restarting wlan0"
  /sbin/ifdown 'wlan0'
  sleep 5
  /sbin/ifup --force 'wlan0'
  sleep 5
fi

ping -c4 192.168.0.1 > /dev/null

if [ $? != 0 ]
then
  echo "No network connection, restarting device"
  sudo /sbin/shutdown -r now
fi
