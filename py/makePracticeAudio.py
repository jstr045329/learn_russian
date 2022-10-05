import os
import sys
import argparse
from random import shuffle
from pydub import AudioSegment

def getFileList():
    if os.name == "nt":
        s = os.popen('dir wav\*.wav').read()
    else:
        s = os.popen("ls -l wav/*.wav").read()
    los = s.split()
    return [x for x in los if x[-4:] == ".wav"]

def main():
    cmdLineParser = argparse.ArgumentParser(description="Concatenate Random IO files")
    cmdLineParser.add_argument("-t", "--time", action="store", type=int, dest="time", default=60, help="length of resulting audio file in minutes")
    cmdLineParser.add_argument("-r", "--repetitions", action="store", type=int, dest="repetitions", default=3, help="Number of times to repeat each word")
    args = cmdLineParser.parse_args()
    my_file_list = getFileList()
    # Sometimes shuffle doesn't work very well so shuffle multiple times:
    shuffle(my_file_list)
    shuffle(my_file_list)
    shuffle(my_file_list)
    time_goal = 60 * args.time
    total_time = 0
    output_sound = AudioSegment.from_wav("wav" + os.sep + my_file_list[0])
    for i in range(1, args.repetitions):
        output_sound += AudioSegment.from_wav("wav" + os.sep + my_file_list[0])
    idx = 1
    while total_time < time_goal:
        one_file_name = "wav" + os.sep + my_file_list[idx]
        print("Adding %s" % (one_file_name))
        new_sound = AudioSegment.from_wav(one_file_name)
        for i in range(args.repetitions):
            output_sound += new_sound
        total_time += new_sound.duration_seconds
        print("Total time is: %.2f" % (total_time))
        idx += 1
        if idx >= len(my_file_list):
            idx = 0
            shuffle(my_file_list)
            shuffle(my_file_list)
            shuffle(my_file_list)
    output_sound.export("my_lesson.mp3", format="mp3")
    
if __name__ == "__main__":
    main()
