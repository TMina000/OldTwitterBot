import datetime

def get_current_time_in_specified_format():
    """Summary line.
    現在時刻を指定のフォーマットで取得する関数

    Args:
        なし
    Returns: 
        formatted_datetime: 現在時刻
    """

    datetime_now = datetime.datetime.now()
    formatted_datetime = str(datetime_now.strftime('%Y%m%d%H%M%S%f'))

    return formatted_datetime