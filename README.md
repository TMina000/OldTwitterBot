# OldTwitterBot
## 説明
AWSを使用したtwitter Botのソースコードです。
このソースコードだけでは、使用できません。

## 使用AWS機能
下記AWSの使用や設定が必要です。
* Lambda
* Amazon EventBridge
* DynamoDB
* CloudWatch
* CodeBuild
* Amazon ECR
* S3
* CodeCommit

## 処理フロー

1.ユーザーがDBにデータを登録する(任意)	

2.ユーザーがcloudwatchlogに時間を設定する(必要があれば)

3.cloudwatchlogがラムダをキックする

4.履歴の投稿フラグの確認、一番古い投稿されてないデータを取得する

4.1.ステータスコード確認

4.1.1.200以外の場合、エラーログを出力して終了	

5.200なら下記、投稿されていないデータの確認	

5.1.投稿されてないデータ存在しない場合

5.1.1.マスターDBから履歴DBにコピー	

5.1.1.1.ステータスコード確認		

5.1.1.1.1.200以外の場合、エラーログを出力して終了	

6.履歴DBの古いものからデータを取得(コピー日確認、投稿フラグ確認)		

6.1.200以外の場合、エラーログを出力して終了			

7.1.ツイッターに投稿					

7.1.1.ステータス確認				

7.1.1.1.200以外の場合、エラーログを出力して終了			

8.履歴DBに投稿日を追加、投稿フラグを立てる			

8.1.ステータス確認				

8.1.1.200以外の場合、エラーログを出力して終了		

9.処理終了					

## テーブル構造

### 投稿テーブル
|論地テーブル名|物理テーブル名|備考|
|--|--|--|
|投稿|XXX_posts|XXXは各Twitterアカウント|

|論理名|物理名|型|備考|
|--|--|--|--|
|投稿内容|post|string(PK)||
|登録日|created_at|string|%Y%m%d%H%M%S%f|

### 履歴投稿テーブル
|論地テーブル名|物理テーブル名|備考|
|--|--|--|
|履歴投稿|XXX_history_posts|XXXは各Twitterアカウント|

|論理名|物理名|型|備考|
|--|--|--|--|
|投稿内容|post|string||
|登録日|created_at|string(PK)|コピーした日 </br>%Y%m%d%H%M%S%f|
|投稿日|registration_at|string|未投稿の場合:null</br>投稿済みの場合:投稿時刻</br>%Y%m%d%H%M%S%f|
|投稿済みフラグ|posted|string|投稿済み:true</br>未投稿:false|

#### グローバルセカンダリインデックス 
|物理名	|主キー	|ソートキー	|備考|
|--|--|--|--|
|posted-created_at-index|	posted	|created_at| |

## 参考資料

### CloudWatchの Eventsの機能

https://support.serverworks.co.jp/hc/ja/articles/360009704354-CloudWatch-Events%E3%82%92%E3%83%88%E3%83%AA%E3%82%AC%E3%83%BC%E3%81%AB%E3%81%97%E3%81%A6%E3%82%B8%E3%83%A7%E3%83%96%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B-SNS%E3%83%88%E3%83%AA%E3%82%AC%E3%83%BC-
	
### Twitter API
https://techacademy.jp/magazine/51411
	
### Docker

https://zenn.dev/kou_pg_0131/articles/lambda-container-image

https://www.blog.danishi.net/2021/02/17/post-4535/




