#!/usr/bin/env python
from getpass import getpass
from sys import exit

from bcrypt import gensalt, hashpw

pass1 = getpass("Enter password:")
pass2 = getpass("Confirm:")

if pass1 != pass2:
    print "Passwords didn't match!"
    exit(1)

print hashpw(pass1, gensalt())
