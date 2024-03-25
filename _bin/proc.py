#!/usr/bin/env python3
# python -m venv --prompt podcast %USERPROFILE%/.venv/podcast.venv
# CALL %USERPROFILE%\.venv\podcast.venv\Scripts\activate.bat
# python -m pip install --upgrade pip wheel
# pip install --upgrade pyyaml pydub

from pprint import pprint
import os
import re
import time
import copy
from argparse import ArgumentParser

import yaml
import pydub

IDS = [
    'bettywu-journeytothewest',
    'goodnightmoon-gullivertravels',
    'goodnightmoon-littleprince',
    'goodnightmoon-pinocchio',
    'goodnightmoon-tomsawyer',
    'goodnightmoon-huckleberryfinn',
]

def main():
    parser = ArgumentParser()
    parser.add_argument('-u', '--update_time', action="store_true")
    args = parser.parse_args()

    for id in IDS:
        yml = f"_data/podcasts/{id}.yml"

        items = {}
        ydata = {}
        if not os.path.lexists(yml):
            ydata['title'] = ""
            ydata['description'] = ""
            ydata['items'] = []
        else:
            with open(yml, "r", encoding="utf-8") as fyml:
                ydata = yaml.full_load(fyml)
                for item in ydata['items']:
                    items[item['title'][0:2]] = item
        
        orig = copy.deepcopy(ydata)
        
        for fn in os.listdir(id):
            if not fn.endswith(".mp3"):
                continue
            dd = fn[0:2]
            info = pydub.utils.mediainfo(f'.\{id}\{fn}')
            it = {
                'title': fn,
                'size': info['size'],
                'duration': int(float(info['duration']))
            }
            if dd not in items:
                ydata['items'].append(it)
            elif not re.match(r'\d\d\.mp3', fn):
                items[dd] = it
            else:
                items[dd]['size'] = it['size']
                items[dd]['duration'] = it['duration']
        
        if 'time' not in ydata or ydata['time'] is None or len(ydata['time']) == 0 or args.update_time:
            ydata['time'] = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
        
        with open(yml, "w", encoding="utf-8", newline='\n') as yml:
            yml.write(f"title: {ydata['title'] or ''}\n")
            yml.write(f"description: {ydata['description'] or ''}\n")
            yml.write(f"time: {ydata['time']}\n")
            yml.write(f"items:\n")
            for item in ydata['items']:
              yml.write(f"  - title: {item['title']}\n")
              yml.write(f"    size: {item['size']}\n")
              yml.write(f"    duration: {item['duration']}\n")

            



if __name__ == '__main__':
    main()
