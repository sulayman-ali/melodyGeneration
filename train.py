import tensorflow.keras as keras
from preprocessing import generate_training_sequences, SEQUENCE_LENGTH

#corresponds to vocabulary size in training data 
OUTPUT_UNITS = 38
#specifies neuron count in each layer of network, we will only use one LSTM layer w/ 256 neurons
NUM_UNITS = [256]
#loss function
LOSS = "sparse_categorical_crossentropy"
#learning rate
LEARNING_RATE = 0.001
EPOCHS = 50
BATCH_SIZE = 64
SAVE_MODEL_PATH = "model.h5"

def build_model(output_units, num_units, loss,learning_rate):
	#step 1: create model architecture w/ functional API

	input_layer = keras.layers.Input(shape = (None,output_units))
	lstm = keras.layers.LSTM(num_units[0])(input_layer)
	dropout = keras.layers.Dropout(0.2)(lstm)
	output_layer = keras.layers.Dense(output_units,activation="softmax")(dropout)

	model = keras.Model(input_layer,output_layer)

	#step 2: compile the model
	model.compile(loss = loss, 
				  optimizer = keras.optimizers.Adam(lr= learning_rate),
				  metrics = ["accuracy"])
	#print summary of model
	model.summary()

	return model


def train(output_units = OUTPUT_UNITS, num_units = NUM_UNITS, loss = LOSS, learning_rate = LEARNING_RATE):
	#high level function which goes through all necessary steps to run network

	#step 1: generate training sequences
	inputs, targets = generate_training_sequences(SEQUENCE_LENGTH)

	#step 2: build our LSTM network
	model = build_model(output_units, num_units, loss,learning_rate)

	#step 3: train the model
	model.fit(inputs,targets,epochs=EPOCHS, batch_size = BATCH_SIZE)

	#step 4: save the model
	model.save(SAVE_MODEL_PATH)

if __name__ == "__main__":
	train()
