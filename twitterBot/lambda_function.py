import twitter_operation
import dynamodb_operation

def lambda_handler(event, context):
    """Summary line.
    lambda実行時に最初に呼ばれる関数

    Args:
        event: イベント事に渡される投稿対象のTwitter
        context: コンテキスト情報
    Returns: 
        statusCode: 200

    """
    print("Twitterへの自動投稿処理実行")
    items = dynamodb_operation.get_posted_content(event["Twitter"])
    can_updated = twitter_operation.post_to_twitter(items)
    dynamodb_operation.complete_post(event["Twitter"], can_updated)
    print("Twitterへの自動投稿処理終了")
    return {
        'statusCode': 200
    }
