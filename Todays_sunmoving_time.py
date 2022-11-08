#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
import datetime
# sin function using degree
def sind(d):
    return math.sin(math.radians(d))

# cos function using degree
def cosd(d):
    return math.cos(math.radians(d))

# tan function using degree
def tand(d):
    return math.tan(math.radians(d))

# calculate Julius year (year from 2000/1/1, for variable "t")
def jy(yy, mm, dd, h, m, s, i):# yy/mm/dd h:m:s, i: time difference
    yy -= 2000
    if (mm <= 2):
        mm += 12
        yy -= 1

    k = 365 * yy + 30 * mm + dd - 33.5 - i / 24.0 + math.floor(3 * (mm + 1) / 5.0) \
        + math.floor(yy / 4.0) - math.floor(yy / 100.0) + math.floor(yy / 400.0)
    k += ((s / 60.0 + m) / 60 + h) / 24.0 # plus time
    k += (65 + yy) / 86400.0 # plus delta T
    return k / 365.25

# solar position1 (celestial longitude, degree)
def spls(t): # t: Julius year
    L = 280.4603 + 360.00769 * t \
        + (1.9146 - 0.00005 * t) * sind(357.538 + 359.991 * t) \
        + 0.0200 * sind(355.05 +  719.981 * t) \
        + 0.0048 * sind(234.95 +   19.341 * t) \
        + 0.0020 * sind(247.1  +  329.640 * t) \
        + 0.0018 * sind(297.8  + 4452.67  * t) \
        + 0.0018 * sind(251.3  +    0.20  * t) \
        + 0.0015 * sind(343.2  +  450.37  * t) \
        + 0.0013 * sind( 81.4  +  225.18  * t) \
        + 0.0008 * sind(132.5  +  659.29  * t) \
        + 0.0007 * sind(153.3  +   90.38  * t) \
        + 0.0007 * sind(206.8  +   30.35  * t) \
        + 0.0006 * sind( 29.8  +  337.18  * t) \
        + 0.0005 * sind(207.4  +    1.50  * t) \
        + 0.0005 * sind(291.2  +   22.81  * t) \
        + 0.0004 * sind(234.9  +  315.56  * t) \
        + 0.0004 * sind(157.3  +  299.30  * t) \
        + 0.0004 * sind( 21.1  +  720.02  * t) \
        + 0.0003 * sind(352.5  + 1079.97  * t) \
        + 0.0003 * sind(329.7  +   44.43  * t)
    while (L >= 360):
        L -= 360
    while (L < 0):
        L += 360
    return L

# solar position2 (distance, AU)
def spds(t): # t: Julius year
    r = (0.007256 - 0.0000002 * t) * sind(267.54 + 359.991 * t) \
        + 0.000091 * sind(265.1 +  719.98 * t) \
        + 0.000030 * sind( 90.0) \
        + 0.000013 * sind( 27.8 + 4452.67 * t) \
        + 0.000007 * sind(254   +  450.4  * t) \
        + 0.000007 * sind(156   +  329.6  * t)
    r = pow(10, r)
    return r

# solar position3 (declination, degree)
def spal(t): # t: Julius year
    ls = spls(t)
    ep = 23.439291 - 0.000130042 * t
    al = math.degrees(math.atan(tand(ls) * cosd(ep)))
    if ((ls >= 0) and (ls < 180)):
        while (al < 0):
            al += 180
        while (al >= 180):
            al -= 180
    else:
        while (al < 180):
            al += 180
        while (al >= 360):
            al -= 180
    return al

# solar position4 (the right ascension, degree)
def spdl(t):# t: Julius year
    ls = spls(t)
    ep = 23.439291 - 0.000130042 * t
    dl = math.degrees(math.asin(sind(ls) * sind(ep)))
    return dl

# Calculate sidereal hour (degree)
def sh(t, h, m, s, l, i):
    # t: julius year, h: hour, m: minute, s: second,
    # l: longitude, i: time difference
    d = ((s / 60.0 + m) / 60.0 + h) / 24.0 # elapsed hour (from 0:00 a.m.)
    th = 100.4606 + 360.007700536 * t + 0.00000003879 * t * t - 15 * i
    th += l + 360 * d
    while (th >= 360):
        th -= 360
    while (th < 0):
        th += 360
    return th

# Calculating the seeming horizon altitude "sa"(degree)
def eandp(alt, ds):# subfunction for altitude and parallax
    e = 0.035333333 * math.sqrt(alt)
    p = 0.002442818 / ds
    return p - e

def sa(alt, ds):# alt: altitude (m), ds: solar distance (AU)
    s = 0.266994444 / ds
    r = 0.585555555
    k = eandp(alt,ds) - s - r
    return k

# Calculating solar alititude (degree) {
def soal(la, th, al, dl):
    # la: latitude, th: sidereal hour,
    # al: solar declination, dl: right ascension
    h = sind(dl) * sind(la) + cosd(dl) * cosd(la) * cosd(th - al)
    h = math.degrees(math.asin(h))
    return h

# Calculating solar direction (degree) {
def sodr(la, th, al, dl):
    # la: latitude, th: s:dereal hour,
    # al: solar declination, dl: right ascension
    t = th - al
    dc = -cosd(dl) * sind(t)
    dm = sind(dl) * sind(la) - cosd(dl) * cosd(la) * cosd(t)
    if (dm == 0):
        st = sind(t)
        if (st > 0):
            dr = -90
        if (st == 0):
            dr = 9999
        if (st < 0):
            dr = 90
    else:
        dr = math.degrees(math.atan(dc / dm))
        if (dm < 0):
            dr += 180

    if (dr < 0):
        dr += 360
    return dr

def calc(yy, mm, dd, i, lon, lat, alt=0, hh=-1, m=-1):
    """
    return list:
        item 0: astronomical twilight start
        item 1: voyage twilight start
        item 2: citizen twilight start
        item 3: sun rise
        item 4: meridian
        item 5: sun set
        item 6: citizen twilight end
        item 7: voyage twilight end
        item 8: astronomical twilight end

    each item has time, and solar direction (in degrees) if item is sun rise or sun set,
    solar altitude (in degrees) if item is meridian.
    """
    result = []

    t = jy(yy, mm, dd - 1, 23, 59, 0, i)
    th = sh(t, 23, 59, 0, lon, i)
    ds = spds(t)
    ls = spls(t)
    alp = spal(t)
    dlt = spdl(t)
    pht = soal(lat, th, alp, dlt)
    pdr = sodr(lat, th, alp, dlt)

    for hh in range(0, 24):
        for m in range(0, 60):

            t = jy(yy, mm, dd, hh, m, 0, i)
            th = sh(t, hh, m, 0, lon, i)

            ds = spds(t)
            ls = spls(t)
            alp = spal(t)
            dlt = spdl(t)

            ht = soal(lat, th, alp, dlt)
            dr = sodr(lat, th, alp, dlt)
            tt = eandp(alt, ds)

            t1 = tt - 18
            t2 = tt - 12
            t3 = tt - 6
            t4 = sa(alt, ds)

            key = "%d-%02d-%02d %02d:%02d:00+%02d" % (yy, mm, dd, hh, m, i)

            if ((pht < t4) and (ht > t4)):
                result.append((key, math.floor(dr)))

            if ((pht > t4) and (ht < t4)):
                result.append((key, math.floor(dr)))
            """
            #itme 0
            if ((pht < t1) and (ht > t1)):
                result.append((key, None))
            #item 1
            if ((pht < t2) and (ht > t2)):
                result.append((key, None))
            #item 2
            if ((pht < t3) and (ht > t3)):
                result.append((key, None))
            #item 3
            if ((pht < t4) and (ht > t4)):
                result.append((key, math.floor(dr)))
            #item 4
            if ((pdr < 180) and (dr > 180)):
                result.append((key, math.floor(ht)))
            #item 5
            if ((pht > t4) and (ht < t4)):
                result.append((key, math.floor(dr)))
            #item 6
            if ((pht > t3) and (ht < t3)):
                result.append((key, None))
            #item 7
            if ((pht > t2) and (ht < t2)):
                result.append((key, None))
            #item 8
            if ((pht > t1) and (ht < t1)):
                result.append((key, None))
            """
            pht = ht
            pdr = dr

    #f.result.value = ans
    return result

if __name__ == '__main__':

    today = datetime.date.today()
    #Location of Longitude and Latitude
    Loc_Lon=135.001918
    Loc_Lat=34.649279
    r = calc(today.year, today.month, today.day, 9, Loc_Lon, Loc_Lat, 0.)

    for k, v in r:
        print("%s [ %s ]" % (k, v))
        

