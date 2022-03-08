#====================================================================
# The example is based on the Vernam Cipher
# A cipher is a type of one-time pad cryptosystem.
# It uses the boolean XOR function.
#====================================================================
# The novelty of the proposed solution concerns the method of generating one-time
# notebooks, for which the coordinates of the attractor trajectory are used
# Lorenz at a considerable distance from his starting point.
#====================================================================
# One-time notepad is generated dynamically for what it is used
# unique origin value and number of steps (points
# trajectories). The principle of operation of the proposed algorithm is presented below.
# When developing a regular algorithm, the choice of coordinates for the formation
# the cipher pad can be arbitrarily complicated, for example by using
# multiple trajectories.
#====================================================================
import numpy as np
import os
import math
from itertools import cycle
from hashlib import sha512
from scipy.integrate import odeint
import argparse
#====================================================================
# Getting command line options
#====================================================================
def param():
    parser = argparse.ArgumentParser(
    prog='L241.py',
    description='Vernam cipher. The novelty of the proposed solution concerns ' \
                'a way to generate one-time pads, why ' \
                'the coordinates of the trajectory of the Lorenz attractor are used' \
                'at a considerable distance from its starting point.',
    epilog='(c) Author: Botnev.A.V. <abotnev00@gmail.com> 08.12.2016'
    )

    parser.add_argument('-f','--fname', nargs='?', default='text0.txt')
    args = parser.parse_args()
    return args.fname

#====================================================================
# Coefficients of the Lorentz equations for obtaining a classical attractor
#====================================================================
s,r,b=10,28,8/3
#====================================================================
# Number of trajectory points to the origin used
# as a one-time notepad
#====================================================================
coutn_iter = 5001
#====================================================================
# Encryption (decryption) a xor b Vernam cipher
#====================================================================
def encrypt1(var, key):
    return  [a ^ ord(b) for (a,b) in zip(var, key)]
#====================================================================
# Lorenz ODE system for attractor cleaning
#====================================================================
def f(y, t):
   # x   y   z
    y1, y2, y3 = y
    return [s*(y2-y1), -y2+(r-y3)*y1, -b*y3+y1*y2]
#====================================================================
# We solve the ODE system and calculate its phase trajectory
# Initial value for example
# x =  1.0000000000000001,
# y = -1.0000000000000001,
# z = 10.0000000000000001
# Number of steps to get enough point spread
# n=5001
# a0 = [x, y, z] ODE solution (trajectory coordinates based on them
# one-time notepad is dynamically created)
#====================================================================
def lorenz(x,y,z,n):
    t = np.linspace(0,50,n)
    y0 = [x, y, z]
    a0 = odeint(f, y0, t, full_output=False).T
    return a0
#====================================================================
#        We get the next line of the cipher pad 128 bytes
#====================================================================
def m_read(a0,nzap):
    if len(a0[0]) >= nzap:
        line = str(a0[0][nzap]) + str(a0[1][nzap]) + str(a0[2][nzap]) +'\n'
        #print(line.strip())
        line1 = sha512(line.encode()).hexdigest()
        #print(line1)
        return line1
    return [1]
#====================================================================
# Calculate the size of the one-time pad, where 128 is the length in bytes
# hash calculated using the sha512 algorithm. Basis for hash calculation
# are the coordinates of the attractor's trajectory. However, the file size
# in bytes before encryption and after are equal.
### print(sha256(bytes([1, 2, 3])).hexdigest())
### print(sha512(bytes([1, 2, 3])).hexdigest())
#====================================================================
def file_crypt(fpath):
    siz = os.path.getsize(fpath) # file size in bytes.
    key = math.ceil(siz/128)     # number of points used for
    return key                   # getting a cipher pad
                                 # (rounding up)
#====================================================================
#                Encryption main procedure
#====================================================================
def crypt(f1,f2):
    file1 = open(f1,'rb')
    file2 = open(f2, 'ab')

    for i in range(keylen):
        text1     = file1.read(128)
        key1      = m_read(a0=zap,nzap=coutn_iter+i)
        encrypted = encrypt1(text1, key1)
        barray    = bytearray(encrypted)
        file2.write(barray)

    file2.close()
    file1.close()
#====================================================================
#        Existence Check and Deletion of Test Files
#====================================================================
def fexists(f):
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)), f)
    if os.path.exists(path):
        os.remove(path)
#====================================================================
#             Delete test files if any
#====================================================================
fexists(f='encrypted.txt')
fexists(f='decrypted.txt')
#====================================================================
#            Getting command line options
#====================================================================
fname = param()
#====================================================================
#    Calculate the length of the one-time pad for the encrypted file
#====================================================================
keylen = file_crypt(fpath=fname) #'text0.txt')
#====================================================================
# Calculate the trajectory (taking into account the length of the one-time pad)
#====================================================================
zap = lorenz(x =  1.0012400000000001, \
             y = -1.0000000010000001, \
             z = 10.0000000000000101, \
             n = coutn_iter+keylen)
#====================================================================
#                 One-time pad encryption
#====================================================================
crypt(f1 = fname,    f2 = 'encrypted.txt')
#====================================================================
#               Decryption with a one-time pad
#====================================================================
crypt(f1 = 'encrypted.txt',f2 = 'decrypted.txt')
#====================================================================
# Remember
# coutn_iter = 5001
# x=  1.0012400000000001
# y= -1.0000000010000001
# z= 10.0000000000000101
# and the file encrypted with this cipher pad (encrypted.txt)
#====================================================================
