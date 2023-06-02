#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Simple DBF viewer for Linux by dosbox.

Use:

dbf_view_dos [options] --dbf_filename=/path/to/dbf/file

Options:
    --help|-h|-?    Program help
    --version|-v    Program version
    --viewer=       DBF viewer. CDBF/BDBFS-EN/BDBFS-RU
    --no-exit       Don't exit of dosbox automatically
    --no-wait       Don't wait for dosbox to exit

[NOTE]
To change the size of the dosbox window,
you need to set the options in the configuration file ~/.dosbox/dosbox-0.74-3.conf:

windowresolution=1280x960
output=opengl

"""

import sys
import os
import os.path
import platform
import getopt

__version__ = (0, 0, 0, 4)

DOSBOX_CMD_FMT = 'dosbox -c \"mount C: %s\" -c \"mount D: /mnt\" -c \"mount E: /media\" -c \"mount X: /usr/share/dbf_view_dos\" -c \"X:\\rk.com\" -c "X:\\%s %s" %s %s'

DOSBOX_CMD_OPTION_EXIT = '-c "exit"'

DOSBOX_CMD_OPTION_NOWAIT = '%s'

DBF_VIEWERS = {
    'CDBF': 'CDBF\\cdbf.exe',
    'BDBFS-RU': 'BDBFS-RU\\bdbfs.exe',
    'BDBFS-EN': 'BDBFS-EN\\bdbfs.exe',
}


def getHomePath():
    """
    Home directory path.
    """
    os_platform = platform.uname()[0].lower()
    if os_platform == 'windows':
        home_path = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    elif os_platform == 'linux':
        home_path = os.environ['HOME']
    else:
        print(u'OS <%s> not support' % os_platform)
        return None
    return os.path.normpath(home_path)


def main(*argv):
    """
    Main function.

    @param argv: Command line options.
    """
    try:
        options, args = getopt.getopt(argv, 'h?v',
                                      ['help', 'version',
                                       'viewer=', 'dbf-filename=',
                                       'no-exit', 'no-wait'])
    except getopt.error as msg:
        print(str(msg))
        print(__doc__)
        sys.exit(2)

    viewer = 'CDBF'
    dbf_filename = None
    do_exit = True
    do_wait = True

    for option, arg in options:
        if option in ('-h', '--help', '-?'):
            print(__doc__)
            sys.exit(0)
        elif option in ('-v', '--version'):
            txt_version = '.'.join([str(ver) for ver in __version__])
            print(u'Version: %s' % txt_version)
            sys.exit(0)
        elif option == '--viewer':
            viewer = arg
        elif option == '--dbf-filename':
            dbf_filename = arg
        elif option == '--no-exit':
            do_exit = False
        elif option == '--no-wait':
            do_wait = False

    if dbf_filename and os.path.exists(dbf_filename):
        viewer_option = DBF_VIEWERS.get(viewer, '')
        if viewer_option:
            home_path = getHomePath()
            exit_option = DOSBOX_CMD_OPTION_EXIT if do_exit else ''
            wait_option = '' if do_wait else DOSBOX_CMD_OPTION_NOWAIT
            dos_dbf_filename = dbf_filename.replace(home_path, 'C:\\').replace('/mnt/', 'D:\\').replace('/media/', 'E:\\').replace(os.path.sep, '\\')
            cmd = DOSBOX_CMD_FMT % (home_path, viewer_option, dos_dbf_filename, exit_option, wait_option)
            print(u'Run command <%s>' % cmd)
            os.system(cmd)
        else:
            print(u'Incorrect viewer <%s>' % viewer)
    else:
        print(u'DBF file <%s> not found' % dbf_filename)


if __name__ == '__main__':
    main(*sys.argv[1:])
