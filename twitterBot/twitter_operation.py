import twitter
import configparser
import datetime
import boto_utils

# iniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')


def post_to_twitter(twitter_account_name, items):
    """Summary line.
    Twitterへの投稿関数

    Args:
       items: 投稿内容
    Returns: 
        is_successful_posting: 投稿成功時の投稿結果(投稿日時、投稿日時)
    """
    config_ini_name = convert_lowercase_letters_to_uppercase(twitter_account_name)
    twitter_connector = twitter_authentication(config_ini_name)
    is_successful_posting = request_post_on_twitter(twitter_connector, items)
    return is_successful_posting


def convert_lowercase_letters_to_uppercase(twitter_account_name):
    """Summary line.
    小文字を大文字に変換する
        config.iniファイルを参照する為の準備
    Args:
       twitter_account_name: Twitterのアカウント名
    Returns: 
        config_ini_name: config.iniファイル参照用の文字列
    """
    config_ini_name = twitter_account_name.upper() 

    return config_ini_name


def twitter_authentication(config_ini_name):
    """Summary line.
    Twitterへのコネクト関数

    Args:
       なし
    Returns: 
        twitter_connector: コネクト
    """

    # 取得したキーとアクセストークンを設定
    authentication_information = twitter.OAuth( 
        consumer_key = config_ini[config_ini_name]["API_KEY"],
        consumer_secret = config_ini[config_ini_name]["API_SECREC_KEY"],
        token = config_ini[config_ini_name]["ACCESS_TOKEN"],
        token_secret = config_ini[config_ini_name]["ACCESS_TOKEN_SECREC"]
    )

    twitter_connector = None
    try:
        twitter_connector = twitter.Twitter(auth=authentication_information)
    except Exception as e:
        print(e)
        print("Twitterへの自動投稿処理終了")

    return twitter_connector


def request_post_on_twitter(twitter_connector, items):
    """Summary line.
    Twitterへ投稿リクエスト関数

    Args:
       twitter_connector: コネクト
       items: 投稿内容
    Returns: 
        can_updated: 投稿結果(投稿日時、投稿日時)
    """

    # twitterへメッセージを投稿
    try:
        # 重複投稿禁止対策
        #datetime_now = str(datetime.datetime.now())
        posted_content = items["post"]
        print(posted_content)
        #posted_content = items["post"] +"\n" + datetime_now
        posted_content="test"
        twitter_connector.statuses.update(status=posted_content)
    except Exception as e:
        print(e)
        print("Twitterへの自動投稿処理終了")

    formatted_datetime = boto_utils.get_current_time_in_specified_format()
    can_updated = [items["created_at"], formatted_datetime]
    
    return can_updated

