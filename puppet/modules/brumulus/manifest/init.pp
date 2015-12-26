# == Class: brumulus
#
# Configure Brumulus for basic operation
#

class brumulus {
	class { '::brumulus::controller': }
  # class { '::brumulus::service': }

}
