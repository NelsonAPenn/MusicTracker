import re
import pickle
import shlex
import glob
import os
import errno
from shutil import copyfile


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise


promoted_music = pickle.load( open( "promoted_music.p", "rb" ) )

with open("source") as f:
    source = f.read().strip()

with open("destination") as f:
    destination = f.read().strip()

if len(re.findall("(M|m)usic", destination)) == 0:
    # Caution against performing this action on any very important, non-music folder
    raise ValueError("Caution")
    exit()

if destination[-1] != '/':
    destination += '/'

updated_promoted_music = promoted_music.copy()
for song in promoted_music: # Remove any possible stragglers
    if not os.path.exists(f"{source}/{song}"):
        print(f"Removing nonexistent song '{song}' from list of favorites.")
        updated_promoted_music.discard(song)

print("Proceed? (y/n)")
response = input()

if response.lower() != "y":
    print("Aborting.")
    exit()

promoted_music = updated_promoted_music.copy()

for subdir, dirs, files in os.walk(destination):
    for f in files:
        absolute = os.path.join(subdir, f)
        relative = absolute[len(destination):]
        if relative not in promoted_music:
            print(f"Removing (probably) demoted song '{relative}' from destination.")
            os.remove(absolute)

for song in promoted_music:
    abs_dest_path = destination + song
    if not os.path.exists(abs_dest_path):
        print(f"Copying new favorite '{song}' to destination.")
        mkdir_p(os.path.dirname(abs_dest_path))
        copyfile(f"{source}/{song}", abs_dest_path)

pickle.dump( promoted_music, open("promoted_music.p", "wb"))
print("Done.")
