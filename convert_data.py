#%%
import csv
import os


reader = csv.reader(open('./covid/covid.csv'))

sentences = set()

for row in reader:
    for question in row[22:27]:
        if len(question) > 0:
            sentences.add(question)

# Add to txt file
with open('data/models/pretrained_transformers/JHUcorona.txt', 'w+') as f:
    f.writelines([f'{q}\n' for q in sentences])
#%%