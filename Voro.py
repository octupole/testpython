#!/usr/bin/env python
# encoding: utf-8
'''
Rg -- shortdesc

Rg is a description

It defines classes_and_methods

@author:     user_name

@copyright:  2017 organization_name. All rights reserved.

@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

import sys
import os
from optparse import OptionParser
from optparse import OptionParser as ArgParser
from optparse import SUPPRESS_HELP as ARG_SUPPRESS
PARSER_TYPE_INT = 'int'
PARSER_TYPE_STR = 'string'

import Micelles.Utilities.openFile as openFile

import Micelles.compVor.Voronoi as Voronoi


__all__ = []
__version__ = 0.1
__date__ = '2017-12-12'
__updated__ = '2017-12-12'

DEBUG = 0
TESTRUN = 0
PROFILE = 0


def myCallback(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(' '))

def parse_args(version,epilog,description):
    """Function to handle building and parsing of command line arguments"""
    usage = "usage: %prog [options] -f  JSONfile"

    parser = ArgParser(version=version,description=description+epilog,usage=usage)
    # Give optparse.OptionParser an `add_argument` method for
    # compatibility with argparse.ArgumentParser

    parser.add_option("-f", "--file", dest="filename", default=None,
                      help="set remote or local input filename", metavar="FILE")
    parser.add_option("-o", "--out", dest="outfile", default=None,
                      help="set output file if 'None' output is the standard output [default: %default]", metavar="FILE")
    parser.add_option("--host", dest="hostname", default=None,
                      help="set remote host name, if None local host is used [default: %default]")
    parser.add_option("--user", dest="username", default=None,
                      help="set remote user name [default: %default]")
    parser.add_option("-b", "--begin", dest="Start", default=None,
                      help="set trajectory start point on the trajectory, if None use the first step [default: %default]")
    parser.add_option("-e", "--end", dest="End", default=None,
                      help="set trajectory end point. If None use the last step [default: %default]")
    Labels=Voronoi.Voronoi.Labels
    label="'"+"','".join(Labels)+"'"
    parser.add_option("--which", action="store", dest="Which",
                      help="Choose what to do. Possible values are:  "+label)

    options = parser.parse_args()
    if isinstance(options, tuple):
        args = options[0]
    else:
        args = options
    if not args.filename:
        parser.print_help()
        sys.exit(1)
    return args


def main(argv=None):
    '''Command line options.'''
    if argv is None:
        argv = sys.argv[1:]

    program_name = os.path.basename(sys.argv[0])
    program_version = "v0.1"
    program_build_date = "%s" % __updated__

    program_version_string = '%%prog %s (%s)' % (program_version, program_build_date)
    # program_usage = '''usage: spam two eggs''' # optional - will be autogenerated by optparse
    program_longdesc = "Copyright 2017 Massimo Marchi (CEA Saclay)                                            \
                Licensed under the Apache License 2.0\nhttp://www.apache.org/licenses/LICENSE-2.0"
    description = (
        'Command line interface for computing Voronoi volumes and surfaces '
        '------------------------------------------------------------'
        '--------------\n'
        'https://github.com/octupole')



    try:
        opts = parse_args(version=program_version_string, epilog=program_longdesc, description=description)
        if opts.outfile:
            print("outfile = %s" % opts.outfile)
        if opts.hostname:
            print("hostname = %s " % opts.hostname)
        if opts.filename:
            print("Voronoi filename = %s " % opts.filename)
        else:
            print('No voronoi filename given, abort ')
            sys.exit(1)

        if opts.Which:
            opts.Which = [which for which in opts.Which.split()]
        else:
            print("--which required, abort ")
            sys.exit(1)

        if not Voronoi.Voronoi.testLabels(opts.Which[0]):
            print("Can't find what to do: %-s not on the list" % opts.Which[0])
            sys.exit(1)
        else:
            if len(opts.Which) != 2 and opts.Which[0] == 'Pick':
                print("Need an argument for option 'Pick', but found None ")
                sys.exit(1)

        myFile = openFile.openFile(filename=opts.filename, host=opts.hostname, user=opts.username)
        myRg = Voronoi.Voronoi(openfile=myFile.fp(), fileout=opts.outfile, start=opts.Start, end=opts.End)
        myRg.read()
        whatToDo = myRg.what(opts.Which[0])
        if len(opts.Which) == 2:
            whatToDo(eval(opts.Which[1]))
        else:
            whatToDo()

        # MAIN BODY #

    except Exception as e:
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help\n")
        return 2


if __name__ == "__main__":

    sys.exit(main())
