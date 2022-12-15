from haversine import haversine
import collections
import pandas as pd
import serial
import time
import io
import pynmea2
from math import dist

default_bound = 2  # 타켓좌표로부터 gps 상으로 2m 이내일 때 stop
flatten = pd.read_csv('normalize_point.csv', index_col=0)  # 좌표평면 코스 DataFrame
flatq = collections.deque([])  # 평면 코스 좌표 queue
for flat in flatten['x_y']:  # 평면 좌표
    flatq.append(flat)


def convert_gps(lat, lon):  # float GPS
    x1 = float(lat)
    x2 = float(lon)
    tmp1 = x1/100
    tmp2 = x2/100
    deg1 = tmp1//1
    deg2 = tmp2//1
    angle1 = (tmp1 % 1)/60*100
    angle2 = (tmp2 % 1)/60*100
    x = deg1+angle1
    y = deg2+angle2
    return (x, y)


def current_flat(pos):
    min_lat = 36.01014
    min_lon = 129.322232
    lat = pos[0]-min_lat
    lon = pos[1]-min_lon
    lat = (lat*1000000).round(0)
    lon = (lon*1000000).round(0)
    return (int(lat), int(lon))


def flat_target():  # 좌표평면 상 다음 target
    x, y = flatq.popleft()
    return (x, y)


def flat_man(x1, x2):  # 좌표평면 상 맨해튼 거리 # 사정거리는 마름모 모양 target = x2, current = x1
    x = abs(x2[0] - x1[0])
    y = abs(x2[1] - x2[0])
    man_dist = x+y
    return man_dist


def flat_ucli(x1, x2):  # 좌표평면 상 직선거리(유클리디안 거리)
    return dist(x1, x2)
