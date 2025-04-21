import pandas as pd
import os
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain.schema import Document 

# Load the CSV file
df = pd.read_csv('brands_flattened_complete.csv', header=0, index_col=False, encoding='utf-8')

# Initialize an empty list to store the sentences
entire_text = []

# Iterate over each row in the DataFrame
for _, row in df.iterrows():
    # Start with the base sentence
    sentence = f"The {row['name-en']} brand has a model called {row['model-name-en']}, which is available as a {row['type-name-en']} type in the years {row['type-years']}."
    
    # Add all features (from 'Gearbox' to the end of the columns)
    # Add all features (from 'Gearbox' to the end of the columns)
    for col in df.columns[df.columns.get_loc('Gearbox'):]:  # Get all columns starting from 'Gearbox'
        feature_value = row[col]
        if pd.notna(feature_value):  # Only include non-NaN values
            if feature_value is True:  # If the feature is `true`
                entire_text.append(f"the {row['type-name-en']} type of {row['model-name-en']} model of {row['name-en']} brand has {col}")
            elif feature_value is False:  # If the feature is `false`
                entire_text.append(f"the {row['type-name-en']} type of {row['model-name-en']} model of {row['name-en']} brand doesn't have {col}")
            else:  # For other values (e.g., strings, numbers)
                entire_text.append(f"the {col} of the {row['type-name-en']} type of {row['model-name-en']} model of {row['name-en']} brand is {feature_value}")
       
    # Add the sentence to the list
    entire_text.append(sentence)

# Print the first few sentences to verify
#print(entire_text[:1])


###################################################
# Create a Chroma vector store from the sentences
db_path = "db"  # Path to store the vector store

# Initialize the embedding model
embedding = OllamaEmbeddings(model="mxbai-embed-large")

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=100)
documents = [Document(page_content=text) for text in entire_text]
chunks = text_splitter.split_documents(documents)

# Create a Chroma vector store from the chunks
vector_store = Chroma.from_documents(
    documents=chunks, embedding=embedding, persist_directory=db_path
)
vector_store.persist()
print("Vector store created and persisted.")


