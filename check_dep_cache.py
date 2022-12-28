"""
DebFile.depends:
[
  [('name', 'version', 'relation')],
  [('name', 'version', 'relation')]
]
[[('0ad-data', '0.0.23.1', '>=')], [('0ad-data', '0.0.23.1-5', '<=')], [('0ad-data-common', '0.0.23.1', '>=')], [('0ad-data-common', '0.0.23.1-5', '<=')], [('libboost-filesystem1.74.0', '1.74.0', '>=')], [('libc6', '2.29', '>=')], [('libcurl3-gnutls', '7.16.2', '>=')], [('libenet7', '', '')], [('libgcc-s1', '3.4', '>=')], [('libgl1', '', '')], [('libgloox18', '1.0.24', '>=')], [('libicu67', '67.1-1~', '>=')], [('libminiupnpc17', '1.9.20140610', '>=')], [('libnspr4', '2:4.9.2', '>=')], [('libnvtt2', '', '')], [('libopenal1', '1.14', '>=')], [('libpng16-16', '1.6.2-1', '>=')], [('libsdl2-2.0-0', '2.0.12+dfsg1', '>=')], [('libsodium23', '1.0.14', '>=')], [('libstdc++6', '9', '>=')], [('libvorbisfile3', '1.1.2', '>=')], [('libwxbase3.0-0v5', '3.0.5.1+dfsg', '>=')], [('libwxgtk3.0-gtk3-0v5', '3.0.5.1+dfsg', '>=')], [('libx11-6', '', '')], [('libxcursor1', '1.1.2', '>')], [('libxml2', '2.9.0', '>=')], [('zlib1g', '1:1.2.0', '>=')], [('dpkg', '1.15.6~', '>=')]]

Apt.Cache.Versions.dependencies: list(apt.package.Dependency)

Scope: Convert dependenciees of Apt.Cache to DebFile.depends format
"""

import apt
import debfile


if __name__ == "__main__":
    apt_cache = apt.Cache()
    # Open cache. Now the apt_cache should have list of packages
    # Possible to pass apt.progress.base.OpProgress() as arg to apt_cache.open to have silent mode
    apt_cache.open(None)
    for pkg in apt_cache:
        for apt_cache_pkg_version in apt_cache[pkg.name].versions:
            list_depends = []
            for real_pkg_depends in apt_cache_pkg_version.dependencies:
                list_depends.append([(x.name, x.version, x.relation) for x in real_pkg_depends])
            deb = debfile.DebPackage()
            if apt_cache_pkg_version.package.name:
                if not deb.check(list_depends, apt_cache_pkg_version.architecture, apt_cache_pkg_version.package.name, apt_cache_pkg_version.version):
                    print("Package:", pkg.name)
                    print("Version", apt_cache_pkg_version.version)
                    print(deb._failure_string)
                    print("")

