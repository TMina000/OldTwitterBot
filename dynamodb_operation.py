
import boto3
import boto_utils
from boto3.dynamodb.conditions import Key

# dynamodb操作



def get_posted_content(table_head_name):
    """Summary line.
    Twitterに投稿する内容を取得する関数

    Args:
        table_head_name: table名の先頭につく文字列
    Returns: 
        items: Twitterに投稿する内容
    """
    
    items = get_oldest_unposted_post(table_head_name)
    can_post = check_existence_post(items)

    # 投稿できる内容が無い場合、postsテーブルから取得
    if not can_post:
        items = get_all_from_posts(table_head_name)
        can_post = check_existence_post(items)

        # TODO 微妙
        # postsテーブルからの取得したリストの存在確認 
        
        if not can_post:
            print("postsテーブルに投稿できる内容が存在しません")
            print("Twitterへの自動投稿処理終了")
            raise Exception
        else:
            copy_post(table_head_name, items)

    return items[0]

def get_oldest_unposted_post(table_head_name):
    """Summary line.
    history_postsにある投稿されていない一番古い投稿を取得する関数

    Args:
        table_head_name: table名の先頭につく文字列
    Returns: 
        items: 一番古い投稿
    """

    table = create_table_connect(table_head_name + "_history_posts")
    response = {}
    
    try:
        # 投稿されていない一番古い投稿を1件取得
        response = table.query(
            IndexName="posted-created_at-index",
            KeyConditionExpression=Key('posted').eq('false'),
            Limit=1
        )
        
    except Exception as e:
        print(e)
        print("Twitterへの自動投稿処理終了")

    # status_codeが200以外かを確認
    items = response["Items"]
    
    return items


def check_existence_post(items):
    """Summary line.
    投稿できる投稿内容があるか確認する関数

    Args:
        items: 取得した投稿内容
    Returns: 
        boolean: 投稿できる場合は、True。できない場合は、False
    """

    if not items:
        print("投稿できる投稿内容が存在しません。")

        return False
    return True




def get_all_from_posts(table_head_name):
    """Summary line.
    postsテーブルからすべての投稿を取得する関数

    Args:
        table_head_name:         table_head_name: table名の先頭につく文字列

    Returns: 
        items: すべての投稿内容
    """

    table = create_table_connect(table_head_name + "_posts")
    response = {}
    try:
        response = table.scan()
    except Exception as e:
        print(e)
        print("Twitterへの自動投稿処理終了")

    # status_codeが200以外かを確認
    check_status(response)

    items = response["Items"]

    return items


def copy_post(table_head_name, items):
    """Summary line.
    history_postsテーブルへpostsテーブルから取得したすべての投稿内容を追加する関数

    Args:
        table_head_name: table名の先頭につく文字列        
        items: postsテーブルから取得したすべての投稿内容

    Returns: 
        なし
    """

    table = create_table_connect(table_head_name + "_history_posts")

    for item in items:
        datetime = boto_utils.get_current_time_in_specified_format()
        
        if check_existence_of_kye_of_item(item):
            print("Twitterへの自動投稿処理終了")
            raise Exception
        if check_existence_of_value_of_item(item):
            print("Twitterへの自動投稿処理終了")
            raise Exception

        response = {}
        try:
            response = table.put_item(
                Item={
                    "created_at": datetime,
                    "post": item["post"],
                    "posted": "false",
                    "registration_at": None
                }
            )
        except Exception as e:
            print(e)
            print("Twitterへの自動投稿処理終了")

        # status_codeが200以外かを確認
        check_status(response)




def check_existence_of_kye_of_item(item):
    """Summary line.
    itemのKyeチェック関数

    Args:
        item: 投稿内容
    Returns: 
        False:問題なし True:問題あり
    """

    if not "post" in item:
        print("kyeが存在しません。")
        return True
    
    return False




def check_existence_of_value_of_item(item):
    """Summary line.
    itemのvalueチェック関数

    Args:
        item: 投稿内容
    Returns: 
        False:問題なし True:問題あり
    """
    
    if item["post"] == None:
        print("valueが存在しません。")
        return True

    return False

def complete_post(table_head_name, can_updated):
    """Summary line.
    history_postsテーブルに投稿完了処理をおこなう関数
        postedをtureに更新
        registration_atの日時を更新

    Args:
        table_head_name: table名の先頭につく文字列        
        can_updated: Twitterへの投稿結果

    Returns: 
        なし
    """
    table = create_table_connect(table_head_name + "_history_posts")
    
    # 登録日時
    created_at = can_updated[0]
    # 投稿日時
    registration_at = can_updated[1]
    response = {}

    try:
        response = table.update_item(
            Key= {"created_at": created_at},
            UpdateExpression="set registration_at = :registration_at ,posted = :posted",
            ExpressionAttributeValues= {
                # 更新
                ':registration_at': registration_at,
                ':posted': "true"
            },
            ReturnValues='UPDATED_NEW'
        )

    except Exception as e:
        print(e)
        print("Twitterへの自動投稿処理終了")

    # status_codeが200以外かを確認
    check_status(response)


def create_table_connect(table_name):
    """Summary line.
    指定テーブルのコネクトを作成する関数

    Args:
        table_name: table名
    Returns: 
        table: コネクト
    """

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(table_name)

    return table


def check_status(response):
    """Summary line.
    responseのstatusを確認する関数

    Args:
        response: レスポンス
    Returns: 
        なし
    """
    status_code = response["ResponseMetadata"]["HTTPStatusCode"]
   
    if status_code != 200:
        print("statusCode = %d, response = %s" %( status_code, response)) 
        print("Twitterへの自動投稿処理終了")
        raise Exception      

    


