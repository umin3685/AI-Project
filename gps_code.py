from haversine import haversine
import collections
import pandas as pd
import serial
import time
import io
import pynmea2
from math import dist
gps_list = []  # 주행 간 측정되는 gps 좌표 list
default_bound = 2  # 타켓좌표로부터 gps 상으로 2m 이내일 때 stop
distance = pd.read_csv('new_point.csv', index_col=0)  # 거리 코스 DataFrame
# Init Course Information
disq = collections.deque([])  # 거리 코스 좌표 queue

for dis in distance['x_y']:  # 거리 좌표
    disq.append(dis)


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


def current_string(pos, n1, n2):  # GPS좌표가 필요할 때 불러와서 저장
    x = str(pos[0])
    y = str(pos[1])
    if len(x) >= n1:
        x = x[:n1]
    else:
        x = x + '0'
    if len(y) >= n2:
        y = y[:n2]
    else:
        y = y + '0'
    return (x, y)


def target_position():  # queue pop
    x, y = disq.popleft()
    return (x, y)


def gps_dist(pos, target):  # distance to target from current position(pos = tuple, target = tuple)
    return haversine(pos, target, unit='m')


def main():
    disq.popleft()  # start 좌표 ==> 쓸데없음
    # GPS좌표를 받아오는 port = com4, 1초마다 gps좌표receive
    ser = serial.Serial('COM4', 9600, timeout=1.0)
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))  # to read Serial
    target = target_position()  # 첫 번쨰 목표 좌표
    while disq:  # queue가 텅 빌 때 까지
        line = sio.readline()
        if(line[0:6] == '$GPRMC'):
            test = line.split(',')
            if test[2] == 'A':
                gps = convert_gps(test[3], test[5])  # 현재 gps 좌표(실수형)
        # set_angle
        # PWM_ON
        if gps_dist(gps, target) <= default_bound:
            # PWM_OFF
            target = target_position()
            # set_angle
            # PWM_ON

        # 비명 or detect falling
        # PWM OFF
        string_gps = current_string(gps, 9, 10)
        # string_gps to WORK STATION

    while gps_dist(gps, target) > default_bound:
        # set_angle
        # PWM_ON
        pass
    return
