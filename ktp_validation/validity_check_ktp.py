import re
import ktp_validation.functions as functions

from datetime import datetime


# Search the NIK number
def search_nik(numbers, text):

    # Define the pattern to get NIK (we take a string that has the total numbers = numbers we define in the parameter)
    reg_nik = '[0-9]{' + str(numbers) + '}'
    
    # We take the string that matched an return it as a result
    search_nik = re.compile(reg_nik)
    nik = search_nik.findall(text)[0]

    return nik

# Search the date of birth
def search_dob(text):

    # Define the pattern to get dates (20-07-2018, 20 07 2018, 20-07 2018, 20 07-2018)
    reg_dob = '(\d{2}[\/ -]\d{2}[\/ -]\d{2,4})'
    
    # Find all strings that match
    dates = re.findall(reg_dob, text)

    # We iterate through the results and convert it into datetime format
    for i in range(len(dates)):
        date = re.sub('[- ]', '', dates[i])
        dates[i] = datetime.strptime(date, '%d%m%Y')
    
    # We take the smallest dates in a KTP, beacuse it must be his/her birth date
    date = min(dates)

    return datetime.strftime(date, '%d/%m/%Y')


# Main function, there are four main steps here
def main(ktp_path, input_name, input_date_of_birth, input_nik):

    # 1. Read the txt file based on its path
    text = functions.read_txt(ktp_path)

    # 2. Get the date of birth
    try:
        date_of_birth = search_dob(text)
    except:
        date_of_birth = ''

    # 3. Get the NIK number
    try:
        nik = search_nik(17, text)
    except:
        try:
            nik = search_nik(16, text)
        except:
            try:
                nik = search_nik(15, text)
            except:
                nik = ''

    # 4. Check validity of the name, date of birth, and NIK
    name_validity, name_validity_score, name = functions.check_validity('g', 0.6, input_name, text, show_name=True)
    date_of_birth_validity, date_of_birth_validity_score, _ = functions.check_validity('s', 0.9, input_date_of_birth, date_of_birth)
    nik_validity, nik_validity_score, _ = functions.check_validity('s', 0.9, input_nik, nik)

    return {
                'name': {
                    'result': name,
                    'validity': name_validity,
                    'score': name_validity_score
                },

                'dob': {
                    'result': date_of_birth,
                    'validity': date_of_birth_validity,
                    'score': date_of_birth_validity_score
                },

                'nik': {
                    'result': nik,
                    'validity': nik_validity,
                    'score': nik_validity_score
                }
           }