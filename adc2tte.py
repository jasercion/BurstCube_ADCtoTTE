from astropy.io import fits
from astropy.table import Table
import numpy as np
import sys

def bintablehdu_constructor(data, hduname):
    table = Table(rows=data[0], names=data[1])
    bintablehdu = fits.BinTableHDU(table, name=hduname)
    return bintablehdu

file = sys.argv[1]
f = open(file,"r")
lines = f.readlines()
input = []

for x in lines:
    input.append(tuple((x.split(' ')[0],
                        x.split(' ')[1],
                        x.split(' ')[2],
                        x.split(' ')[3].strip())))

f.close()

scaledpulse = []

elements = input.pop(0)

for x in input:
    scaledpulse.append([int(x[1]),int(x[3])-int(x[2])])

channels = []
tstart = (input[0])[1]
tstop = (input[-1])[1]
emin = 0
emax = 250
i = 1

while i < 17:
    channels.append([i,emin,emax])
    emin = emax+1
    emax = emax+250
    i += 1

eventpairs = []

for x in scaledpulse:
    for y in channels:
        if x[1] in range(y[1],y[2]+1,1):
            eventpairs.append([x[0],y[0]])

primary_hdu = fits.PrimaryHDU()
ebounds_hdu = bintablehdu_constructor([channels,('CHANNEL','E_MIN','E_MAX')], 'EBOUNDS')
events_hdu = bintablehdu_constructor([eventpairs,('EVENT','PHA')], 'EVENTS')
gti_hdu = bintablehdu_constructor([[[tstart,tstop]],('TSTART','TSTOP')], 'GTI')

hdulist = fits.HDUList([primary_hdu,ebounds_hdu,events_hdu,gti_hdu])

hdulist.writeto('burstcubette.fits')
