import datetime
import tkinter as tk
from tkinter import messagebox
import time
import os

short_break = 1
medium_break = 3
long_break = 6
hour_count = 0

current_time = datetime.datetime.now()
    
target_time = current_time + datetime.timedelta(seconds=5)
while(True):
    while current_time < target_time:
        current_time = datetime.datetime.now()
    target_time = current_time + datetime.timedelta(seconds=5)
    hour_count += 1
    print(hour_count)
