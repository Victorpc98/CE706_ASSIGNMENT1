# CE706_ASSIGNMENT1

## Members

* Víctor Pérez Cester 	(vp19885@essex.ac.uk) ->	1900232
* Joel Valiente Sanchez (jv19228@essex.ac.uk) ->	1900289

## How to Run

To run the project you must install all the dependencies first by running the following command on your linux terminal.

    pip3 install -r requirements.txt

Once all the dependencies are installed, you can execute the code as above.

    python3 main.py --url <your_url_to_parse>

If you want the system to be verbose you can add the --verbose flag as above.

    python3 main.py --url <your_url_to_parse> --verbose

Once the code finished the execution you can check the outputs inside the output/ folder.


## Src Code
Provided in /src/ folder.

### URLDownloader

The URLDownloader module will download a given URL and return the html as plain text. 

### Parser

The Parser module will download a given URL using the URLDownloader module and parse it's content to extract all the visible
data. 

### Preprocessing

The Preprocessing module will receive a plain text and preprocess it, separating it in documents and tokens from the collection.

* The downloaded HTML is called the collection
* A document is every line or sentence in the HTML
* A token is every word contained in a document

### Pos

The Pos module will compute the Part Of Speach Tags for every token.

### KeywordsFilter

The KeywordsFilter module will compute wich words and sentences are more important for indexing. To do so, it will compute
the Inverse Document Frequency (IDF) as log(N/DFT), where

* N : The number of documents in our collection.
* DFT: Document Frequency Term

The Term Frequency table will be computed as well and, mixing both results, the table TF-IDF will be computed.

### Stemming 
The Stemming module is dedicated to compute the stems for every token. It uses the WordNetLemmatizer class from the nltk module to compute the stems. 
