import os 
import music21 as m21
from music21 import environment
import unittest
import json 
#m21 can parse kern, MIDI, MusicXML files and convert and revert these files @ will. Represents music in an OOP manner. 

KERN_DATASET_PATH = "data/test"
ACCEPTABLE_DURATIONS = [0.25,0.5, 0.75,1.0,1.5,2,3,4]
SAVE_DIR = 'dataset'
SINGLE_FILE_DATASET = "file_dataset"
SEQUENCE_LENGTH = 64
MAPPING_PATH = "vocabulary.json"

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

	for note in song.flat.notesAndRests:
		if note.duration.quarterLength not in acceptable_durations:
			return False

	return True

def transpose(song):
	'''expects music21 song object
	   returns song tranposed to Cmaj/Amin (depending on song's origin mode) | 
	   Done so generative model does not have to learn all 24 musical keys
	'''

	#get key from song | usually stored @ index 4 of first measure
	parts = song.getElementsByClass(m21.stream.Part) 
	part_0_measure = parts[0].getElementsByClass(m21.stream.Measure)
		#take first measure's 4th element to extract the key 
	key = part_0_measure[0][4]

	#check if key was actually notated in a song or not.
	if not isinstance(key, m21.key.Key):
		#use m21 to estimate the key
		key = song.analyze("key")

	#get interval for transposition | ex: if song is in Bmaj --> Cmaj, we need to transpose song by an interval 
	#check if song is in major or minor
	if key.mode == "major":
		#calculate interval from origin key to destination pitch (C)
		interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("C"))

	elif key.mode == "minor":
		#calculate interval from origin key to destination pitch (A)
		interval = m21.interval.Interval(key.tonic, m21.pitch.Pitch("A"))

	#tranpose the song by the calculated interval
	transposed_song = song.transpose(interval)
	return transposed_song

def encode_song(song, time_step = 0.25):
	'''
	p = 60, d = 1 -> [60,"_","_","_"]
	expects music21 object
	returns string of time series representation of that object 

	'''
	encoded_song = []

	for event in song.flat.notesAndRests:

		#handle notes
		if isinstance(event, m21.note.Note):
			symbol = event.pitch.midi

		elif isinstance(event, m21.note.Rest):
			symbol = "r"

		#converts symbols into time series notation
		steps = int(event.duration.quarterLength/time_step)
		for step in range(steps):
			if step == 0:
				encoded_song.append(symbol)
			else:
				encoded_song.append("_")

	#convert encoded_song to string form
	encoded_song = " ".join(map(str,encoded_song))

	return encoded_song
			

def preprocess(dataset_path):

	#load the data
	print("Loading songs ... ")
	songs = load_songs_in_kern(dataset_path)
	print(f"{len(songs)} songs loaded")

	for i, song in enumerate(songs):
		#filter out songs which  have non-acceptable durations 
		if not has_acceptable_durations(song,ACCEPTABLE_DURATIONS):
			print("unnacceptable")
			continue

		#transpose all songs to Cmajor/Amin 
		song = transpose(song)

		#encode songs w/ music time series representation
		encoded_song = encode_song(song)

		#save the songs to text file
		file_name = str(i) + "_encoded"
		save_path = os.path.join(SAVE_DIR, file_name)

		with open(save_path,"w") as fp:
			fp.write(encoded_song)

def load(file_path):
    with open(file_path, "r") as fp:
        song = fp.read()
    return song

def create_single_file_dataset(dataset_path,file_dataset_path,sequence_length):
	
	new_song_delimiter = "/ " * sequence_length

	songs = ""
	#load encoded songs and add delimiters
	for path, _, folder in os.walk(dataset_path):  #
		for file in folder:
			file_path = os.path.join(path,file)
			song = load(file_path)
			songs = songs + song + " " + new_song_delimiter

	songs = songs[:-1] #remove empty space
	#save the string containing data
	with open(file_dataset_path, "w") as fdp:
		fdp.write(songs)

	return songs 

def create_mapping(songs, mapping_path):

	#define grammar
	mappings = {}

	songs = songs.split()
	vocabulary = list(set(songs))
	for i, symbol in enumerate(vocabulary):
		mappings[symbol] = i 

	#save grammar to JSON
	with open(mapping_path,"w") as mp:
		json.dump(mappings,mp,indent = 4)

# class TestPreprocessing(unittest.TestCase):
# 	pass

def main():
	preprocess(KERN_DATASET_PATH)
	songs = create_single_file_dataset(SAVE_DIR,SINGLE_FILE_DATASET,SEQUENCE_LENGTH)
	create_mapping(songs,MAPPING_PATH)

if __name__ == "__main__":
	# songs = load_songs_in_kern(KERN_DATASET_PATH)
	# print(f"Loaded {len(songs)} songs")
	# #isolate song
	# #song = songs[0]
	main()
	# try:
	# 	#song.show()
	# except:
		#us = environment.UserSettings()
		#us['musicxmlPath'] = '/Applications/MuseScore 3.app/Contents/MacOS/mscore'
		#song.show()
