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
    
    $path='/var/lib/brumulus'
    $path_www="${path}/www"
    $user=brumulus
    $service=brumulusd
    $git='https://github.com/chrisdpa/brumulus.git'
    $src="${path}/src"
    $onewiregpio=22

}

# == Class: brumulus::controller
#
# Install base components
#

class brumulus::controller inherits brumulus::parameters
{
    include git

    kmod::load{ 'w1-gpio': }
    kmod::load{ 'w1-therm': }

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
#            'lapack',
            'scipy',
            'scikit-fuzzy', 
            'queuelib', 
            'falcon', 
            'Cython', 
            'twisted'
#           'twisted.internet' 
    ]

    package { $pip_packages:
        ensure   => installed,
        provider => pip,
    }

    user { $user:
        ensure     => 'present',
        managehome => true,
    }

    file { $path: 
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

    file { "${path}/bin":
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
        directory   => "${path}/bin/",
        user        => $user,
        group       => $user,
        logdir_mode => '0770',
    }

    service { $service:
        ensure  => running,
        enable  => true,
    } 
}

# == Class: brumulus::gui
#
# Install GUI components
#

class brumulus::gui inherits brumulus::parameters{

    class { 'nginx': } 

    nginx::resource::vhost { 'www.brumulus.com':
        www_root => $path_www,
    }

}