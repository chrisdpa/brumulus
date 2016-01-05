# == Class: brumulus
#
# Configure Brumulus for basic operation
#

class brumulus {
	class { '::brumulus::controller': }
}

class brumulus::parameters {
	
	$path='/var/lib/brumulus'
	$path_www="${path}/www"
	$user=brumulus
	$service=brumulusd
	$git='https://github.com/chrisdpa/brumulus.git'
	$src="${path}/src"

}
