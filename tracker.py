import pickle
import shlex
import glob
import sys
from itertools import chain

with open("source") as f:
    music_folder_path = f.read().strip()

def music_generator(glob_path):
    absolute_glob_path = f"{music_folder_path}/{glob_path}"
    for absolute_path in glob.glob(absolute_glob_path, recursive=True):
        path = absolute_path[len(music_folder_path) + 1:]
        yield path

promoted_music = None

try:
    promoted_music = pickle.load( open( "promoted_music.p", "rb" ) )
except:
    promoted_music = set()

# print("music$ ", end="")
for line in sys.stdin:
    try:
        arr = shlex.split(line)
    except:
        print("\tMalformed input.")
        continue

    if len(arr) == 0:
        continue

    mode = arr[0]

    if mode == "demote":
        if len(arr) < 2:
            print("\tInvalid command.")
            continue

        for path in music_generator( arr[1] ):
            if path in promoted_music:
                print("\tDemoting '" + path + "' from favorites.")
            promoted_music.discard(path)


    elif mode == "promote":
        if len(arr) < 2:
            print("\tInvalid command.")
            continue
        
        for path in music_generator( arr[1] ):
            if path not in promoted_music:
                print("\tPromoting '" + path + "' to favorites.")
            promoted_music.add(path)


    elif mode == "ls":
        if len(arr) > 1:
            for path in music_generator( arr[1] ):
                if path in promoted_music:
                    print(f"\tMatched '{path}'.")
        else:
            for path in promoted_music:
                print(f"\t{path}")

    
    elif mode == "diff":
        
        if len(arr) > 1:
            combined_generator = music_generator( arr[1] )
        else:
            combined_generator = chain( music_generator("*"), music_generator("**/*") )

        for path in combined_generator:
            if path in promoted_music:
                color = "01;32"
            else:
                color = "01;31"
            print(f"\t\x1B[{color}m{path}\x1B[00m")
    

    elif mode == "commit":
        pickle.dump( promoted_music, open( "promoted_music.p", "wb" ) )
        print("\tCommitted.")
    
    
    elif mode == "quit" or mode == "q":
        break
    
    
    elif mode == "help":
        print("\tUse 'promote [glob]' to promote songs.")
        print("\tUse 'demote [glob]' to demote songs.")
        print("\tUse 'ls [glob]' to see what matching songs are in favorites.")
        print("\tUse 'diff [glob]' to compare songs in favorites and those in your filesystem.")
        print("\tUse 'quit', 'q', or EOF/Ctrl-D to commit changes and exit.")
        print("\tUse 'help' to list commands.")
    
   
    else:
        print("\tInvalid command")
    # print("music$ ", end="")
    


pickle.dump( promoted_music, open( "promoted_music.p", "wb" ) )
print("")
print("Committed.")
