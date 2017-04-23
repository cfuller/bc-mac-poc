import os, requests, time, boto3
from requests.auth import HTTPBasicAuth
from flask import Blueprint, request, render_template, flash
from werkzeug.utils import secure_filename
from app import app
from app.main.forms import UploadForm

main = Blueprint('main', __name__, url_prefix='')


@main.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm(request.form)

    if request.method == 'POST' and 'video' in request.files:
        f = request.files['video']
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.root_path, 'static/videos', filename
        ))

        flash("Video file uploaded saved - " + filename, 'success')

        title = form.title.data
        desc = form.description.data
        url = app.root_path + '/static/videos/' + filename

        token = auth()

        flash('Authenticated', 'success')

        headers = {'Authorization': 'Bearer ' + token}

        r = requests.post('https://cms.api.brightcove.com/v1/accounts/' + app.config['VC_ACCOUNT'] + '/videos',
                          json={"name": title, "long_description": desc, "state": "INACTIVE"}, headers=headers)
        json = r.json()

        if r.status_code > 399:
            flash('Error: ' + json['message'], 'danger')
            return render_template('main/upload.html', form=form)
        else:
            vid = json['id']
            flash('Video ' + vid + ' - record created', 'success')

            r = requests.get('https://ingest.api.brightcove.com/v1/accounts/' + app.config['VC_ACCOUNT'] + '/videos/' + vid + '/upload-urls/' + title, headers=headers)
            json = r.json()

            s3 = boto3.resource('s3',
                                aws_access_key_id=json['access_key_id'],
                                aws_secret_access_key=json['secret_access_key'],
                                aws_session_token=json['session_token'])

            s3.Object(json['bucket'], json['object_key']).upload_file(url)

            r = requests.post('https://ingest.api.brightcove.com/v1/accounts/' + app.config['VC_ACCOUNT'] + '/videos/' + vid + '/ingest-requests',
                              json={"master": {"url": json['api_request_url']}}, headers=headers)
            json = r.json()
            flash('Ingest job ' + json['id'] + ' started', 'info')


    return render_template('main/upload.html', form=form)


def auth():
    token_file = os.path.join(app.root_path, 'static/data', 'token.txt')

    if os.path.isfile(token_file):
        file = open(token_file, 'r')
        d = file.read()
        token, ttime = d.split(',')
        now = int(time.time())
        ttime = int(ttime)
        if now < (ttime + 300):
            print ('true')
            return token
        else:
            token = login(token_file)
            return token
    else:
        token = login(token_file)
        return token


def login(token_file):
    data = {'grant_type': 'client_credentials'}
    r = requests.post('https://oauth.brightcove.com/v3/access_token', data,
                      auth=HTTPBasicAuth(app.config['VC_API_ID'], app.config['VC_API_SECRET']))

    json = r.json()
    token = json['access_token']
    file = open(token_file, 'w')
    file.write(token + ',' + str(int(time.time())))
    file.close()
    return token
