import os
import psutil
import time

def close_all_applications():
    # Add your code here to close all running applications
    os.system("taskkill /f /fi \"status eq running\"")

def clean_memory():
    # Close all open Chrome windows
    os.system("taskkill /f /im chrome.exe")

while True:
    close_all_applications()
    # clean_memory()
    time.sleep(3600)  # Wait for 1 hour (3600 seconds)
