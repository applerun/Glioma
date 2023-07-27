import numpy as np
import matplotlib.pyplot as plt

Training = np.array([84, 130, 53], dtype = "float")
Validation = np.array([237, 125, 49], dtype = "float")
Testing = np.array([255, 0, 0], dtype = "float")
ProcessedDataset = np.array([68, 114, 196], dtype = "float")
Modeling1 = ((Training + Validation) / 2).astype("int")
Modeling2 = ((Modeling1+ProcessedDataset)/2).astype("int")
print(Modeling1)
print(Modeling2)
print(((Training*8+Validation+Testing)/10).astype("int"))