#!/usr/bin/env python3

import threading
import time
import json 
from collections import deque
import subprocess 
import os

eww_bin = ["eww", "-c", f"{os.path.expanduser('~')}/.config/eww/mania"]

# phigros timing window. I don't actually play mania
pwindow = 0.08
lwindow = 0.16
bwindow = 0.18
mid = 1
showtime = mid+lwindow
fps = 50

message = ""
combo = 0
debug = ""

class Lane:
    def __init__(self): 
        # q format: timestamp
        self.q = deque()
        self.t = threading.Thread(target=self.update, daemon=True)
        self.t.start()

    def update(self): 
        global combo
        global message
        while True:
            if len(self.q) == 0: 
                continue
            if showtime-(time.time() - self.q[0]) <= 0:
                message = "Miss"
                combo = 0
                self.q.popleft()

            time.sleep(1/fps)

    def get(self): 
        lane = []
        for stamp in self.q: 
            tleft = showtime - (time.time()-stamp)
            if tleft <= 0: 
                continue

            lane.append(tleft*100/showtime)

        return lane

    def add(self): 
        self.q.append(time.time())

    def hit(self): 
        global combo
        if len(self.q) == 0: 
            return ""
        t = abs((time.time()-self.q[0]) -mid)
        if t <= pwindow: 
            combo += 1
            self.q.popleft()
            return "Perfect"
        if t <= lwindow:
            combo += 1
            self.q.popleft()
            return "Ok"
        if t <= bwindow:
            combo = 0 
            self.q.popleft()
            return "Bad"

        return ""

def readinput(l): 
    global message
    global debug
    index = 0
    with open("./scripts/input.txt", "w") as f: 
        f.write("")
    while True: 
        with open("./scripts/input.txt", "r") as f:
            for c in f.read()[index:]: 
                if (c == "" or c == "\n"): 
                    continue
                if c == "d": 
                    message = l[0].hit()
                if c == "f": 
                    message = l[1].hit()
                if c == "j": 
                    message = l[2].hit()
                if c == "k": 
                    message = l[3].hit()
                index += 1
        time.sleep(1/fps) 

def track():
    # timing is the bane of my existence
    time.sleep(mid-0.51)
    subprocess.call(["play", "./beatmaps/paradise/audio.mp3"], stdout=subprocess.DEVNULL)

def chart(l): 
    s = set()
    
    objects = deque()
    with open("./beatmaps/paradise/paradisepresent.osu") as f: 
        lines = f.readlines()
        parse = False
        for line in lines: 
            if "[HitObjects]" in line:
                parse = True 
                continue
            if not parse: 
                continue
            stuff = line.split(",")
            objects.append((int(stuff[2]), int(stuff[0])))
            s.add(int(stuff[0]))

    s = list(s)
    s.sort()

    translate = {}

    for i, pos in enumerate(s): 
        translate[pos] = i
    start = time.time()

    playtrack = threading.Thread(target=track, daemon=True)
    playtrack.start()

    while len(objects) != 0: 

        while objects[0][0]/1000 <= time.time()-start:
            _, wher = objects.popleft()
            if wher in translate: 
                l[translate[wher]].add()

        time.sleep(1/fps)

def main():
    for i in range(3, 0, -1): 
        data = {
            "combo": 0, 
            "message": f"{i}", 
            "lanes": [
                [],
                [],
                [],
                [],
            ]
        }
        
        subprocess.run(eww_bin + ["update", f"mjson={json.dumps(data)}"])
        time.sleep(1)

    l = [Lane(), Lane(), Lane(), Lane()]
    readinp = threading.Thread(target=readinput, daemon=True, args=(l,))
    readinp.start()
    charting = threading.Thread(target=chart, daemon=True, args=(l,))
    charting.start()
    while True: 
        data = {
            "combo": combo, 
            "message": message, 
            "lanes": [
                l[0].get(),
                l[1].get(),
                l[2].get(),
                l[3].get(),
            ]
        }

        # print(json.dumps(data))
        subprocess.run(eww_bin + ["update", f"mjson={json.dumps(data)}"])

        time.sleep(1/fps)


if __name__ == "__main__":
    main()

