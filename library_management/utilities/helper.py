import math
import os
import time
from hashlib import md5

from django.conf import settings
from pydp.algorithms.laplacian import Count

from utilities.s3_utils import upload_to_s3, generate_presigned_url

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


def apply_dp(epsilon, grouped_data, filename):
    read_count = list(grouped_data['read_count'])
    dp_read_count = list()
    for data in read_count:
        x = Count(epsilon)
        count = x.quick_result(list(range(1, data + 1)))
        dp_read_count.append(count)
    grouped_data['dp_read_count'] = dp_read_count
    grouped_data = grouped_data.drop('read_count', 1)
    grouped_data.to_csv(BASE_DIR + f"/data/{filename}")


def create_df_csv(df, condition):
    lookup = {
        1: f'group_by_dept_dp_{int(time.time())}.csv',
        2: f'group_by_study_level_dp_{int(time.time())}.csv',
        3: f'group_by_dept_study_level_dp_{int(time.time())}.csv'
    }
    filename = lookup[int(condition)]
    apply_dp(math.log(3), df, filename)
    upload_to_s3(BASE_DIR + f"/data/{filename}", f"data_share/{filename}", settings.AWS_STORAGE_BUCKET_NAME)
    os.remove(BASE_DIR + f"/data/{filename}")
    url = generate_presigned_url('media/' + f"data_share/{filename}", settings.AWS_STORAGE_BUCKET_NAME)
    return url
