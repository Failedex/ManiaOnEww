# Osu mania, made on [EWW](https://github.com/elkowar/eww)

This project marks the end of my sanity.

## Dependencies 
Currently runs on wayland
- eww (obviously)
- python 
- sox (play)

## Usage 
```
eww -c ./ open mania
```
Keys are d, f, j, k for each lane respectively

Stuff can be edited through `scripts/mania.py`, like fps, offset, difficulty, and keys.

## Notes 
- If you can't tell, Eww is not made for this. That doesn't stop me from trying though.
- There are no hold notes yet, the script just treats it as a normal hit note.
- I used the timing window from Phigros.
- The code is Spaghetti. Doesn't help that I've never actually used threads before.
- [This](https://osu.ppy.sh/beatmapsets/1797319#mania/3685612) is the beatmap I used.
- I don't actually osu mania, so a lot of other things could also be wrong.
