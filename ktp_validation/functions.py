import re
import json
import os
import base64

from difflib import SequenceMatcher
from datetime import datetime
from urllib.request import urlretrieve


# Read the json file based on its path
def read_json(path):
    with open(path) as file:
        text = json.load(file)
    return text

# Read the txt file based on its path
def read_txt(path):
    try:
        with open(path, 'r') as file:
            text = file.read().lower()
    except:
        with open(path, 'r', encoding='utf8') as file:
            text = file.read().lower()
    return text

# Parse the txt file and put it into list of words
def parse_to_words(text, point_coma=False):
    words = []
    if point_coma == False:
        text = re.sub('[^a-zA-Z0-9]+', ' ', text)
    else:
        text = re.sub('[^a-zA-Z0-9.,]+', ' ', text)
    for word in text.split(' '):
        words.append(word)
    return words

# Filter list value based on specific keyword
def filter_list(list, keyword):
    return [element for element in list if keyword in element]

# Convert the list of words into pair of n-words
def convert_words_into_pair(text, n_words):
    words = []
    new_text = []
    result = []

    # Loop through text and slice it into list of n-words
    for i in range(len(text) - (n_words-1)):
        for j in range(n_words):
            words.append(text[i+j])
        new_text.append(words)
        words = []
    
    # Flatten the list so the list of n-words became a sentence of n-words
    for i in new_text:
        three_words = ' '.join(i)
        result.append(three_words)
    
    return result

# Check the similarity between two strings (range between 0 - 1)
def compute_similarity_score(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Check whether some keywords is in sentences or not (given in a score called g_score)
def compute_g_score(words, text, show_name=False):
    score = 0.0
    name = []
    for word in words:
        if word in text:
            if show_name:
                name.append(word)            
            score += 1
    g_score = score/len(words)
    
    if show_name:
        return g_score, name
    return g_score

# Check validity (is the data from document similar to the user's input)
def check_validity(type, threeshold, input, text, show_name=False, many_values=False):

    status = False
    score = 0.0
    name = []
    value = ''

    # There are two method here, 'g' for g_score and 's' for similarity_score
    # g_score computes the percentages of matches words
    if type == 'g':
        input = parse_to_words(input.lower())
        text = parse_to_words(text.lower())
        if show_name:
            score, name = compute_g_score(input, text, show_name=True)
            name = ' '.join(name)
        else:
            score = compute_g_score(input, text)
        if score >= threeshold:
            status = True
        return status, score, name
    
    # similarity_score computes the similarity between two strings using SequenceMatcher function in python
    elif type == 's':
        if many_values:
            for element in text:
                new_score = compute_similarity_score(input.lower(), element.lower())
                if new_score > score:
                    score = new_score
                    value = element
        else:
            score = compute_similarity_score(input.lower(), text.lower())
        if score >= threeshold:
            status = True
        return status, score, value

# Function to find a starting index based on stop words given
def find_start_index(text, stop_words):
    
    # Iterate through text and save the index of the stop word
    start_index = -1
    found = False

    for stop_word in stop_words:
        for word in text:
            if word == stop_word:
                start_index = text.index(stop_word)
                found = True
                break
        if found:
            break
    
    # If we cannot find the stop words (starting point) we will return none
    if start_index == -1:
        return ''
    
    return start_index

# Function to find a starting index based on the similarity of stop words given
def find_start_index_using_similarity(text, stop_words):
    
    # Iterate through text and save the index of the stop word
    start_index = -1
    similarity = 0
    word = ''

    for stop_word in stop_words:
        for word in text:
            words_similarity = compute_similarity_score(word, stop_word)
            if words_similarity > similarity:
                similarity = words_similarity
                start_index = text.index(word)
                similar_text = stop_word

    return start_index, similar_text

# Compare between words and find the similar word
def find_the_most_similar_word(text, words):

    max_similarity = 0
    similar_word = ''

    for word in words:
        similarity = compute_similarity_score(word, text)
        if similarity > max_similarity:
            max_similarity = similarity
            similar_word = word
    
    return similar_word


# This function will select text based on its start_index and its offset
def select_text(text, start_index, offset, joiner=''):

    # We select text based on the starting index and form a new sentence
    if start_index < 0:
        start_index = 0
    text_selection = text[start_index:start_index + offset]
    text_selection = joiner.join(text_selection)

    return text_selection

# It will return string that match the criteria from the given regex
def filter_based_on_regex(text, pattern, get_all=False):
    filter = re.compile(pattern)
    try:
        if get_all:
            filter_result = filter.findall(text)
        else:
            filter_result = filter.findall(text)[0]
    except:
        filter_result = ''
    
    return filter_result

# Download data
def download_file(download_url, path):
    urlretrieve(download_url, path)

# Create a folder and download applicant's .pdf files
def create_folder_and_download_files(data):

    # Get applicant name and current datetime
    try:
        applicant_name = data['ktp']['name']
    except:
        applicant_name = data['akta']['name']
    
    current_datetime = datetime.now()
    current_datetime = current_datetime.strftime("%Y%m%d-%H%M%S")
    
    # Create folder based on the applicant name and datetime
    applicant_path = 'document/' + current_datetime + '_' + applicant_name
    os.mkdir(applicant_path)
    
    # Download pdf files and save it to a specific path
    try:
        pdf_ktp = base64.b64decode(data['ktp']['pdf_url'])
        pdf_file = open(applicant_path + '/ktp_' + applicant_name + '.pdf','wb')
        pdf_file.write(pdf_ktp)
        pdf_file.close()
    except:
        pdf_akta = base64.b64decode(data['akta']['pdf_url'])
        pdf_file = open(applicant_path + '/akta_' + applicant_name + '.pdf','wb')
        pdf_file.write(pdf_akta)
        pdf_file.close()
    
    pdf_ijazah = base64.b64decode(data['ijazah']['pdf_url'])
    pdf_file = open(applicant_path + '/ijazah_' + applicant_name + '.pdf','wb')
    pdf_file.write(pdf_ijazah)
    pdf_file.close()

    pdf_transkrip = base64.b64decode(data['transkrip']['pdf_url'])
    pdf_file = open(applicant_path + '/transkrip_' + applicant_name + '.pdf','wb')
    pdf_file.write(pdf_transkrip)
    pdf_file.close()
    
    pdf_toefl = base64.b64decode(data['toefl']['pdf_url'])
    pdf_file = open(applicant_path + '/toefl_' + applicant_name + '.pdf','wb')
    pdf_file.write(pdf_toefl)
    pdf_file.close()

    return applicant_path, applicant_name