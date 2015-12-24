# == Class: brumulus
#
# Configure Brumulus for basic operation
#

class brumulus {
	class { '::brumulus::controller': }
  # class { '::brumulus::service': }

}



class brumulus::service{

supervisor::program { $SERVICE:
 ensure      => present,
 enable      => true,
 command     => '/usr/bin/python Brumulus.py',
 directory   => "${APP_HOME}/py/control/",
 user        => $USER,
 group       => $USER,
 logdir_mode => '0770',
}

# service { $SERVICE:
#    ensure  => running,
#    enable  => true,
#  } 

}

}