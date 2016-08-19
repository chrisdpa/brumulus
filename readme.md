== Hardware

Raspberry Pi 2
PiTFT - 2.8" TFT+Touchscreen 
Wifi Dongle
Temperature Probe ds18b20

== Bootstrap

=== Configure wifi
  - https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md
  - Set a static IP allocation on the router for the RPi wifi MAC address
  - Reboot

=== Logon 
  - ssh pi@192.168.0.150 (what ever you allocated to the wifi adapter above) 

=== Install Puppet
  - sudo apt-get install puppet git

=== Clone the Git Repository
  - git clone https://github.com/chrisdpa/brumulus.git

{{{Cloning into 'brumulus'...
remote: Counting objects: 190, done.
remote: Total 190 (delta 0), reused 0 (delta 0), pack-reused 190
Receiving objects: 100% (190/190), 95.60 KiB, done.
Resolving deltas: 100% (85/85), done.}}}

=== Install the puppet modules required

sudo puppet module install theforeman-git
sudo puppet module install jfryman-nginx
sudo puppet module install proletaryo-supervisor
sudo puppet module install camptocamp-kmod

=== Run the puppet agent
sudo puppet apply brumulus/puppet/modules/brumulus/manifest/init.pp
