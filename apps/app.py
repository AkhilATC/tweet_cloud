from flask import Flask
from flask import request, jsonify, Blueprint, redirect, send_file, send_from_directory, Response
import yaml
from io import BytesIO
from flask import make_response
from flask_cors import CORS
import apps.custom_exceptions as ce
import apps.data_generation as dg
from apps.twitter_connector import GrabTweets as GT
import io
import base64
import csv

# blueprint
twiity = Blueprint('apps', __name__, template_folder='templates')


def download_file(inputed_data):
    """
    downloading file
 # with open(value, 'rb') as bites:
        #     return send_file(
        #         io.BytesIO(bites.read()),
        #         attachment_filename='logo.png',
        #         mimetype='image/png',
        #         as_attachment=True
        #     )
    """
    print(inputed_data)
    print(type(inputed_data))
    path = dg.generate_excel_file(inputed_data)
    return path


def base64_image_encording(path):

    with open(path, "rb") as img_file:
        mage_string = base64.b64encode(img_file.read())
    return mage_string
    _


@twiity.route('/set_configuration', methods=['POST'])
def set_config():
    """
    index
    return: str
    """

    config_data = request.json
    #print(config_data)
    result = {}
    try:
        consumer_key = config_data.get('consumer_key').strip()
        consumer_secret_key = config_data.get('consumer_secret').strip()
        access_token_key = config_data.get('access_token_key').strip()
        access_token_secret = config_data.get('access_token_secret').strip()
        user_name = config_data.get('user_name').strip()
        if None not in (consumer_key, consumer_secret_key, access_token_key, access_token_secret) and all(
                each is not '' for each in [consumer_key, consumer_secret_key, access_token_key, access_token_secret]):
            with open(r'apps/config/settings.yml') as file_:
                settings_list = yaml.load(file_, Loader=yaml.FullLoader)
            print(settings_list)
            settings_list['twitter_settings']['consumer_key'] = consumer_key
            settings_list['twitter_settings']['consumer_secret'] = consumer_secret_key
            settings_list['twitter_settings']['access_token_key'] = access_token_key
            settings_list['twitter_settings']['access_token_secret'] = access_token_secret
            settings_list['twitter_settings']['user_name'] = user_name
            with open("apps/config/settings.yml", 'w') as yaml_file:
                yaml_file.write(yaml.dump(settings_list, default_flow_style=False))
            result = GT().user_info()
            # name = dict(result).pop('name')

            return jsonify(result),200
        else:

            raise ce.InvalidAuthenticationSettings
    except Exception as e:
        print(e)
        result = {'message': 'Invalid payload formats'}
        return jsonify({'response': result}),400


@twiity.route('/export_home_timeline_tweets', methods=['GET'])
def get_home_timeline_tweetss():
    """
    @params : count,download
    @return : base64 image,
    if download:
        excel
    """
    try:
        count = request.args.get('count')
        flag = True if request.args.get('render') == 'true' else False
        print(type(flag))
        print('export_home_timeline_tweets {}'.format(flag))
        if count:
            value = GT(count=int(count)).get_home_timeline_tweets(flag)
        else:
            value = GT().get_home_timeline_tweets(flag)
        if flag is True:
            return base64_image_encording(value)
        return download_file(value)

    except Exception as e:
        print(e)
        return jsonify({}), 400


@twiity.route('/streamming_tweets', methods=['POST'])
def Streamming():
    """
    @params:track,lang,count
    @return :list of tweet words

    """
    payload = request.json

    try:
        print("streamming_tweets")
        print(payload)
        track = payload.get('track')
        lang = payload.get('lang','en')
        count = request.args.get('count')
        flag = True if request.args.get('render') == 'true' else False
        response = GT(count=int(count)).stremming(track, lang, flag)
        if flag is True:
            return base64_image_encording(response)
        else:
            return download_file(response)
    except Exception as e:
        print(e)
        return jsonify({}), 400


@twiity.route('/search_tweets', methods=['POST'])
def search_for_tweets():
    """

    :return: list of tweet words
    """
    payload = request.json
    try:
        query = payload.get('track')
        geo_code = payload.get('geocode')
        count = request.args.get('count')
        flag = True if request.args.get('render') == 'true' else False
        print(geo_code)

        response = GT(count=int(count)).search(query, flag, geocode=geo_code)

        if flag is True:
            print("flag is true")
            return base64_image_encording(response)
        else:
            return download_file(response)

    except Exception as e:
        print(e)
        return jsonify({}), 400


