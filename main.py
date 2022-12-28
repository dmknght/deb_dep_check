# Copyright (c) 2005-2009 Canonical Ltd
#
# AUTHOR:
# Michael Vogt <mvo@ubuntu.com>
#
# This file is part of GDebi
#
# GDebi is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# GDebi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GDebi; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#

import apt
from apt.cache import Cache
import apt.debfile
import os
import sys
from gettext import gettext as _


class DebPackage(apt.debfile.DebPackage):
    def __init__(self, filename, cache, downloaded=False):
        super(DebPackage, self).__init__(cache=cache, filename=filename)
        self.downloaded = downloaded

    def __getitem__(self, item):
        if not item in self._sections:
            # Translators: it's for missing entries in the deb package,
            # e.g. a missing "Maintainer" field
            return _("%s is not available") % item
        return self._sections[item]


class GDebiCli(object):
    def __init__(self):
        tp = apt.progress.base.OpProgress()
        self._cache = Cache(tp)

    def open(self, file):
        try:
            if file.endswith(".deb"):
                self._deb = DebPackage(file, self._cache)
            else:
                sys.stderr.write(_("Unknown package type '%s', exiting\n") % file)
                sys.exit(1)
        except (IOError, SystemError, ValueError) as e:
            sys.stderr.write(_("Failed to open the software package\n"))
            sys.stderr.write(_("The package might be corrupted or you are not "
                               "allowed to open the file. Check the permissions "
                               "of the file.\n"))
            sys.exit(1)
        # check the deps
        if not self._deb.check():
            print("Package:", self._deb["Package"])
            print("Version:", self._deb["Version"])
            print(self._deb._failure_string)
            return False
        return True


if __name__ == "__main__":
    repo_path = "/var/www/html/parrot/pool/"  # Edit me: actual dir on repository
    app = GDebiCli()
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            abs_file_path = root + "/" + file
            if abs_file_path.endswith(".deb"):
                app.open(abs_file_path)
