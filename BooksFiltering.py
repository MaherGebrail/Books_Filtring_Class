#!/usr/bin/env python3
import pandas as pd
from collections import Counter
import os


class BooksData:
    """
    BooksData Class used to filter the books in Books dir path
    Actually the Class doesn't do a lot as  much as it's a flexible way to have more functions together.
    """
    def __init__(self, path=None, data=False, BooksMethods=False):
        """

        :param path: to write the path of Books dir
        :param data: it's used to take in frames to work with, with the class methods
        :param BooksMethods: the default is false (To bring you back the Table) --> if it's Turned To True ,
            it'll will not bring you the data ,, but it'll handle it for another later methods
        """
        self.path = path
        self.data = data
        self.BooksMethods = BooksMethods

    @staticmethod
    def read_words_list(txt_):
        with open(txt_, 'r') as file:
            text = file.read().lower().strip()
            text = text.replace("\n", " ").replace("\r", " ").split(" ")
            skips = [',', '.', "''", ':', "'", '"', '']
            for i in skips:
                if i in text:
                    text.remove(i)

        return text

    @staticmethod
    def countWords(text):
        counted = Counter(text)
        keys = 0
        value = 0
        for key, val in counted.items():
            keys += 1
            value += val

        return keys, value

    def return_(self, methods):
        if methods:
            return BooksData(path=self.path, data=self.data, BooksMethods=methods)
        else:
            return self.data

    def makeSheet(self, methods=False):

        sheet = pd.DataFrame(columns=['Language', "Author", "Book", "UniqeWords", "countedWords"])
        num = 1
        for language in os.listdir(self.path):
            if os.path.isdir(f"{self.path}/{language}"):
                for author in os.listdir(f"{self.path}/{language}"):
                    if os.path.isdir(f"{self.path}/{language}/{author}"):
                        for book in os.listdir(f"{self.path}/{language}/{author}"):
                            got_book_words = self.read_words_list(f"{self.path}/{language}/{author}/{book}")
                            uniqueWords, values = self.countWords(got_book_words)
                            sheet.loc[num] = language, author, book, uniqueWords, values
                            num += 1
                    elif os.path.isfile(f"{self.path}/{language}/{author}"):
                        got_book_words = self.read_words_list(f"{self.path}/{language}/{author}")
                        uniqueWords, values = self.countWords(got_book_words)
                        sheet.loc[num] = language, "UnKnown author", author, uniqueWords, values
                        num += 1
        self.data = sheet
        return self.return_(methods)

    def getOddrows(self, methods=False):
        list_boolen = []
        num = 0
        for _ in self.data.iterrows():
            if num % 2:
                num += 1
                list_boolen.append(False)
            else:
                list_boolen.append(True)
                num += 1
        cols = [i for i in self.data.columns]
        oddDataFrame = pd.DataFrame(columns=cols)

        n = 1
        for i in range(len(list_boolen)):
            if list_boolen[i]:
                oddDataFrame.loc[n] = self.data.iloc[i]
                n += 1

        self.data = oddDataFrame
        return self.return_(methods)

    def __repr__(self):
        return repr(self.data)


path_ = './Books'
fullTable = BooksData(path=path_).makeSheet()
# oddRows = BooksData(data=fullTable).getOddrows()
#   or
oddRows = BooksData(path=path_).makeSheet(True).getOddrows()
print(fullTable)
print(oddRows)

chevalier = (fullTable[fullTable['Author'] == 'chevalier'])

print(fullTable.head(10))

print("\n\nrow 5 :\n", fullTable.loc[5])
print("\n\nknown book for unknown authors : \n", fullTable.loc[fullTable['Author'] == 'UnKnown author'])
print("\n\nfirst 3 rows written by chevalier :\n", chevalier)
print("\n\nrows with shakespeare as author, and has unique words > 30000 :\n",
      fullTable[(fullTable.Author == 'shakespeare') & (fullTable.countedWords > 30000)])
