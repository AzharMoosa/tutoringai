from tensorflow.keras.optimizers.legacy import SGD
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.models import Sequential
import numpy as np
import pickle
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk
import os
from backend.common.conversation_engine.util import ConversationEngineUtil
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

def process_intents(intents):
    words = []
    classes = []
    documents = []
    for intent in intents["intents"][:1000]:
        for pattern in intent["patterns"]:
            word_list = word_tokenize(pattern)
            words.extend(word_list)
            documents.append(((word_list), intent["tag"]))
            if intent["tag"] not in classes:
                classes.append(intent["tag"])

    return words, classes, documents


def lemmatize_words(lemmatizer, words):
    ignore = {"?", "!", ".", ","}
    words = [lemmatizer.lemmatize(word)
             for word in words if word not in ignore]
    return sorted(set(words))


def generate_word_patterns(word_list, lemmatizer):
    return set([lemmatizer.lemmatize(word.lower()) for word in word_list])


def generate_training_data(words, classes, documents, lemmatizer):
    training_data = []

    for document in documents:
        word_list, tag = document
        word_patterns = generate_word_patterns(word_list, lemmatizer)
        bag = [1 if word in word_patterns else 0 for word in words]
        output_row = [0] * len(classes)
        output_row[classes.index(tag)] = 1
        training_data.append([bag, output_row])

    return training_data


def shuffle_dataset(dataset):
    idx = np.random.permutation(len(dataset))
    return dataset[idx]


def train_test_split(training_data):
    training_data = shuffle_dataset(training_data)
    return list(training_data[:, 0]), list(training_data[:, 1])


def train_model(train_x, train_y, epochs=500, batch_size=5, verbose=0):
    model = Sequential()
    model.add(Dense(128, input_shape=(len(train_x[0]), ), activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]), activation="softmax"))

    sgd = SGD(learning_rate=1e-2, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss="categorical_crossentropy",
                  optimizer=sgd, metrics=["accuracy"])
    hist = model.fit(np.array(train_x, dtype=object).astype('float32'), np.array(train_y, dtype=object).astype('float32'),
                     epochs=epochs, batch_size=batch_size, verbose=verbose)
    model.save(f"{__location__}/model/chatbotmodel.h5", hist)


def train_chatbot():
    intents = ConversationEngineUtil.load_intent()
    words, classes, documents = process_intents(intents)
    lemmatizer = WordNetLemmatizer()

    words = lemmatize_words(lemmatizer, words)
    classes = sorted(set(classes))

    pickle.dump(words, open(f"{__location__}/model/words.pkl", "wb"))
    pickle.dump(classes, open(f"{__location__}/model/classes.pkl", "wb"))

    training = generate_training_data(words, classes, documents, lemmatizer)

    training = np.array(training, dtype=object)
    train_x, train_y = train_test_split(training)

    train_model(train_x, train_y)

    print("Successfully Trained Chatbot!")


def get_training_data():
    intents = ConversationEngineUtil.load_intent()
    words, classes, documents = process_intents(intents)
    lemmatizer = WordNetLemmatizer()

    words = lemmatize_words(lemmatizer, words)
    classes = sorted(set(classes))

    pickle.dump(words, open(f"{__location__}/model/words.pkl", "wb"))
    pickle.dump(classes, open(f"{__location__}/model/classes.pkl", "wb"))

    training = generate_training_data(words, classes, documents, lemmatizer)

    training = np.array(training, dtype=object)
    
    train_x, train_y = train_test_split(training)

    return train_x, train_y

if __name__ == "__main__":
    train_chatbot()