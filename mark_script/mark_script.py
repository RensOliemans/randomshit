import os
import eyed3
import time

start = time.time()
print('This program changes the ID3 tags of all .mp3 files '
      'in this directory.\n' +
      'The files have to have the format "<song name> - <song artist>.mp3"\n')
mp3files = [f for f in os.listdir() if f[-4:] == '.mp3']
features = ['featuring', 'feat.', 'ft.', 'FT.', 'FEAT.', 'feat', 'ft', 'FT',
            'FEAT', 'Feat.', 'Feat']
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
    rest = text[1][:-4]
    title = None
    for feature_text in features:
        if feature_text in rest:
            # todo: get featured artist from title and append to artist
            splitted = rest.split(feature_text)
            title = splitted[0]
            featured_artist = splitted[1]
            artist += ' ft.' + featured_artist
            break

    if not title:
        title = rest

    audiofile = eyed3.load(f)
    try:
        audiofile.tag.artist, audiofile.tag.title = artist, title
    except:
        print(f)
    audiofile.tag.save()
    os.rename(f, title + ".mp3")

if incorrect_files:
    print("There were {} incorrectly named files".format(incorrect_files))
print("Changed tags of {} files. It took {:.3} seconds."
      .format(len(mp3files) - incorrect_files, time.time() - start))
