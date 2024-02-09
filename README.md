# Parser of books from the website tululu.org

These scripts downloads books in text format and their cover images, along with additional information such as the book title, author, genres, and comments.

## How to install

Python3 should already be installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## Arguments

The script parser.py for downloading books accepts the following optional arguments:

--start_id: Start book ID to download (default: 1)

--end_id: End book ID to download (default: 10)

The script parse_tululu_category.py for downloading science fiction books accepts the following optional arguments:

--start_page: Enter the number of the first page (default: 1)

--end_page: Enter the number of the last page (default: 10)

--dest_folder: Enter the directory for text, images, json to be stored in (default: the directory where the script is)

--skip_imgs: Skips images downloading

--skip_txt: Skips txt downloading

## How to run Scripts

Run the scripts using the following command:

```bash
python parser.py
```

```bash
python parse_tululu_category.py
```

## Objective of the project

The code is written for educational purposes on the online course for web developers [dvmn.org] (https://dvmn.org/)


