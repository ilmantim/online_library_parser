# Parser of books from the website tululu.org

This script downloads books in text format and their cover images, along with additional information such as the book title, author, genres, and comments.

## How to install

Python3 should already be installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## Arguments

The script accepts the following optional arguments:

--start_id: Start book ID to download (default: 1)

--end_id: End book ID to download (default: 10)

## How to run Script

Run the script using the following command:

```bash
python parser.py
```

## Objective of the project

The code is written for educational purposes on the online course for web developers [dvmn.org] (https://dvmn.org/)


