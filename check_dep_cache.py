"""
A script to scan current apt cache and find out broken packages
"""

import apt
import debfile


class DebPackage:
    def __init__(self, cache, package_name):
        """
        :param cache: the apt.Cache()
        :param package_name: name of the package to check
        """
        self.package_name = package_name
        self.cache = cache
        self.depends = []

    def _iterate_package_versions(self):
        """
        Iterate all versions of a package on the repository
        The data type is <class 'apt.package.Version'>
        :return:
        """
        # Iterate all versions of current package on the repository
        for current_package_ver in self.cache[self.package_name].versions:
            yield current_package_ver

    def _get_depends(self, package_version):
        """
        Get package's dependency of a package with a specific version. Data type <class 'apt.package.Dependency'>
        :param package_version: <class 'apt.package.Version'>
        :return:
        """
        for depends in package_version.dependencies:
            self.depends.append([(x.name, x.version, x.relation) for x in depends])

    def _show_dependency_errors(self, error_string, version):
        print("Package: ", self.package_name)
        print("Version: ", version)
        print(error_string)
        print("------------------")

    def check_package_issue(self):
        """
        Call DebPackage to check dependency errors
        :return:
        """
        deb_pointer = debfile.DebPackage()
        for package_version in self._iterate_package_versions():
            self._get_depends(package_version)
            if not deb_pointer.check(self.depends, package_version.architecture, self.package_name, package_version.version):
                self._show_dependency_errors(deb_pointer._failure_string, package_version)


if __name__ == "__main__":
    apt_cache = apt.Cache()
    # Open cache. Now the apt_cache should have list of packages
    # Possible to pass apt.progress.base.OpProgress() as arg to apt_cache.open to have silent mode
    apt_cache.open(None)
    for pkg in apt_cache:
        deb_pkg = DebPackage(apt_cache, pkg.name)
        deb_pkg.check_package_issue()
