import os
import time
from hashlib import md5

import pandas as pd
from pydp.algorithms.laplacian import Count

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


def create_response_dict(data, message, success=True, page=None, **kwargs):
    response_dict = dict()
    if success:
        response_dict["data"] = data
    if page:
        response_dict['page'] = page
    response_dict["message"] = message
    response_dict["success"] = success
    response_dict.update(kwargs)
    return response_dict


def create_db_id():
    return md5(f"{time.time()}".encode('utf-8')).hexdigest()


def test_dp(epsilon):
    try:
        grouped_data = pd.read_csv(BASE_DIR + "/data/group_by_dept.csv")
        read_count = list(grouped_data['read_count'])
        dp_read_count = list()

        for data in read_count:
            x = Count(epsilon)
            count = x.quick_result(list(range(1, data + 1)))
            dp_read_count.append(count)
        grouped_data['dp_read_count'] = dp_read_count
        grouped_data.to_csv(BASE_DIR + "/data/group_by_dept_dp.csv")
    except Exception as e:
        print(e)
