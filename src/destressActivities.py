import datetime
import tkinter as tk
from tkinter import messagebox
import time
import os

global img

short_break = 1
medium_break = 3
long_break = 6
hour_count = 0
current_time = datetime.datetime.now()
    
target_time = current_time + datetime.timedelta(hours=1)
while(True):
    while current_time < target_time:
        current_time = datetime.datetime.now()
    target_time = current_time + datetime.timedelta(seconds=5)
    hour_count += 1
    #print(hour_count)
    if hour_count % 6 == 0:
        img = 'curious.png'
        continue
    elif hour_count % 3 == 0:
        img = 'embrace-journey.png'
        continue
    elif hour_count % 1 == 0:
        img = 'take-care.png'
        continue
        