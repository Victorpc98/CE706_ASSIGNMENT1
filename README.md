# CE706_ASSIGNMENT1
CE706 - INFORMATION RETRIEVAL ASSIGNMENT 1

# Src Code

## URLDownloader

The URLDownloader module will download a given URL and return the html as plain text. 

## Parser

The Parser module will download a given URL using the URLDownloader module and parse it's content to extract all the visible
data. 

## Preprocessing

The Preprocessing module will receive a plain text and preprocess it, separating it in documents and tokens from the collection.

* The downloaded HTML is called the collection
* A document is every line or sentence in the HTML
* A token is every word contained in a document

## Pos

The Pos module will compute the Part Of Speach Tags for every token

## KeywordsFilter

The KeywordsFilter module will compute wich words and sentences are more important for indexing. To do so, it will compute
the Inverse Document Frequency (IDF) as log(N/DFT), where

* N : The number
