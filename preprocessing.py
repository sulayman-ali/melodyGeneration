import os 
import music21 as m21
from music21 import environment
import unittest
#m21 can parse kern, MIDI, MusicXML files and convert and revert these files @ will. Represents musc in an OOP manner. 

KERN_DATASET_PATH = "data/test"
#Value of 4 represents a whole note, below which is a fraction of a whole note
ACCEPTABLE_DURATIONS = [0.25,0.5, 0.75,1.0,1.5,2,3,4]

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

def has_acceptable_durations(song,acceptable_durations):
	
	'''expects music21 song object. 
	   Returns True if all notes and rests within song are within predefined definitions for model. 
	'''

	for note in song.flat_.notesAndRests_:
		if note.duration.quarterLength_ not in acceptable_durations:
			return False

	return True

def preprocess(dataset_path):

	#load the data
	print("Loading songs ... ")
	songs = load_songs_in_kern(dataset_path)
	print(f"{len(songs)} songs loaded")

	#filter out songs which  have non-acceptable durations 

	#transpose all songs to Cmajor/Amin 

	#encode songs w/ music time series representation

	#save the songs to text file



class TestPreprocessing(unittest.TestCase):
	pass

if __name__ == "__main__":
	songs = load_songs_in_kern(KERN_DATASET_PATH)
	#isolate song
	song = songs[0]
	try:
		song.show()
	except:
		us = environment.UserSettings()
		us['musicxmlPath'] = '/Applications/MuseScore 3.app/Contents/MacOS/mscore'
		song.show()
