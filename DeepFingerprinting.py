import keras

class DeepFingerprintingNeuralNetwork:
	@staticmethod
	def neuralnetwork(input, N):
		model = keras.Sequential()
		no_of_internal_layers = 3
		kernel = 8
		pool = 8
		conv_stride = 1
		pool_stride = 4
		optimization_function = keras.optimizers.Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
		kernel_initialization = keras.initializers.glorot_uniform(seed=0)

		def identity_loss(y_true, y_pred):
		    neg_y_true = 1 - y_true
		    neg_y_pred = 1 - y_pred
		    false_positive = keras.backend.sum(neg_y_true * y_pred)
		    true_negative = keras.backend.sum(neg_y_true * neg_y_pred)
		    specificity  = true_negative / (true_negative + false_positive + keras.backend.epsilon())
		    return specificity

		#Block layer 1
		model.add(keras.layers.Conv1D(filters=32, kernel_size=kernel, input_shape=input, strides=conv_stride, padding='same', name='block1_convolutional_layer1'))
		model.add(keras.layers.BatchNormalization(axis=-1))
		model.add(keras.layers.ELU(alpha=1.0, name='block1_activation_layer1'))
		model.add(keras.layers.Conv1D(filters=32, kernel_size=kernel, strides=conv_stride, padding='same', name='block1_convolutional_layer2'))
		model.add(keras.layers.BatchNormalization(axis=-1))
		model.add(keras.layers.ELU(alpha=1.0, name='block1_activation_layer2'))
		model.add(keras.layers.MaxPooling1D(pool_size=pool, strides=pool_stride, padding='same', name='block1_pooling_layer'))
		model.add(keras.layers.core.Dropout(0.1, name='block1_dropout_layer'))

		#Block layers 2,3,4 connected layers
		for layer in range(1, no_of_internal_layers + 1):
			name1 = "block"+str(layer)+"_convolutional_layer" + str(layer + 2)
			name2 = "block"+str(layer)+"_convolutional_layer" + str(layer + 3)
			model.add(keras.layers.Conv1D(filters=32 * layer + 1, kernel_size=kernel, strides=conv_stride, padding='same', name=name1)) #Block Convolution layer 1
			model.add(keras.layers.BatchNormalization()) #Batch normalization
			model.add(keras.layers.core.Activation('relu', name="block"+str(layer)+"_activation_layer" + str(layer + 2))) #Block RELU Activation layer 1
			model.add(keras.layers.Conv1D(filters=32 * layer + 1, kernel_size=kernel, strides=conv_stride, padding='same', name=name2)) #Block Convolution layer 1
			model.add(keras.layers.BatchNormalization()) #Batch normalization
			model.add(keras.layers.core.Activation('relu', name="block1"+str(layer)+"_activation_layer" + str(layer + 3))) #Block RELU Activation layer 2
			model.add(keras.layers.MaxPooling1D(pool_size=pool, strides=pool_stride, padding='same')) #Max Pooling
			model.add(keras.layers.core.Dropout(0.1, name="block2"+str(layer)+"_dropout")) #Block Dropout layer

		#Fully connected layer1
		model.add(keras.layers.core.Flatten(name='flatten'))
		model.add(keras.layers.core.Dense(512, kernel_initializer=kernel_initialization, name='fully_connected_layer1'))
		model.add(keras.layers.BatchNormalization())
		model.add(keras.layers.core.Activation('relu', name='fully_connected_activation1'))
		model.add(keras.layers.core.Dropout(0.7, name='fully_connected_dropout1'))

		#Fully connected layer1
		model.add(keras.layers.core.Dense(512, kernel_initializer=kernel_initialization, name='fully_connected_layer2'))
		model.add(keras.layers.BatchNormalization())
		model.add(keras.layers.core.Activation('relu', name='fully_connected_activation2'))
		model.add(keras.layers.core.Dropout(0.5, name='fully_connected_dropout2'))

		#Output prediction
		model.add(keras.layers.core.Dense(N, kernel_initializer=kernel_initialization, name='fully_connected_layer3')) #Where N is the number of pages we are testing for
		model.add(keras.layers.core.Activation('softmax', name="softmax"))

		model.compile(loss=identity_loss, optimizer=keras.optimizers.Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0))
		return model

