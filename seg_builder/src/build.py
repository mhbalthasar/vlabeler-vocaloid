#!/bin/env python3
import sys
from build_as import main as as_main
from build_seg import main as seg_main

def main(argv):
    if len(argv)==0:
        print("This command is combine the build_seg and build_as\n")
        print("build.py [wav_folder]")
        print("Enhanced settings:")
        print("\tcommand:\tbuild.py [wav_folder] [pin_length]")
        print("\tintroduce:\tpin_length\tdefault: -1, pin_length is a value in milliseconds. When the distance between two rows between the previous marker's ed and the current marker's ph1 is less than this value, ph1 is adjusted to merge into one row at ed's position. Similarly, when two marker regions overlap, the same operation is done to avoid pronunciation faults. This feature is turned off if pin_length is negative.")
        return
    seg_main(argv)
    as_main(argv)
    
if __name__=="__main__":
    main(sys.argv[1:])