import os

for datei in os.listdir("Tables"):
    print (datei[-5:].lower())