import zipfile
import os
import pandas as pd
import numpy as np
import glob
import string
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
# Specify the file path
file_path = r'C:\Users\Admin\Document-Summarization\BBCNews_archive.zip'

# Extract the ZIP file
with zipfile.ZipFile(file_path, 'r') as zip_ref:
    zip_ref.extractall()

# Specify the parent folder path
parent_folder = 'BBC News Summary'

# Specify the news articles and summaries folder paths
articles_folder = os.path.join(parent_folder, 'News Articles')
summaries_folder = os.path.join(parent_folder, 'Summaries')

# Print the list of files in the articles folder
print('News Articles:')
for file_name in os.listdir(articles_folder):
    file_path = os.path.join(articles_folder, file_name)
    if os.path.isfile(file_path):  # Check if it's a file and not a subdirectory
        print(file_name)
        
# Print the list of files in the summaries folder
print('\nSummaries:')
for file_name in os.listdir(summaries_folder):
    file_path = os.path.join(summaries_folder, file_name)
    if os.path.isfile(file_path):  # Check if it's a file and not a subdirectory
        print(file_name)

# Get the file paths for articles and summaries
articles_path = glob.glob(os.path.join(articles_folder, "*/*.txt"))
summaries_path = glob.glob(os.path.join(summaries_folder, "*/*.txt"))

# Loading the data into arrays
articles = []
summaries = []
categories = []

for article_path, summary_path in zip(articles_path, summaries_path):
    with open(article_path, "r", encoding="ISO-8859-1") as article_file:
        article_text = article_file.read()
        articles.append(article_text)
        
    with open(summary_path, "r", encoding="ISO-8859-1") as summary_file:
        summary_text = summary_file.read()
        summaries.append(summary_text)
        category = os.path.basename(os.path.dirname(article_path))
        categories.append(category)

# Creating pandas DataFrame
df = pd.DataFrame({
    'Articles': articles,
    'Summaries': summaries,
    'Categories': categories
})

# Print DataFramedf
# print(df)


# let's remove punctuation 
def rem_punct(text): 
    translator = str.maketrans('', '', string.punctuation) 
    return text.translate(translator) 

df['Clean Article'] = df["Articles"].apply(rem_punct)
df['Clean Summaries'] = df['Summaries'].apply(rem_punct)
# df.head()


# let's remove stopwords 
nltk.download('stopwords')
nltk.download('punkt')
  
# remove stopwords function 
def rem_stopwords(text): 
    stop_words = set(stopwords.words("english")) 
    word_tokens = word_tokenize(text) 
    filtered_text = [word for word in word_tokens if word not in stop_words] 
    return filtered_text 

df['Clean Article'] = df["Clean Article"].apply(rem_stopwords)
df['Clean Summaries'] = df['Clean Summaries'].apply(rem_stopwords)
print(df.head())

