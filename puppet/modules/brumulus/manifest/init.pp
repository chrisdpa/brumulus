include brumulus

# == Class: brumulus
#
# Configure Brumulus for basic operation
#
class brumulus {
    class { '::brumulus::controller': }
    # class { '::brumulus::gui': }
}

# == Class: brumulus::parameters
#
# Common settings
#
class brumulus::parameters {

    $path_install='/var/lib/brumulus'
    $path_www='/var/www/brumulus.com'
    $user=brumulus
    $service=brumulusd
    $git='https://github.com/chrisdpa/brumulus.git'
    $src="${path_install}/src"
    $onewiregpio=22

}

# == Class: brumulus::controller
#
# Install base components
#

class brumulus::controller inherits brumulus::parameters
{
    include git

    kmod::load{ 'w1_gpio': }
    kmod::load{ 'w1_therm': }

    file_line { "Set 1-Wire GPIO PIN Number ${onewiregpio}":
        path => '/boot/config.txt',
        line => "dtoverlay=w1-gpio,gpiopin=${onewiregpio}",
    }

    $packages = ['python-scipy', 'python-daemon']

    package { $packages:
        ensure => installed
    }

    $pip_packages = [
            'numpy',
            'scipy',
            'scikit-fuzzy',
            'queuelib',
            'falcon',
            'Cython',
            'twisted'
    ]

    package { $pip_packages:
        ensure   => installed,
        provider => pip,
    }

    user { $user:
        ensure     => 'present',
        managehome => true,
    }

    file { $path_install:
        ensure => 'directory',
        owner  => $user,
        group  => $user,
        mode   => '0755',
    }

    file { '/var/data':
        ensure => 'directory',
        owner  => $user,
        group  => $user,
        mode   => '0755',
    }

    file { '/var/data/brumulus':
        ensure => 'directory',
        owner  => $user,
        group  => $user,
        mode   => '0755',
    }

    git::repo { $user:
        target => $src,
        source => $git,
        user   => $user,
    }

    file { "${path_install}/bin":
        ensure => 'link',
        target => "${src}/py/control/",
        owner  => $user,
        group  => $user,
    }

    include ::supervisor

    supervisor::program { $service:
        ensure                 => present,
        enable                 => true,
        command                => '/usr/bin/python Brumulus.py',
        directory              => "${path_install}/bin/",
        user                   => 'root',
        group                  => 'root',
        logdir_mode            => '0775',
        autorestart            => true,
        stdout_logfile_backups => 2,
    }

    file { '/usr/local/bin/wificheck.sh':
      source => "${src}/puppet/modules/brumulus/files/wificheck.sh",
      mode   => '0755',
    }

    cron { 'wificheck':
      command => '/usr/local/bin/wificheck.sh',
      user    => root,
      minute  => '*/5'
    }


}

# == Class: brumulus::gui
#
# Install GUI components
#
class brumulus::gui inherits brumulus::parameters{


    package { 'nginx':
        ensure   => installed,
    }

    file { '/var/www':
        ensure => directory,
    }

    file { '/var/www':
        ensure => 'link',
        target => "${path_install}/src/www/",
        owner  => 'root',
        group  => 'root',
    }

    file { '/usr/lib/arm-linux-gnueabihf/nss/':
        ensure => 'link',
        target => '/usr/lib/nss',
        owner  => 'root',
        group  => 'root',
    }

    package { 'chromium':
        ensure   => installed,
    }
    package { 'x11-xserver-utils':
        ensure   => installed,
    }
    package { 'unclutter':
        ensure   => installed,
    }

    file { '/etc/xdg/lxsession/LXDE-pi/autostart':
      ensure => file,
      owner  => 'root',
      group  => 'root',
      mode   => '0644',
      source => 'puppet:///modules/brumulus/x-autostart',
    }

    # ~/.xinitrc
    # #!/bin/sh
    # exec /usr/bin/chromium --disable-web-security --kiosk http://127.0.0.1/kiosk.html

    # /etc/nginx/sites-enabled/default
    # server {
    #     root /var/www;
    #     index index.html index.htm kiosk.html;
    #     server_name localhost;
    #     location / {
    #         try_files $uri $uri/ /index.html;
    #     }
    #     location /data/ {
    #         proxy_pass       http://localhost:8000/;
    #     }
    # }

}
