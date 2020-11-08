import os 
import music21 as m21
from music21 import environment
#m21 can parse kern, MIDI, MusicXML files and convert and revert these files @ will. Represents musc in an OOP manner. 

KERN_DATASET_PATH = "data/test"

def load_songs_in_kern(dataset_path):
	'''pass in a valid folder path holding all training songs in .krn format converts to m21 
	   and returns list of m21 objects
	'''
	songs = []
	#iterate through all data files  and load w/ music21
	for path, subdir, files in os.walk(dataset_path): 
		#recursively goes through all the files 
		for file in files:
			#load only .krn files
			if file[-3:] == "krn":
				#load w/ music 21, song is a m21 stream (m21 base class)
				song = m21.converter.parse(os.path.join(path, file))
				songs.append(song)

	return songs


def preprocess(dataset_path):

	#load the data
	print("Loading songs ... ")
	songs = load_songs_in_kern(dataset_path)
	print(f"{len(songs)} songs loaded")
	#filter out songs which  have non-acceptable durations 

	#transpose all songs to Cmajor/Amin 

	#encode songs w/ music time series representation

	#save the songs to text file

if __name__ == "__main__":
	songs = load_songs_in_kern(KERN_DATASET_PATH)
	# print(preprocess(KERN_DATASET_PATH))
	#isolate song
	song = songs[0]
	try:
		song.show()
	except:
		us = environment.UserSettings()
		us['musicxmlPath'] = '/Applications/MuseScore 3.app/Contents/MacOS/mscore'
		song.show()
