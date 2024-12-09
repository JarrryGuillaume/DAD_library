import matplotlib.pyplot as plt
import numpy as np 
from matplotlib.gridspec import GridSpec
from .markov_sequence import MarkovSequenceGenerator
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score

class MarkowDataset: 
    def __init__(self, train_set, test_set, labels):
        self.train = np.array(train_set)
        self.test = np.array(test_set)
        self.labels = np.array(labels)

class MarkovianBenchMark: 
    def __init__(self, 
                 model, 
                 n_symbols_list, 
                 n_states_list, 
                 dataset_size=1000, 
                 sequence_length=100,

                 # Test kwarg
                 proportion_anomalous=0.5,
                 n_anomaly_generator=5, 
                 nbins=20,
                ): 
        self.model = model
        self.n_symbols_list = n_symbols_list
        self.n_states_list = n_states_list
        self.dataset_size = dataset_size
        self.sequence_length = sequence_length
        
        self.proportion_anomalous = proportion_anomalous
        self.n_anomaly_generator = n_anomaly_generator

        self.nbins = nbins
        
    def generate_dataset(self, n_symbols, n_states):
        train_generator = MarkovSequenceGenerator(n_states=n_states, n_symbols=n_symbols, sequence_length=self.sequence_length)
        train_set = train_generator.generate_all_sequences(self.dataset_size)

        n_good = int((1 - self.proportion_anomalous) * self.dataset_size)
        n_bad = int((self.dataset_size - n_good) / self.n_anomaly_generator)

        good_data = train_generator.generate_all_sequences(n_good)

        bad_data = []
        for _ in range(self.n_anomaly_generator): 
            anomaly = MarkovSequenceGenerator(n_states=n_states, n_symbols=n_symbols, sequence_length=self.sequence_length).generate_all_sequences(n_bad)
            bad_data.extend(anomaly)
        
        test_set = good_data + bad_data
        labels = [0 for _ in range(n_good)] + [1 for _ in range(n_bad * self.n_anomaly_generator)]
        return MarkowDataset(train_set, test_set, labels)    

    def plot_distribution(self, n_symbols, n_states, labels, anomaly_scores, ax):      
        good = anomaly_scores[~labels]
        bad = anomaly_scores[labels]
        ax.hist(good, label="baseline", bins=self.nbins)
        ax.hist(bad, label="anomaly", bins=self.nbins)
        ax.set_title(f"n symbols {n_symbols} : hidden states {n_states}")
        ax.set_xlabel("anomaly score")
        ax.set_ylabel("n samples")
        ax.legend()

    def benchmark(self): 
        fig = plt.figure(figsize=(15, 10))
        n_plot = int(len(self.n_symbols_list) / 2 + 1/2) 
        print(n_plot)
        gs = GridSpec(n_plot, 2)

        for i, (n_symbols, n_states) in enumerate(zip(self.n_symbols_list, self.n_states_list)): 
            dataset = self.generate_dataset(n_symbols, n_states)

            self.model.train(dataset.train)
            anomaly_scores = self.model.predict_proba(dataset.test)
            predictions = self.model.predict(dataset.test)

            precision = precision_score(dataset.labels, predictions)
            recall = recall_score(dataset.labels, predictions)
            accuracy = accuracy_score(dataset.labels, predictions)
            f1 = f1_score(dataset.labels, predictions)

            print("=======================")
            print(f"Model : {type(self.model)}")
            print(f"precision : {precision}")
            print(f"recall : {recall}")
            print(f"accuracy : {accuracy}")
            print(f"f1 : {f1}")

            ax = fig.add_subplot(gs[i % n_plot, i > n_plot - 1])
            self.plot_distribution(n_symbols, n_states, dataset.labels, anomaly_scores, ax)

            self.model.reset()

        plt.show()
