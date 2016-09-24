#!/usr/bin/python
# -*- coding: utf-8 -*-
"""vzdump-hook-script.pl ported in python

This is a port of vzdump-hook-script.pl (https://github.com/proxmox/pve-manager/blob/master/vzdump-hook-script.pl version 3.1-11)

"""

__author__ = "Matteo Sgalaberni"
__license__ = "GPL"

#example parameters in production
#101: Sep 23 00:15:07 INFO: HOOK: backup-end snapshot 101
#101: Sep 23 00:15:07 INFO: HOOK-ENV: vmtype=qemu;dumpdir=/dati1/dump;storeid=dati1;hostname=vmname;tarfile=/dati1/dump/vzdump-qemu-101-2016_09_22-23_10_01.vma.lzo;logfile=/dati1/dump/vzdump-qemu-101-2016_09_22-23_10_01.log

import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("phase", help="backup phase")
    parser.add_argument("mode", help="backup mode")
    parser.add_argument("vmid", help="backup vmid")

    args = parser.parse_args()

    # example hook script for vzdump (--script option)

    print "HOOK: %s" % ' '.join(sys.argv)


    if (args.phase == 'job-start' or
        args.phase == 'job-end'  or
        args.phase == 'job-abort'):

        dumpdir = os.environ["DUMPDIR"]
        storeid = os.environ["STOREID"]

        print "HOOK-ENV: dumpdir=%s;storeid=%s\n" % (dumpdir, storeid);
        # do what you want
    elif (args.phase == 'backup-start' or
    	 args.phase == 'backup-end' or
    	 args.phase == 'backup-abort' or
    	 args.phase == 'log-end' or
    	 args.phase == 'pre-stop' or
    	 args.phase == 'pre-restart'):

        vmtype =  os.environ["VMTYPE"] # openvz/qemu
        dumpdir = os.environ["DUMPDIR"]
        storeid = os.environ["STOREID"]
        hostname = os.environ["HOSTNAME"]
        # tarfile is only available in phase 'backup-end'
        tarfile = os.environ["TARFILE"]
        # logfile is only available in phase 'log-end'
        logfile = os.environ["LOGFILE"]

        print "HOOK-ENV: vmtype=%s;dumpdir=%s;storeid=%s;hostname=%s;tarfile=%s;logfile=%s" % (vmtype,dumpdir,storeid,hostname,tarfile,logfile)

        # example: copy resulting backup file to another host using scp
        if args.phase == 'backup-end':
            print "backup end"
        	#system ("scp $tarfile backup-host:/backup-dir") == 0 or
        	#    die "copy tar file to backup-host failed";
            # example: copy resulting log file to another host using scp
            pass
        if args.phase == 'log-end':
            print "log end"
        	#system ("scp $logfile backup-host:/backup-dir") == 0 or
        	#    die "copy log file to backup-host failed";
            pass

    else:
        raise Exception("got unknown phase '%s'" % phase)

    sys.exit(0)

if __name__ == "__main__":
    main()
