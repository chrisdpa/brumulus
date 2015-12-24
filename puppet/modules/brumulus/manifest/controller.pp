# == Class: brumulus::install
#
# Install base components
#

class brumulus::install{
	$path='/var/lib/brumulus'
	$user=brumulus
	$service=brumulusd
	$git='https://github.com/chrisdpa/brumulus.git'
	$src="${path}/src"

	include git

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

#	supervisor::program { $service:
#		ensure      => present,
#		enable      => true,
#		command     => '/usr/bin/python Brumulus.py',
#		directory   => "${path}/py/control/",
#		user        => $user,
#		group       => $user,
#		logdir_mode => '0770',
#	}

	# service { $service:
	#    ensure  => running,
	#    enable  => true,
	#  } 
}