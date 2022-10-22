import unittest
import boto3
from dynamodb_operation import create_table_connect
from dynamodb_operation import get_oldest_unposted_post
from dynamodb_operation import check_existence_post
from dynamodb_operation import check_status
from dynamodb_operation import copy_post
from dynamodb_operation import complete_post
from dynamodb_operation import get_all_from_posts
from dynamodb_operation import get_posted_content
from dynamodb_operation import check_existence_of_kye_of_item
from dynamodb_operation import check_existence_of_value_of_item
from boto3.dynamodb.conditions import Key

"""Summary line.
unit test参考サイト:
https://qiita.com/aomidro/items/3e3449fde924893f18ca

・テスト実行
twitter-bot> python -m coverage run -m unittest discover tests

・カバレッジレポート出力
twitter-bot> python -m coverage report

・カバレッジレポートHTML出力
twitter-bot> python -m coverage html
"""

HOSTORY_POSTS_TABLE = "DynamoDB名"
POSTS_TABLE = "DynamoDB名"

def expected_history_posts_table():

    expected_dynamodb = boto3.resource("dynamodb")
    expected_table = expected_dynamodb.Table(HOSTORY_POSTS_TABLE)
    return expected_table


def expected_posts_table():

    expected_dynamodb = boto3.resource("dynamodb")
    expected_table = expected_dynamodb.Table(POSTS_TABLE)
    return expected_table    

def dummy_post_query_search_kye_created_at(table, created_at):   
    try:
        response = table.query(
            KeyConditionExpression=Key('created_at').eq(created_at)
        )
    except Exception as e:
        print(e) 
    
    return response['Items']


def dummy_post_scan(table):   
    try:
        response = table.scan()    
    except Exception as e:
        print(e) 
    
    return response['Items']


def dummy_put_post(table, dummy_item):

    try:
        table.put_item(Item=dummy_item)
    except Exception as e:
        print(e)    

def dummy_update_post(table, created_at, registration_at, posted):
    try:
        response = table.update_item(
            Key= {"created_at": created_at},
            UpdateExpression="set registration_at = :registration_at ,posted = :posted",
            ExpressionAttributeValues= {
                # 更新
                ':registration_at': registration_at,
                ':posted': posted
            },
            ReturnValues='UPDATED_NEW'
        )

    except Exception as e:
        print(e)


def dummy_delete_post(table, created_at):
    try:
        table.delete_item(
            Key={
                "created_at": created_at
            }
           )
    except Exception as e:
        print(e)    


class CreateTableConnect(unittest.TestCase):


    # テスト実行前の処理
    def setUp(self):
        print("Test Method: test_create_table_connect Test Case: SUCCESS")
 
    # テスト実行後の処理
    def tearDown(self):
        pass

    def test_create_table_connect(self):
        """Summary line.
        create_table_connect関数の試験
        """
        expected = expected_history_posts_table()
        actual = create_table_connect(HOSTORY_POSTS_TABLE)
        self.assertEqual(expected, actual)

class GetOldestUnpostedPost(unittest.TestCase):
    POSTED_FALSE_PRIMARY_KYE = "20000213124650208274"
    POSTED_TRUE_PRIMARY_KYE = "19990213124650208274"
    table = expected_history_posts_table()

    DUMMY_POSTED_FALSE_ITEM={
        "created_at": POSTED_FALSE_PRIMARY_KYE,
        "registration_at":"null",
        "post": "テストデータfalse",
        "posted":"false"
    }

    DUMMY_POSTED_TRUE_ITEM={
        "created_at": POSTED_TRUE_PRIMARY_KYE,
        "registration_at":"null",
        "post": "テストデータtrue",
        "posted":"true"
    }

    # テスト実行前の処理
    def setUp(self):
        dummy_put_post(self.table, self.DUMMY_POSTED_FALSE_ITEM)
      
    # テスト実行後の処理
    def tearDown(self):
        dummy_delete_post(self.table, self.POSTED_FALSE_PRIMARY_KYE)
  
        
    
    def test_pattern_posted_false_get_oldest_unposted_post(self):
        """Summary line.
        get_oldest_unposted_post関数の試験
            一番古い日付のpostedがfalseのデータが取得される事
        """
        print("Test Method: get_oldest_unposted_post Test Pattern: posted(false) Test Case: SUCCESS")
  
        expected=[self.DUMMY_POSTED_FALSE_ITEM]
        actual = get_oldest_unposted_post("KameiRyosuke")

        self.assertEqual(expected, actual)


    def test_pattern_posted_true_get_oldest_unposted_post(self):
        """Summary line.
        get_oldest_unposted_post関数の試験
            一番古い日付のpostedがtrue
            次に古い日付のpostedがfalseの時に「次に古い日付」のデータが取得される事           
        """
        print("Test Method: get_oldest_unposted_post Test Pattern: posted(false) Test Explanation:posted(true)に古いもが存在する Test Case: SUCCESS")
        # 前準備
        dummy_put_post(self.table, self.DUMMY_POSTED_TRUE_ITEM)

        not_expected=[self.DUMMY_POSTED_TRUE_ITEM]
        actual = get_oldest_unposted_post("KameiRyosuke")

        self.assertNotEqual(not_expected, actual)
        
        # 後処理
        dummy_delete_post(self.table, self.POSTED_TRUE_PRIMARY_KYE)


class GetAllFromPosts(unittest.TestCase):
        
    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass

    def test_pattern_table_head_name_not_exist_get_all_from_posts(self):
        """Summary line.
        get_all_from_posts関数の試験
            引数のtable_head_nameが存在しないテーブルの時
        """
        print("Test Method: get_all_from_posts Test Explanation: 引数のtable_head_nameが存在しないテーブルの時 Test Case: FAILED")
        
        table_head_name = "test"
        items = [{"post":"テスト"}]
        with self.assertRaises(Exception):
            get_all_from_posts(table_head_name, items)

class CheckExistencePost(unittest.TestCase):
        
    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass

    def test_pattern_argument_none_check_existence_post(self):
        """Summary line.
        check_existence_post関数の試験
            引数がNoneの時にFalseが取得される事
        """
        print("Test Method: check_existence_post Test Pattern: argument(None) Test Case: SUCCESS")
        actual = check_existence_post(None)

        self.assertEqual(False, actual)


    def test_pattern_argument_not_none_check_existence_post(self):
        """Summary line.
        check_existence_pos関数の試験
            引数がnot Noneの時にTrueが取得される事
        """
        print("Test Method: check_existence_post Test Pattern: argument(not None) Test Case: SUCCESS")
        actual = check_existence_post("test")

        self.assertEqual(True, actual)


class CheckStatus(unittest.TestCase):
            
    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass

    def test_pattern_status_200_check_status(self):
        """Summary line.
        check_status関数の試験
            引数のresponseのstatus codeが200の時
        """
        print("Test Method: check_status Test Explanation: ステータスコードが200の場合 Test Case: SUCCESS")
        
        http_status_code = {"HTTPStatusCode":200}
        response_metadata = {"ResponseMetadata":http_status_code}

        actual = check_status(response_metadata)

        self.assertEqual(None, actual)


    def test_pattern_status_not_200_check_status(self):
        """Summary line.
        check_status関数の試験
            引数がnot Noneの時にTrueが取得される事
        """
        print("Test Method: check_status Test Explanation: ステータスコードが200以外の場合 Test Case: FAILED")
        http_status_code = {"HTTPStatusCode":300}
        response_metadata = {"ResponseMetadata":http_status_code}

        with self.assertRaises(Exception):
            check_status(response_metadata)

class CheckExistenceOfKyeOfItem(unittest.TestCase):
    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass
    
    def test_argument_none_kye_check_existence_of_kye_of_item(self):
        """Summary line.
        check_existence_of_kye_of_item関数の試験
            引数がitemのkyeが存在しない時にTrueが取得される事
        """
        print("Test Method: check_existence_of_kye_of_item Test Pattern: argument(kye none) Test Case: SUCCESS")
        item = {"post_dummy":"テスト"}
        actual = check_existence_of_kye_of_item(item)

        self.assertEqual(True, actual)

    def test_argument_existence_kye_check_existence_of_kye_of_item(self):
        """Summary line.
        check_existence_of_kye_of_item関数の試験
            引数がitemのkyeが存在する時にFalseが取得される事
        """
        print("Test Method: check_existence_of_kye_of_item Test Pattern: argument(kye existence) Test Case: SUCCESS")
        item = {"post":"テスト"}
        actual = check_existence_of_kye_of_item(item)

        self.assertEqual(False, actual)


class CheckExistenceOfValueOfItem(unittest.TestCase):
    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass

    def test_argument_none_value_check_existence_of_value_of_item(self):
        """Summary line.
        check_existence_of_value_of_item関数の試験
            引数がitemのvalueが存在しない時にTrueが取得される事
        """
        print("Test Method: check_existence_of_value_of_item Test Pattern: argument(value none) Test Case: SUCCESS")

        item = {"post": None}
        actual = check_existence_of_value_of_item(item)
        print(actual)
        self.assertEqual(True, actual)

    def test_argument_existence_kye_check_existence_of_value_of_item(self):
        """Summary line.
        check_existence_of_value_of_item関数の試験
            引数がitemのvalueが存在する時にFalseが取得される事
        """
        print("Test Method: check_existence_of_value_of_item Test Pattern: argument(value existence) Test Case: SUCCESS")
        item = {"post": "テスト"}
        actual = check_existence_of_value_of_item(item)

        self.assertEqual(False, actual)

class CopyPost(unittest.TestCase):
            
    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass

    def test_pattern_table_head_name_not_exist_copy_post(self):
        """Summary line.
        copy_post関数の試験
            引数のtable_head_nameが存在しないテーブルの時
        """
        print("Test Method: copy_post Test Explanation: 引数のtable_head_nameが存在しないテーブルの時 Test Case: FAILED")
        
        table_head_name = "test"
        items = [{"post":"テスト"}]
        with self.assertRaises(Exception):
            copy_post(table_head_name, items)


    def test_pattern_item_kye_not_exist_copy_post(self):
        """Summary line.
        copy_post関数の試験
            引数のitemのKyeが存在しない時
        """
        print("Test Method: copy_post Test Explanation: 引数のitemのkyeが存在しない時 Test Case: FAILED")
        
        table_head_name = "KameiRyosuke"
        items = [{"post_dummy":"テスト"}]
        with self.assertRaises(Exception):
            copy_post(table_head_name, items)


    def test_pattern_item_value_not_exist_copy_post(self):
        """Summary line.
        copy_post関数の試験
            引数のitemのvalueが存在しない時
        """
        print("Test Method: copy_post Test Explanation: 引数のitemのvalueが存在しない時 Test Case: FAILED")
        table_head_name = "KameiRyosuke"
        items = [{"post":None}]
        with self.assertRaises(Exception):
            copy_post(table_head_name, items)


class CompletePost(unittest.TestCase):
    CREATED_AT = "20000213124650208278"
    REGISTRATION_AT = "20001213124650208274"
    table = expected_history_posts_table()
    post_contents = "テストデータ"
    DUMMY_POSTED_ITEM={
        "created_at": CREATED_AT,
        "registration_at":"null",
        "post": post_contents,
        "posted":"false"
    }
    
    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass
    
    def test_pattern_table_head_name_not_exist_complete_post(self):
        """Summary line.
        complete_post関数の試験
            引数のtable_head_nameが存在しないテーブルの時
        """
        print("Test Method: complete_post Test Explanation: 引数のtable_head_nameが存在しないテーブルの時 Test Case: FAILED")
        #can_updated
        table_head_name = "test"
        can_updated = [self.CREATED_AT, self.REGISTRATION_AT]
        with self.assertRaises(Exception):
            complete_post(table_head_name, can_updated)


    def test_pattern_can_updated_index_0_not_exist_complete_post(self):
        """Summary line.
        complete_post関数の試験
            引数のcan_updatedのindex0が存在しない時
        """
        print("Test Method: complete_post Test Explanation:  引数のcan_updatedのindex0が存在しない時 Test Case: FAILED")
        
        table_head_name = "KameiRyosuke"
        can_updated = [None, self.REGISTRATION_AT]
        with self.assertRaises(Exception):
            complete_post(table_head_name, can_updated)


    def test_pattern_can_updated_index_1_not_exist_complete_post(self):
        """Summary line.
        complete_post関数の試験
            引数のcan_updatedのindex1が存在しない時
        """
        print("Test Method: complete_post Test Explanation: 引数のcan_updatedのindex1が存在しない時 Test Case: FAILED")
        table_head_name = "KameiRyosuke"
        can_updated = [self.CREATED_AT]
        with self.assertRaises(Exception):
            complete_post(table_head_name, can_updated)


    def test_complete_post(self):
        """Summary line.
        complete_post関数の試験
            引数が正常に存在する時
        """
        print("Test Method: complete_post Test Case: SUCCESS")
        table_head_name = "KameiRyosuke"
        can_updated = [self.CREATED_AT, self.REGISTRATION_AT]
 
         # 前準備
        dummy_put_post(self.table, self.DUMMY_POSTED_ITEM)

        complete_post(table_head_name, can_updated)

        # update内容確認
        actual = dummy_post_query_search_kye_created_at(self.table, self.CREATED_AT)
        
        self.assertEqual(self.CREATED_AT, actual[0]["created_at"])
        self.assertEqual(self.REGISTRATION_AT, actual[0]["registration_at"])
        self.assertEqual(self.post_contents, actual[0]["post"])
        self.assertEqual("true", actual[0]["posted"])
        
        # ダミーデータ削除
        dummy_delete_post(self.table, self.CREATED_AT)


class GetPostedContent(unittest.TestCase):
    REGISTRATION_AT = "20010213124650208274"
    HISTORY_POSTED_PRIMARY_KYE = "20000213124650208274"
    HISTORY_REGISTRATION_AT = "20001213124650208274"
    POSTED_PRIMARY_KYE = "19900213124650208274"
    table_history_posts = expected_history_posts_table()
    table_posts = expected_posts_table()

    DUMMY_HISTORY_POSTED_ITEM={
        "created_at":  HISTORY_POSTED_PRIMARY_KYE,
        "registration_at":"null",
        "post": "テストデータfalse",
        "posted":"false"
    }

    DUMMY_POSTED_ITEM={
        "created_at": POSTED_PRIMARY_KYE,
        "post": "テストデータ"
    }

    # テスト実行前の処理
    def setUp(self):
        pass
      
    # テスト実行後の処理
    def tearDown(self):
        pass


    def test_get_posted_content(self):
        """Summary line.
        test_get_posted_content関数の試験
            投稿履歴テーブルに投稿可能レコードがあった場合、1レコード取得される
        """
        print("Test Method: get_posted_content Test Case: SUCCESS")
        # 一番古い投稿可能なレコードを挿入
        dummy_put_post(self.table_history_posts, self.DUMMY_HISTORY_POSTED_ITEM)
        table_head_name = "KameiRyosuke"

        actual = None
        actual = get_posted_content(table_head_name)
        self.assertEqual(self.DUMMY_HISTORY_POSTED_ITEM["created_at"], actual["created_at"])
        self.assertEqual(self.DUMMY_HISTORY_POSTED_ITEM["registration_at"], actual["registration_at"])
        self.assertEqual(self.DUMMY_HISTORY_POSTED_ITEM["post"], actual["post"])
        self.assertEqual(self.DUMMY_HISTORY_POSTED_ITEM["posted"], actual["posted"])
        
        # 一番古い投稿可能なレコードを削除     
        dummy_delete_post(self.table_history_posts, self.POSTED_PRIMARY_KYE)


    def test_get_posted_content_can_post_false(self):
        """Summary line.
        test_get_posted_content関数の試験
            投稿履歴テーブルに投稿可能レコードがない場合、
            投稿テーブルよりレコードをcopyし投稿可能な状態にし
            1レコード取得される
        """
        print("Test Method: test_get_posted_content_can_post_false Test Explanation: 投稿履歴テーブルに投稿可能レコードがない場合、投稿テーブルよりレコードをcopyし投稿可能な状態。 Test Case: SUCCESS")
        
        # テスト終了後元に戻す
        save_history_items = dummy_post_scan(self.table_history_posts)
        save_items = dummy_post_scan(self.table_posts)

        for item in save_history_items: 
            if item["posted"] == "false":
                dummy_update_post(self.table_history_posts, item["created_at"], self.REGISTRATION_AT, "true")
        
        dummy_put_post(self.table_posts, self.DUMMY_POSTED_ITEM)

        table_head_name = "KameiRyosuke"
        actual = get_posted_content(table_head_name)
        self.assertEqual(self.DUMMY_POSTED_ITEM["created_at"], actual["created_at"])
        self.assertEqual(self.DUMMY_POSTED_ITEM["post"], actual["post"])

        delete_history_items = dummy_post_scan(self.table_history_posts)
        for item in delete_history_items:
            dummy_delete_post(self.table_history_posts, item["created_at"])

        delete_items = dummy_post_scan(self.table_posts)
        for item in delete_items:
            dummy_delete_post(self.table_posts, item["created_at"])

        for item in save_history_items:
            dummy_put_post(self.table_history_posts, item)

        for item in save_items:
            dummy_put_post(self.table_posts, item)


    def test_get_posted_content_can_post_not(self):
        """Summary line.
        test_get_posted_content関数の試験
            投稿履歴テーブルに投稿可能レコードがない場合、
            投稿テーブルにレコードが存在しない場合。
        """
        print("Test Method: test_get_posted_content_can_post_not Test Explanation: 投稿履歴テーブルに投稿可能レコードがない場合、投稿テーブルにレコードが存在しない場合。 Test Case: FAILED")
        
        # テスト終了後元に戻す
        save_history_items = dummy_post_scan(self.table_history_posts)
        save_items = dummy_post_scan(self.table_posts)

        for item in save_history_items: 
            if item["posted"] == "false":
                dummy_update_post(self.table_history_posts, item["created_at"], self.REGISTRATION_AT, "true")
        
        dummy_put_post(self.table_posts, self.DUMMY_POSTED_ITEM)

        delete_items = dummy_post_scan(self.table_posts)
        for item in delete_items:
            dummy_delete_post(self.table_posts, item["created_at"])

        table_head_name = "KameiRyosuke"

        with self.assertRaises(Exception):
            get_posted_content(table_head_name)

        delete_history_items = dummy_post_scan(self.table_history_posts)
        for item in delete_history_items:
            dummy_delete_post(self.table_history_posts, item["created_at"])

        for item in save_history_items:
            dummy_put_post(self.table_history_posts, item)

        for item in save_items:
            dummy_put_post(self.table_posts, item)


if __name__ == '__main__':
    unittest.main()
