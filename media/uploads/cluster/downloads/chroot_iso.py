#!/usr/bin/env python
##################################################################
# StarCluster (http://web.mit.edu/starcluster)                   #
#                                                                #
# Mount a Linux OS iso file to a directory and chroot into it    #
#                                                                #
# The iso file must contain a full Linux operating system inside #
##################################################################

import os
import sys

if os.getuid() != 0:
    print 'chroot_iso.py must be run as root'
    sys.exit(1)

if len(sys.argv) != 3:
    print 'usage: %s <iso_file> <target_dir>' % sys.argv[0]
    sys.exit(1)

ISO_FILE=sys.argv[1]
TARGET_DIR=sys.argv[2]

if not os.path.isfile(ISO_FILE):
    print 'iso file %s does not exist or is not a regular file' % ISO_FILE
    sys.exit(1)

if not os.path.isdir(TARGET_DIR):
    print 'target directory %s does not exist' % TARGET_DIR
    sys.exit(1)

CHROOT_PROC = os.path.join(TARGET_DIR, 'proc')
CHROOT_DEV = os.path.join(TARGET_DIR, 'dev')
CHROOT_RESOLV = os.path.join(TARGET_DIR, 'etc','resolv.conf')
CHROOT_MTAB = os.path.join(TARGET_DIR, 'etc','mtab')

os.system('mount -o loop %s %s' % (ISO_FILE,TARGET_DIR))
os.system('mount -t proc none %s' % CHROOT_PROC)
os.system('mount -o bind /dev %s' % CHROOT_DEV)
os.system('cp /etc/resolv.conf %s' % CHROOT_RESOLV)
os.system('grep -v rootfs /proc/mounts > %s' % CHROOT_MTAB)
os.system('chroot %s /bin/bash' % TARGET_DIR)
os.system('umount %s' % CHROOT_PROC)
os.system('umount %s' % CHROOT_DEV)
os.system('rm %s' % CHROOT_RESOLV)
os.system('rm %s' % CHROOT_MTAB)
