from tensorflow import keras
from tensorflow.keras.optimizers.legacy import SGD
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, TensorBoard
import keras_tuner as kt
from backend.common.util import get_training_data
import numpy as np
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

class MarcHyperModel(kt.HyperModel):
    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape
    
    def build(self, hp):
        model = Sequential()

        first_layer_neurons = hp.Int("first_layer_neurons", min_value=32, max_value=128, step=32)
        first_layer_activation = hp.Choice("first_layer_activation", values=["relu", "gelu", "elu", "selu"])

        model.add(Dense(units=first_layer_neurons, 
                        input_shape=self.input_shape, 
                        activation=first_layer_activation))
        
        if hp.Boolean("first_dropout"):
            model.add(Dropout(0.5))

        second_layer_neurons = hp.Int("second_layer_neurons", min_value=32, max_value=128, step=32)
        second_layer_activation = hp.Choice("second_layer_activation", values=["relu", "gelu", "elu", "selu"])

        model.add(Dense(units=second_layer_neurons, activation=second_layer_activation))

        if hp.Boolean("second_dropout"):
            model.add(Dropout(0.5))
        
        model.add(Dense(self.output_shape, activation="softmax"))

        optimizer_lr = hp.Choice("learning_rate", values=[1e-2, 1e-3, 1e-4])

        sgd = SGD(learning_rate=optimizer_lr, decay=1e-6, momentum=0.9, nesterov=True)
        adam = Adam(learning_rate=optimizer_lr)

        optimizer = hp.Choice("optimizer", values=['sgd', 'adam'])

        if optimizer == 'adam':
            model.compile(loss="categorical_crossentropy", optimizer=adam, metrics=["accuracy"])
        elif optimizer == 'sgd':
            model.compile(loss="categorical_crossentropy", optimizer=sgd, metrics=["accuracy"])
        
        return model

def hyperparameter_tuning():
    # Create Hypermodel
    train_x, train_y = get_training_data()
    hypermodel = MarcHyperModel(input_shape=(len(train_x[0]),), output_shape=len(train_y[0]))
    
    # Define Tuner
    tuner = kt.Hyperband(hypermodel,
                     objective='val_accuracy',
                     max_epochs=10,
                     factor=3,
                     directory=f"{__location__}/model",
                     project_name='marc')

    # Search For Hyperparameters
    stop_early = EarlyStopping(monitor='val_loss', patience=5)

    tuner.search(np.array(train_x).astype("float32"),
                 np.array(train_y).astype("float32"),
                 epochs=50,
                 validation_split=0.3,
                 callbacks=[stop_early, TensorBoard(f"{__location__}/model/hp_logs")])

    optimal_hp = tuner.get_best_hyperparameters()[0]
    
    # Create Model Using Hyperparameters
    best_model = tuner.hypermodel.build(optimal_hp)

    # Determine Epochs
    history = best_model.fit(np.array(train_x, dtype=object).astype('float32'), 
                np.array(train_y, dtype=object).astype('float32'),
                epochs=100,
                validation_split=0.3)
    accuracy_per_epoch = history.history["val_accuracy"]
    best_epoch = accuracy_per_epoch.index(max(accuracy_per_epoch)) + 1

    # Build Final Model & Evaluate
    model = tuner.hypermodel.build(optimal_hp)
    model.fit(np.array(train_x, dtype=object).astype('float32'), 
              np.array(train_y, dtype=object).astype('float32'),
              epochs=best_epoch,
              validation_split=0.2)

    print(f"""
    === HYPERPARAMETERS RESULTS ===
    Units 1: {optimal_hp.get('first_layer_neurons')}.
    Activation 1: {optimal_hp.get('first_layer_activation')}.
    Dropout 1: {optimal_hp.get("first_dropout")}

    Units 2: {optimal_hp.get('second_layer_neurons')}.
    Activation 2: {optimal_hp.get('second_layer_activation')}.
    Dropout 2: {optimal_hp.get("second_dropout")}

    Optimizer: {optimal_hp.get('optimizer')}
    Optimizer Learning Rate: {optimal_hp.get('learning_rate')}
    
    Best Epoch: {best_epoch}
    """)

if __name__ == "__main__":
    hyperparameter_tuning()

    