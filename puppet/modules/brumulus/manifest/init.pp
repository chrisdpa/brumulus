include brumulus

# == Class: brumulus
#
# Configure Brumulus for basic operation
#

class brumulus {
    class { '::brumulus::controller': }
    # class { '::brumulus::gui': }
}

class brumulus::parameters {
    
    $path_install='/var/lib/brumulus'
    $path_www="/var/www/brumulus.com"
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
        mode   => '0750',
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
        ensure      => present,
        enable      => true,
        command     => '/usr/bin/python Brumulus.py',
        directory   => "${path_install}/bin/",
        user        => 'root',
        group       => 'root',
        logdir_mode => '0770',
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

    file { '/var/www/brumulus.com':
        ensure => 'link',
        target => "${path_install}/src/www/",
        owner  => $user,
        group  => $user,
    }

}