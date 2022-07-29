import os

try:
    os.chdir("fff")

except FileNotFoundError:
    print("?")