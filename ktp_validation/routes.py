from flask import render_template, url_for, flash, redirect, request
from ktp_validation.forms import RecognitionForm
from ktp_validation import app

from PIL import Image
from datetime import datetime

import os
import shutil
import ktp_validation.functions as functions
import ktp_validation.jpg_to_txt as jpg_to_txt
import ktp_validation.validity_check_ktp as vc_ktp

def find_the_highest_score(type, list, output_directory, name='', dob='', nik='', institution='', degree='', gpa='', english_score=''):

    # Initiate the dictionary result and other parameter
    result = {}
    first = True

    # list = functions.filter_list(list, type)
    
    # Loop through the given list and get the result, validity, and score
    for file in list:
        if type == 'akta':
            result_vc = vc_akta.main(output_directory + file, 'dictionary.json', name, date_of_birth)
        elif type == 'ktp':
            result_vc = vc_ktp.main(output_directory + file, name, dob, nik)
        elif type == 'ijazah':
            result_vc = vc_ijazah.main(output_directory + file, name, institution, degree)
        elif type == 'transkrip':
            result_vc = vc_transkrip.main(output_directory + file, name, gpa)
        elif type == 'toefl':
            result_vc = vc_english_score.main(output_directory + file, name, english_score)

        # Check whether it is a first iteration, if it is so save it to result variable
        try:
            if first:
                result = result_vc
                first = False

            # If it is not the first iteration, we compare it to the highest score
            else:
                for key, value in result_vc.items():
                    if result_vc[key]['score'] > result[key]['score']:
                        result[key] = result_vc[key]
        except:
            return ''

    return result

def save_picture(ktp):
    img = Image.open(ktp)

    current_timestamps = datetime.now().strftime("%d%m%Y-%H%M%S")
    ktp_fn = current_timestamps + '_' + 'ktp.jpg'

    img.save(os.path.join(app.root_path, 'static', 'ktp', ktp_fn))

    return ktp_fn

def clean_folder(folder='ktp_validation/static/ktp/'):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():
    form = RecognitionForm()

    if request.method == 'GET':
        image_file = url_for('static', filename='default.jpg')
        return render_template('home.html', form=form, image_file=image_file, input_data=None)

    elif request.method == 'POST':
        image_file = url_for('static', filename='default.jpg')

        if form.validate_on_submit():
            clean_folder()
            ktp_file = save_picture(form.ktp.data)
            image_file = url_for('static', filename='ktp/'+ktp_file)

            name = request.form['name']
            nik = request.form['nik']
            dob = request.form['dob']

            jpg_to_txt.main('ktp_validation/static/ktp/')

            input_data = {
                'name': name,
                'dob': dob,
                'nik': nik 
            }

            list_of_txt_files = os.listdir('ktp_validation/static/ktp/output/')
            
            ktp = find_the_highest_score('ktp', list_of_txt_files, 'ktp_validation/static/ktp/output/', \
                                        name=name, \
                                        dob=dob, \
                                        nik=nik)

            flash(f'Success', 'success')
            return render_template('home.html', form=form, image_file=image_file, input_data=input_data, recognition=ktp)


        return render_template('home.html', form=form, image_file=image_file, input_data=None)