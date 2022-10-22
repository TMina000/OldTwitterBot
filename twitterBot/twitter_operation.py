import twitter
import configparser
import datetime
import boto_utils

# iniファイルの読み込み
config_ini = configparser.ConfigParser()
config_ini.read('config.ini', encoding='utf-8')


def post_to_twitter(items):
    """Summary line.
    Twitterへの投稿関数

    Args:
       items: 投稿内容
    Returns: 
        is_successful_posting: 投稿成功時の投稿結果(投稿日時、投稿日時)
    """
    twitter_connector = twitter_authentication()
    is_successful_posting = request_post_on_twitter(twitter_connector, items)
    return is_successful_posting


def twitter_authentication():
    """Summary line.
    Twitterへのコネクト関数

    Args:
       なし
    Returns: 
        twitter_connector: コネクト
    """

    # 取得したキーとアクセストークンを設定
    authentication_information = twitter.OAuth( 
        consumer_key = config_ini["TWITTER"]["API_KEY"],
        consumer_secret = config_ini["TWITTER"]["API_SECREC_KEY"],
        token = config_ini["TWITTER"]["ACCESS_TOKEN"],
        token_secret = config_ini["TWITTER"]["ACCESS_TOKEN_SECREC"]
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
        datetime_now = str(datetime.datetime.now())
        posted_content = items["post"] +"\n" + datetime_now
        
        twitter_connector.statuses.update(status=posted_content)
    except Exception as e:
        print(e)
        print("Twitterへの自動投稿処理終了")

    formatted_datetime = boto_utils.get_current_time_in_specified_format()
    can_updated = [items["created_at"], formatted_datetime]
    
    return can_updated


