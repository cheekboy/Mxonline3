import json
import logging
import time
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest

responsestring = ""
# your expected instance type
instance_type = "ecs.xn4.small"
vswitch_id = "vsw-bp13yqlcg81ewswreibb5"
image_id = "centos_7_03_64_20G_alibase_20170818.vhd"
security_group_id = "sg-bp15ylvdo8ouhytt6eqg"
amount = 1;
auto_release_time = "2018-12-05T22:40:00Z"

runtime = 0;

# create instance automatic running
def batch_create_instance():
    request = build_request()
    request.set_Amount(amount)
    _execute_request(request)


# create instance with public ip.
def batch_create_instance_with_public_ip():
    request = build_request()
    request.set_Amount(amount)
    request.set_InternetMaxBandwidthOut(1)
    _execute_request(request)


# create instance with auto release time.
def batch_create_instance_with_auto_release_time():
    request = build_request()
    request.set_Amount(amount)
    request.set_AutoReleaseTime(auto_release_time)
    _execute_request(request)


def _execute_request(request):
    response = _send_request(request)
    if response.get('Code') is None:
        instance_ids = response.get('InstanceIdSets').get('InstanceIdSet')
        running_amount = 0
        while running_amount < amount:
            time.sleep(15)
            running_amount = check_instance_running(instance_ids)
    print("ecs instance %s is running", instance_ids)


def check_instance_running(instance_ids):
    request = DescribeInstancesRequest()
    request.set_InstanceIds(json.dumps(instance_ids))
    response = _send_request(request)
    if response.get('Code') is None:
        instances_list = response.get('Instances').get('Instance')
        running_count = 0
        for instance_detail in instances_list:
            if instance_detail.get('Status') == "Starting":
                running_count += 1
        return running_count


def build_request():
    request = RunInstancesRequest()
    request.set_ImageId(image_id)
    request.set_VSwitchId(vswitch_id)
    request.set_SecurityGroupId(security_group_id)
    request.set_InstanceName("Instance12-04")
    request.set_InstanceType(instance_type)
    return request


# send open api request
def _send_request(request):
    global runtime,responsestring
    request.set_accept_format('json')
    try:
        response_str = clt.do_action(request)
        if runtime > 0:
            responsestring=response_str
            logging.info(response_str)
        runtime+=1
        response_detail = json.loads(response_str)
        return response_detail
    except Exception as e:
        logging.error(e)


def main(ak_id1,ak_secret):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S')
    ak_id = "LTAIGVXfVgRPT6Kc"
    ak_secret = "KRxRClg5iQ5scvHs4cD9l9OBakjXFe"
    region_id = "cn-hangzhou"
    clt = client.AcsClient(ak_id, ak_secret, region_id)
    batch_create_instance()
    # batch_create_instance_with_public_ip()
    # batch_create_instance_with_auto_release_time()