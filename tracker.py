import pickle
import shlex
import glob
promotedMusic = None
try:
    promotedMusic = pickle.load( open( "promotedMusic.p", "rb" ) )
except:
    promotedMusic = set()

arr = shlex.split(input())
while len(arr) != 0:
    mode = arr[0]
    if mode == "demote":
        for path in glob.glob(arr[1]):
            if path in promotedMusic:
                print("\tDemoting '" + path + "' from favorites.")
            promotedMusic.discard(path)
    elif mode == "promote":
        for path in glob.glob(arr[1]):
            if path not in promotedMusic:
                print("\tPromoting '" + path + "' to favorites.")
            promotedMusic.add(path)
    elif mode == "ls":
        for path in glob.glob(arr[1]):
            if path in promotedMusic:
                print("\tMatched '" + path + "'.")
    elif mode == "quit" or mode == "q":
        break
    elif mode == "help":
        print("\tUse 'promote [glob]' to promote songs.")
        print("\tUse 'demote [glob]' to demote songs.")
        print("\tUse 'ls [glob]' to see what matching songs are in favorites.")
        print("\tUse 'quit', 'q', or an empty line of input to commit changes and exit.")
        print("\tUse 'help' to list commands.")
    arr = shlex.split(input())
print("Committed.")
pickle.dump( promotedMusic, open( "promotedMusic.p", "wb" ) )
