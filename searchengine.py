"""
File: searchengine.py
---------------------
This program is being used to create a search engine
"""

import os
import sys
import string


def create_index(filenames, index, file_titles):
    """
    This function is passed:
        filenames:      a list of file names (strings)

        index:          a dictionary mapping from terms to file names (i.e., inverted index)
                        (term -> list of file names that contain that term)

        file_titles:    a dictionary mapping from a file names to the title of the article
                        in a given file
                        (file name -> title of article in that file)

    The function will update the index passed in to include the terms in the files
    in the list filenames.  Also, the file_titles dictionary will be updated to
    include files in the list of filenames.

    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title'}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test2.txt'], index, file_titles)
    >>> index
    {'file': ['test2.txt'], '2': ['test2.txt'], 'title': ['test2.txt'], 'ball': ['test2.txt'], 'carrot': ['test2.txt'], 'dog': ['test2.txt']}
    >>> file_titles
    {'test2.txt': 'File 2 Title'}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt', 'test2.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt', 'test2.txt'], '1': ['test1.txt'], 'title': ['test1.txt', 'test2.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt', 'test2.txt'], 'carrot': ['test1.txt', 'test2.txt'], '2': ['test2.txt'], 'dog': ['test2.txt']}
    >>> index = {}
    >>> file_titles = {}
    >>> create_index(['test1.txt', 'test2.txt', 'test2.txt'], index, file_titles)
    >>> index
    {'file': ['test1.txt', 'test2.txt'], '1': ['test1.txt'], 'title': ['test1.txt', 'test2.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt', 'test2.txt'], 'carrot': ['test1.txt', 'test2.txt'], '2': ['test2.txt'], 'dog': ['test2.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title', 'test2.txt': 'File 2 Title'}
    >>> index = {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles = {'test1.txt': 'File 1 Title'}
    >>> create_index([], index, file_titles)
    >>> index
    {'file': ['test1.txt'], '1': ['test1.txt'], 'title': ['test1.txt'], 'apple': ['test1.txt'], 'ball': ['test1.txt'], 'carrot': ['test1.txt']}
    >>> file_titles
    {'test1.txt': 'File 1 Title'}
    """
    # open file from the list
    for file in filenames:
        with open(file) as f:
            title = next(f)[:-1]
            words_in_title = make_list_of_words(title)

            # Add title to files_titles list
            if title not in file_titles:
                file_titles[file] = title

            # Add title words to index list
            for word in words_in_title:
                new_lower_word = clean_word(word)

                if new_lower_word != "":
                    add_term_to_index(index, new_lower_word, file)

            # Add the rest of the words to the index list
            for line in f:
                raw_terms = make_list_of_words(line)
                for word in raw_terms:
                    term = clean_word(word)
                    if term != "":
                        add_term_to_index(index, term, file)


def make_list_of_words(line):
    """for each line of the file,
    this function make a list of each word in said line"""

    line = line.strip()

    raw = line.split()

    return raw


def clean_word(word):
    """
    This function will strip any punctuation or
    other characters return the word, in lowercase
    """
    word = word.strip()

    new_word = word.lower()

    new_word_2 = new_word.strip(string.punctuation)

    return new_word_2


def add_term_to_index(index, term, file):
    """
    This function adds the term and files associated with said term
    to the index
    """
    if term not in index:

        index[term] = []

        index[term].append(file)

    else:

        if file not in index[term]:

            index[term].append(file)


def search(index, query):
    """
    This function is passed:
        index:      a dictionary mapping from terms to file names (inverted index)
                    (term -> list of file names that contain that term)

        query  :    a query (string), where any letters will be lowercase

    The function returns a list of the names of all the files that contain *all* of the
    terms in the query (using the index passed in).

    >>> index = {}
    >>> create_index(['test1.txt', 'test2.txt'], index, {})
    >>> search(index, 'apple')
    ['test1.txt']
    >>> search(index'ball')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'file')
    ['test1.txt', 'test2.txt']
    >>> search(index, '2')
    ['test2.txt']
    >>> search(index, 'carrot')
    ['test1.txt', 'test2.txt']
    >>> search(index, 'dog')
    ['test2.txt']
    >>> search(index, 'nope')
    []
    >>> search(index, 'apple carrot')
    ['test1.txt']
    >>> search(index, 'apple ball file')
    ['test1.txt']
    >>> search(index, 'apple ball nope')
    []
    """
    # Put search into a list
    words = query.split()
    list_of_files = []
    first_term = words[0]

    if len(words) == 1:
        for word in words:
            if word in index:
                list_of_files += index[word]

    if len(words) > 1:
        if first_term in index:
            list_of_files += index[first_term]

        # Get the next term
        for i in range(len(words) - 1):
            next_term = words[i + 1]

            # Return empty list if term not in index
            if next_term not in index:
                for j in range(len(list_of_files)):
                    list_of_files.pop()

            else:
                list2 = index[next_term]

                # Find all the common files between all words in query
                list_of_files = find_intersection(list_of_files, list2)

    return list_of_files


def find_intersection(list1, list2):
    """
    This function is passed two lists and returns a new list containing
    'intersection' of the two elements.
    """
    intersection = []

    for elem in list1:
        for i in range(len(list2)):
            elem_2 = list2[i]

            if elem == elem_2:
                if elem not in intersection:
                    intersection.append(elem)

    return intersection


##### YOU SHOULD NOT NEED TO MODIFY ANY CODE BELOW THIS LINE (UNLESS YOU'RE ADDING EXTENSIONS) #####


def do_searches(index, file_titles):
    """
    This function is given an inverted index and a dictionary mapping from
    file names to the titles of articles in those files.  It allows the user
    to run searches against the data in that index.
    """
    while True:
        query = input("Query (empty query to stop): ")
        query = query.lower()  # convert query to lowercase
        if query == '':
            break
        results = search(index, query)

        # display query results
        print(f"Results for query '{query}':")
        if results:  # check for non-empty results list
            for i in range(len(results)):
                title = file_titles[results[i]]
                print(f"{i + 1}.  Title: {title},  File: {results[i]}")
        else:
            print("No results match that query.")


def textfiles_in_dir(directory):
    """
    DO NOT MODIFY
    Given the name of a valid directory, returns a list of the .txt
    file names within it.

    Input:
        directory (string): name of directory
    Returns:
        list of (string) names of .txt files in directory
    """
    filenames = []

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filenames.append(os.path.join(directory, filename))

    return filenames


def main():
    """
    Usage: searchengine.py <file directory> -s
    The first argument specified should be the directory of text files that
    will be indexed/searched.  If the parameter -s is provided, then the
    user can interactively search (using the index).  Otherwise (if -s is
    not included), the index and the dictionary mapping file names to article
    titles are just printed on the console.
    """
    # Get command line arguments
    args = sys.argv[1:]

    num_args = len(args)
    if num_args < 1 or num_args > 2:
        print('Please specify directory of files to index as first argument.')
        print('Add -s to also search (otherwise, index and file titles will just be printed).')
    else:
        # args[0] should be the folder containing all the files to index/search.
        directory = args[0]
        if os.path.exists(directory):
            # Build index from files in the given directory
            files = textfiles_in_dir(directory)
            index = {}  # index is empty to start
            file_titles = {}  # mapping of file names to article titles is empty to start
            create_index(files, index, file_titles)

            # Either allow the user to search using the index, or just print the index
            if num_args == 2 and args[1] == '-s':
                do_searches(index, file_titles)
            else:
                print('Index:')
                print(index)
                print('File names -> document titles:')
                print(file_titles)
        else:
            print(f'Directory {directory} does not exist.')


if __name__ == '__main__':
    main()
