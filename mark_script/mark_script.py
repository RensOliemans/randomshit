import os
import eyed3
import time

start = time.time()
print('This program changes the ID3 tags of all .mp3 files '
      'in this directory.\n' +
      'The files have to have the format "<song name> - <song artist>.mp3"\n')
mp3files = [f for f in os.listdir() if f[-4:] == '.mp3']
incorrect_files = 0
for f in mp3files:
    # format of filename: <song_name> - <song_artist>.mp3 (including space)
    text = f.split(' - ')
    if not len(text) == 2:
        # incorrect format, skip this file
        print("Tag of file '{}' won't be changed, the format is incorrect"
              .format(f))
        incorrect_files += 1
        continue

    artist = text[0]
    title = text[1][:-4]

    audiofile = eyed3.load(f)
    audiofile.tag.artist, audiofile.tag.title = artist, title
    audiofile.tag.save()

if incorrect_files:
    print("There were {} incorrectly named files".format(incorrect_files))
print("Changed tags of {} files. It took {:.3} seconds."
      .format(len(mp3files) - incorrect_files, time.time() - start))
