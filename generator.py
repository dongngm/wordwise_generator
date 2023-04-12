from html.parser import HTMLParser
from io import StringIO
import pandas as pd
import logging
import os
import subprocess
import multiprocessing as mp
from multiprocessing import Pool, Manager
import re
import shutil
import time


logging.basicConfig(level=logging.INFO, format='%(asctime)s [+] %(message)s')
logger = logging.getLogger()
WORD_COL = "word"
WW_COL = "short_def"
DATA_DIR = "./data"
STOPWORD_FPATH = os.path.join(DATA_DIR, "filter.txt")


class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        self.text.write(d)

    def get_data(self):
        return self.text.getvalue()


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def load_lines_fl_to_lst(fpath):
    with open(fpath, 'r', encoding="utf-8") as f:
        return [line.rstrip() for line in f]


def load_words_fl_to_lst(fpath):
    with open(fpath, 'r', encoding="utf-8") as f:
        return f.read().split()


def cleanword(word):
    word = strip_tags(word)
    word = re.sub('[^A-Za-z0-9]+', '', word)
    return word.lower()

def init_worker(words, ww_dict, stopwords):
    global shared_words
    global shared_ww_dict
    global shared_stopwords
    #
    shared_words = words
    shared_ww_dict = ww_dict
    shared_stopwords = stopwords


def ww_lookup(word_idx):
    #
    word = shared_words[word_idx]
    cleaned_word = cleanword(word)
    if cleaned_word not in shared_stopwords:
        if cleaned_word in shared_ww_dict:
            wordwise = shared_ww_dict[cleaned_word]
            logger.debug(f"[#] {cleaned_word} --> {wordwise}");
            # Replace Original Word with Wordwised
            word_ww = re.sub(
                cleaned_word,
                f"<ruby>{cleaned_word}<rt>{wordwise}</rt></ruby>",
                word
            )
            return (word_idx, word_ww)
    #
    # no change
    return (word_idx, word)


def generate(args):
    # validate args
    if not (args.out_epub or args.out_azw3 or args.out_pdf):
        logger.error("Must select at least one output format.")
        exit(1)
    #
    if args.debug:
        logger.setLevel(logging.DEBUG)
    #
    i_file, hint_level, langww, num_t = (
        args.input_file, args.hint_level, args.lang, args.num_threads
    )
    #
    bookfilename = i_file.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    logger.info(f"File to be processed: {bookfilename}")
    logger.info(f"Hint level: {hint_level}")
    # Load Stop Words
    stopwords = load_lines_fl_to_lst(STOPWORD_FPATH)
    # Load WW Dict from CSV
    df01_ww = pd.read_csv(os.path.join(DATA_DIR, f"{langww}.csv"))
    # Filter based on hint_level
    df02_ww = df01_ww[df01_ww.hint_level <= hint_level]
    assert df02_ww.shape[0] > 0 
    # Get wordwise dict: {word -> ww explanation/translation}
    ww_dict = dict(zip(df02_ww[WORD_COL],df02_ww[WW_COL]))
    # Clean temp files
    for p in ["book_dump.htmlz", "book_dump_html", "book_dump_html.zip"]:
        if os.path.isfile(p):
            os.remove(p)
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
    # Convert Book to HTML
    logger.info("Converting book to HTML format")
    subprocess.run(["ebook-convert", i_file, "book_dump.htmlz"], capture_output=True)
    subprocess.run(["ebook-convert", "book_dump.htmlz", "book_dump_html"], capture_output=True)
    # Check if conversion is successful
    if not os.path.isfile("book_dump_html/index1.html"):
        logger.error("Please check if calibre is installed.")
    # Get content
    words = load_words_fl_to_lst("book_dump_html/index1.html")
    logger.info("Loading book content: {} words".format(len(words)))
    # Using manager not working, threads are locked -> slow.
    # with Manager() as manager:
        # mp_words = manager.list(words)
        # mp_ww_dict = manager.dict(ww_dict)
        # mp_stopwords = manager.list(stopwords)
    logger.info("Begin to look-up wordwise. Number of parallel threads: {}".format(min(mp.cpu_count(), num_t)))
    with Pool(min(mp.cpu_count(), num_t), initializer=init_worker, initargs=(words, ww_dict, stopwords)) as pool:
        # ww_idxwords = pool.starmap(ww_lookup, [(mp_words, mp_ww_dict, ww_dict, mp_stopwords) for word_idx in range(len(words))])
        ww_idxwords = pool.starmap(ww_lookup, [(word_idx,) for word_idx in range(len(words))])
    #
    logger.info("Finish looking up wordwise. Consolidating data from threads")
    ww_idxwords_sorted = sorted(ww_idxwords, key=lambda x: x[0])
    ww_idxwords = list(map(lambda x: x[1], ww_idxwords_sorted))
    #
    logger.info("Creating book with wordwise...")
    ww_book_content = " ".join(ww_idxwords)
    with open("book_dump_html/index1.html", "w", encoding="utf-8") as f:
        f.write(ww_book_content)
    #
    subprocess.run(["tar.exe", "-a",  "-c",  "-f", "book_dump_html.zip",  "book_dump_html"])
    # 
    if args.out_epub:
        logger.info("Creating word-wise EPUB...")
        subprocess.run(["ebook-convert",  "book_dump_html.zip", f"{bookfilename}-wordwised-lvl{hint_level}.epub"], capture_output=True)
    if args.out_azw3:
        logger.info("Creating word-wise AZW3...")
        subprocess.run(["ebook-convert",  "book_dump_html.zip", f"{bookfilename}-wordwised-lvl{hint_level}.azw3"], capture_output=True)
    if args.out_pdf:
        logger.info("Creating word-wise PDF...")
        subprocess.run(["ebook-convert",  "book_dump_html.zip", f"{bookfilename}-wordwised-lvl{hint_level}.pdf"], capture_output=True)
    
    # clean temp
    for p in ["book_dump.htmlz", "book_dump_html", "book_dump_html.zip"]:
        if os.path.isfile(p):
            os.remove(p)
        if os.path.isdir(p):
            shutil.rmtree(p, ignore_errors=True)
    #
    logger.info("Finished. Have fun reading books.")
    logger.info("Credit: https://www.facebook.com/doduc.dnad")