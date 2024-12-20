# DAD - Discrete Anomaly Detection

`DAD` is a python library for discrete sequences anomaly detection. This library provides various anomaly detection methods for discrete sequences based on the techniques discussed in the paper [Anomaly Detection for Discrete Sequences: A Survey](https://ieeexplore.ieee.org/document/5645624)

##  🔄 Overview
As of today, the various anomaly detection techniques have been grouped in these three categories : 
- **Kernel based techniques**.
- **Markovian techniques**.
- **Window based techniques**.

Additionnaly, since manipulating discrete sequences often implies sequencing continuous time series, the library provides a Symbolic Aggregate approXimation (**SAX**) algorithm to convert continuous time series into discrete sequences as implemented in this paper [Experiencing SAX: a Novel Symbolic Representation of Time Series](https://link.springer.com/article/10.1007/s10618-007-0064-z).

## 💾 Installation

To set up your project environment, follow these steps:

1. Clone the project repository :
```bash
git clone https://github.com/JarrryGuillaume/DAD_library.git
```
2. Move to the project folder :
```bash
cd DAD_library
```

3. Create a virtual environment :
```bash
python -m venv venv
```
4. Activate the virtual environment :
```bash
.\venv\Scripts\activate
```
5. Install the required packages :
```bash
pip install -r requirements.txt
```

## 📘 Key Notes
Here are some important information regarding the features provided by the library
### 📏 SAX - Symbolic Aggregate approXimation
The **SAX** module allows for the transformation of **continuous sequences** into **discrete symbolic sequences**, making them compatible with the discrete anomaly detection methods implemented in this library.

#### ✨ **Available methods**
SAX converts a continuous time series into a sequence of symbols (like **A, B, C, ...**) by:  
1. **Segmenting** the series into fixed-size windows.  
2. **Normalizing** each window to a standard distribution.  
3. **Mapping** each segment to a symbol from a pre-defined alphabet (like A, B, C, D, etc.).  

This enables you to **apply discrete sequence anomaly detection techniques** to **continuous data**.  

### 🧮 Kernel Based Techniques

These methods rely on a **kernel** to compute a distance or similarity between sequences. From a training set, the library builds a **similarity matrix** (which can be computationally heavy) to evaluate the anomaly score of new samples. 

#### ✨ **Available Methods**
- **KMedoids Based**: Performs Kmedoids on the similarity matrix and assesses test sample against the extracted medoids. 
- **Knearest Based**: Asses the test sample against all sequence of the training set and compute the **k-th nearest sample**. 

### 🚪 Window-Based Techniques
These methods split sequences into smaller fixed-size windows, assign an anomaly score to each window, and aggregate them (mean, median, or other) to get the final anomaly score.

#### ✨ **Available Methods**

- **Lookahead**: Extracts sliding windows and predicts anomalies based on lookahead criteria.
- **NormalDictionary**: Compares windows against a *normal* dictionary to identify anomalies.
- **UnsupervisedSVM**: Uses a one-class SVM to classify windows as normal or anomalous.

### 🎲 **Markovian Techniques**
These methods leverage Markov models (both fixed and variable) for sequence modeling and anomaly detection. They are suitable for modeling sequences with probabilistic dependencies between elements.

#### ✨ **Available Methods**
- **Fixed Markov**: Assumes the current state depends only on the previous state.
- **Sparse Markov Transducer (SMT)**: Uses a sparse suffix tree to capture dependencies with variable-length contexts.
- **Variable Markov Techniques:** Adapts context length for better detection.
- **Hidden Markov Model (HMM):** Uses a probabilistic model where observed sequences are influenced by hidden states.

## ⚙️ **Example Usage**
```python
from KernelBased import MedoidsKernel, KnearestKernel

# Initialize and train the KMedoids method
kmedoids = MedoidsKernel(n_clusters=3)
kmedoids.train(train_sequences)

# Get anomaly score for a test sequence
score = kmedoids.predict_sample(test_sequence)

# Initialize and train the KNearest method
knearest = KnearestKernel(k=5)
knearest.train(train_sequences)

# Get anomaly score for a test sequence
score = knearest.predict_sample(test_sequence)
```
For detailed usage examples, check out the [example notebook](computer_dataset.ipynb) 📝.
