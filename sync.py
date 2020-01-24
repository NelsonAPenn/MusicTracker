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


promotedMusic = pickle.load( open( "promotedMusic.p", "rb" ) )
updatedPromotedMusic = set(promotedMusic)
destination = input()


if len(re.findall("(M|m)usic", destination)) == 0:
    # Caution against performing this action on any very important, non-music folder
    raise ValueError("Caution")
    exit()

if destination[-1] != '/':
    destination += '/'

for song in promotedMusic: # Remove any possible stragglers
    if not os.path.exists("./" + song):
        print("Removing nonexistent song '" + song + "' from list of favorites.")
        updatedPromotedMusic.discard(song)

promotedMusic = set(updatedPromotedMusic)

for subdir, dirs, files in os.walk(destination):
    for f in files:
        absolute = os.path.join(subdir, f)
        relative = absolute[len(destination):]
        if relative not in promotedMusic:
            print("Removing (probably) demoted song '" + relative + "' from destination.")
            os.remove(absolute)

for song in promotedMusic:
    absDestPath = destination + song
    if not os.path.exists(absDestPath):
        print("Copying new favorite '" + song + "' to destination.")
        mkdir_p(os.path.dirname(absDestPath))
        copyfile("./" + song, absDestPath)

pickle.dump( promotedMusic, open("promotedMusic.p", "wb"))
