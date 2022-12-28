Simple scripts to check dependencies of debian packages
main.py: Copy from Gdebi, check dependencies of .deb files. Should run on repository. Must edit absolute path of pool files
check_dep_cache.py: Try to use apt.Cache only (no binary files). It can run on any Debian-based machine. Slow, buggy, ugly, hopeless.
debfile.py: modified script from python3-apt for check-dep-cache.