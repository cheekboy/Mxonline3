# encoding: utf-8
from courses.models import Course, Video, Lesson, CourseResource

__author__ = 'jiangming'
__date__ = '2018/8/29 0009 08:02'
import xadmin
from django.contrib.auth.models import Group, Permission
from users.models import *
import os,json,re
import subprocess

from operation.models import CourseComments, UserFavorite, UserMessage, UserCourse, UserAsk
from organization.models import CityDict, Teacher, CourseOrg
from xadmin.models import Log

# 和X admin的view绑定
from xadmin import views

from .models import EmailVerifyRecord, Banner, UserProfile

from django.http import HttpResponse
from xadmin.plugins.actions import BaseActionView




class MyActionCeateEcs(BaseActionView):
    # 这里需要填写三个属性
    action_name = "创建ecs服务器"    #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'创建服务器%(verbose_name_plural)s'
    model_perm = 'change'

    def do_action(self, queryset):
        for obj in queryset:
            alikey = AliKey.objects.get(id=1)
            #response= regecs.main(alikey.ak_id, alikey.ak_secret)
            s = """
cat <<EOF > ~/test.py
import json
import logging
import time
from aliyunsdkcore import client
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526.RunInstancesRequest import RunInstancesRequest
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
ak_id = "LTAIGVXfVgRPT6Kc"
ak_secret = "KRxRClg5iQ5scvHs4cD9l9OBakjXFe"
region_id = "cn-hangzhou"
# your expected instance type
instance_type = "ecs.xn4.small"
vswitch_id = "vsw-bp13yqlcg81ewswreibb5"
image_id = "centos_7_03_64_20G_alibase_20170818.vhd"
security_group_id = "sg-bp15ylvdo8ouhytt6eqg"
amount = 1;
auto_release_time = "2018-12-05T22:40:00Z"
clt = client.AcsClient(ak_id, ak_secret, region_id)
runtime=0;


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
    #print("ecs instance %s is running", instance_ids)


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
    global runtime
    request.set_accept_format('json')
    try:
        response_str = clt.do_action(request)
        if runtime > 0:
            logging.info(response_str)
            print(response_str)
        runtime+=1
        response_detail = json.loads(response_str)
        return response_detail
    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    batch_create_instance()
    # batch_create_instance_with_public_ip()
    # batch_create_instance_with_auto_release_time()
EOF

python3 ~/test.py
            """
            regex = re.compile(r'\\(?![/u"])')

            str = os.popen(s).read().replace("b'","").replace("'","")
            str = regex.sub(r"\\\\", str)
            return1=json.loads(str)
            obj.ip=return1['Instances']['Instance'][0]["NetworkInterfaces"]['NetworkInterface'][0]['PrimaryIpAddress']
            #其实我们做的只有这一部分 ********
            #obj.images += 'sss'
            obj.save()
        return HttpResponse('{0}'.format(str), content_type='application/json')




class MyAction(BaseActionView):
    # 这里需要填写三个属性
    action_name = "change_sss"    #: 相当于这个 Action 的唯一标示, 尽量用比较针对性的名字
    description = u'Test selected %(verbose_name_plural)s'
    model_perm = 'change'

    def do_action(self, queryset):
        for obj in queryset:
            envarray=obj.env.split(",")
            senv = """          - name: {0}
            value: \"{1}\"
"""
            senvall=""
            for item in envarray:
                itemarray = item.split("=")
                senvall=senvall+senv.format(itemarray[0],itemarray[1])
            s ="""
cat <<EOF > ~/test.txt
---
apiVersion: extensions/v1beta1
kind: Deployment
metadata:
    name: red-nginx{0}
spec:
    replicas: {1} 
    template:
      metadata:
        labels: 
          app: red-nginx{0}
      spec:
        containers:
        - name: nginx{0}
          image: aontimer/{0}
          ports:
          - containerPort: 80
          env:
          - name: DEMO_GREETING
            value: "Hello from the environment"
{2}
---
apiVersion: v1
kind: Service
metadata:
  name: red-service{0}
spec:
  type: NodePort
  selector:
    app: red-nginx{0}
  ports:
    - protocol: TCP
      port: 80

---
apiVersion: extensions/v1beta1
kind: Ingress
metadata:
  name: web{0}
spec:
  rules:
  - host: {0}.myweb.com
    http:
      paths:
      - backend:
          serviceName: red-service{0}
          servicePort: 80
EOF

rancher kubectl create -f ~/test.txt
""".format(obj.images,obj.Number,senvall)
            os.system(s)

            #其实我们做的只有这一部分 ********
            #obj.images += 'sss'
            #obj.save()
        return HttpResponse('{0}'.format(s), content_type='application/json')


# X admin的全局配置信息设置
class BaseSetting(object):
    # 主题功能开启
    enable_themes = True
    use_bootswatch = True


# x admin 全局配置参数信息设置
class GlobalSettings(object):
    site_title = "后台管理"
    site_footer = "mooc"
    # 收起菜单
    # menu_style = "accordion"

    def get_site_menu(self):
        return (
            {'title': '阿里服务器', 'menus': (
                {'title': 'key管理', 'url': self.get_model_url(AliKey, 'changelist')},
                {'title': 'Ecs管理', 'url': self.get_model_url(AliEcs, 'changelist')},
            )},

            {'title': 'DDos防御管理', 'menus': (
                {'title': 'DDos防御管理', 'url': self.get_model_url(RunDdos, 'changelist')},
            )},

            {'title': 'k8s管理', 'menus': (
                {'title': 'images管理', 'url': self.get_model_url(RunDocker, 'changelist')},
            )},
            {'title': '资产管理', 'menus': (
                {'title': 'dns管理', 'url': self.get_model_url(Dns, 'changelist')},
                {'title': 'dnsip管理', 'url': self.get_model_url(DnsIp, 'changelist')},
                {'title': '机房管理', 'url': self.get_model_url(JiFangGuanLi, 'changelist')},
                #{'title': '宿组管理', 'url': self.get_model_url(ShuZuGuanLi, 'changelist')},
                {'title': '主机管理', 'url': self.get_model_url(ZhuJiGuanLi, 'changelist')},

            )},
            {'title': '产品线管理', 'menus': (
                {'title': '产品管理', 'url': self.get_model_url(ChanPinGuanLi, 'changelist')},
                {'title': '项目管理', 'url': self.get_model_url(XiangMuGuanLi, 'changelist')},
                {'title': '负责人管理', 'url': self.get_model_url(FuZeRen, 'changelist')},

            )},
            {'title': '持续交付', 'menus': (
                {'title': '持续交付', 'url': self.get_model_url(ChiXuJiaoFu, 'changelist')},

            )},

            {'title': '基本信息', 'menus': (
                {'title': '供应商信息', 'url': self.get_model_url(GongShangXinXi, 'changelist')},
                {'title': '水泥信息', 'url': self.get_model_url(ShuiNiXinXi, 'changelist')},
                {'title': '客户信息', 'url': self.get_model_url(KeHuXinXi, 'changelist')},
                {'title': '装卸工信息', 'url': self.get_model_url(ZhuangXieGong, 'changelist')},
                {'title': '单位设置', 'url': self.get_model_url(DanWei, 'changelist')},
                {'title': '车辆信息', 'url': self.get_model_url(CheLiang, 'changelist')},

            )},
            {'title': '采购管理', 'menus': (
                {'title': '采购登记', 'url': self.get_model_url(CaiGou, 'changelist')},
                {'title': '采购损耗', 'url': self.get_model_url(CaiGouSunHao, 'changelist')},

            )},
            {'title': '销售管理', 'menus': (
                {'title': '销售登记', 'url': self.get_model_url(XiaoShouDengJi, 'changelist')},

            )},
            {'title': '运卸费管理', 'menus': (
                {'title': '司机结算', 'url': self.get_model_url(SiJiJieSuan, 'changelist')},
                {'title': '司机运费统计', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '司机运费明细', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '装卸结算', 'url': self.get_model_url(ZhuangXieJieSuan, 'changelist')},
                {'title': '装卸统计', 'url': self.get_model_url(KeHuXinXi, 'changelist')},
                {'title': '装卸工明细', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '采购运费结算', 'url': self.get_model_url(CaiGouFuKuan, 'changelist')},
                {'title': '采购运费统计', 'url': self.get_model_url(Banner, 'changelist')},

            )},

            {'title': '货款管理', 'menus': (
                {'title': '水泥货款', 'url': self.get_model_url(ShuiNi, 'changelist')},
                {'title': '客户货款统计', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '期间端收款汇总', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '采购付款', 'url': self.get_model_url(CaiGouFuKuan, 'changelist')},
                {'title': '采购付款统计', 'url': self.get_model_url(KeHuXinXi, 'changelist')},
                {'title': '返利登记', 'url': self.get_model_url(Banner, 'changelist')},

            )},

            {'title': '统计汇总', 'menus': (
                {'title': '当前库存', 'url': self.get_model_url(DangQianKuCun, 'changelist')},
                {'title': '采购明细', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '销售明细', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '区域销售明细', 'url': self.get_model_url(Permission, 'changelist')},
                {'title': '客户销售明细', 'url': self.get_model_url(KeHuXinXi, 'changelist')},
                {'title': '损耗明细', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '业务收入收支统计', 'url': self.get_model_url(KeHuXinXi, 'changelist')},

            )},

            {'title': '发布流程', 'menus': (
                {'title': '开发发布', 'url': self.get_model_url(UserAsk, 'changelist')},
                {'title': '测试发布', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '灰度发布', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '蓝绿发布', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '正式发布', 'url': self.get_model_url(Group, 'changelist')},

            )},
            {'title': '机构管理', 'menus': (
                {'title': '所在城市', 'url': self.get_model_url(CityDict, 'changelist')},
                {'title': '机构信息', 'url': self.get_model_url(CourseOrg, 'changelist')},
                {'title': '机构讲师', 'url': self.get_model_url(Teacher, 'changelist')},
            )},
            {'title': '课程管理', 'menus': (
                {'title': '课程信息', 'url': self.get_model_url(Course, 'changelist')},
                {'title': '章节信息', 'url': self.get_model_url(Lesson, 'changelist')},
                {'title': '视频信息', 'url': self.get_model_url(Video, 'changelist')},
                {'title': '课程资源', 'url': self.get_model_url(CourseResource, 'changelist')},
                {'title': '课程评论', 'url': self.get_model_url(CourseComments, 'changelist')},
            )},

            {'title': '用户管理', 'menus': (
                {'title': '用户信息', 'url': self.get_model_url(UserProfile, 'changelist')},
                {'title': '用户验证', 'url': self.get_model_url(EmailVerifyRecord, 'changelist')},
                {'title': '用户课程', 'url': self.get_model_url(UserCourse, 'changelist')},
                {'title': '用户收藏', 'url': self.get_model_url(UserFavorite, 'changelist')},
                {'title': '用户消息', 'url': self.get_model_url(UserMessage, 'changelist')},
            )},


            {'title': '系统管理', 'menus': (
                {'title': '用户咨询', 'url': self.get_model_url(UserAsk, 'changelist')},
                {'title': '首页轮播', 'url': self.get_model_url(Banner, 'changelist')},
                {'title': '用户分组', 'url': self.get_model_url(Group, 'changelist')},
                {'title': '用户权限', 'url': self.get_model_url(Permission, 'changelist')},
                {'title': '日志记录', 'url': self.get_model_url(Log, 'changelist')},
            )},
        )


# 创建admin的管理类,这里不再是继承admin，而是继承object
class EmailVerifyRecordAdmin(object):
    # 配置后台我们需要显示的列
    list_display = ['code', 'email','send_type', 'send_time']
    # 配置搜索字段,不做时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 配置筛选字段
    list_filter = ['code', 'email', 'send_type', 'send_time']


class RecordAdmin(object):
    data_charts = {
        "user_count": {'title': u"User Report", "x-field": "date", "y-field": ("user_count", "view_count"), "order": ('date',)},
        "avg_count": {'title': u"Avg Report", "x-field": "date", "y-field": ('avg_count',), "order": ('date',)}
    }


# 创建banner的管理类
class BannerAdmin(object):
    list_display = ['title', 'image', 'url','index', 'add_time']
    search_fields = ['title', 'image', 'url','index']
    list_filter = ['title', 'image', 'url','index', 'add_time']


# 创建阿里云key的管理类
class AliKeyAdmin(object):
    search_fields = ['ali_id']
#    list_display = ['name']
#    search_fields = ['name']
#    actions =[MyAction,]
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


# 创建阿里云Ecs的管理类
class AliEcsAdmin(object):
    search_fields = ['ip']

#    list_display = ['name']
#    search_fields = ['name']
    actions =[MyActionCeateEcs,]
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']

xadmin.site.register(AliKey, AliKeyAdmin)
xadmin.site.register(AliEcs, AliEcsAdmin)

# 创建供应商的管理类
class RunDdosAdmin(object):
    list_display = ['name']
    search_fields = ['name']
    actions =[MyAction,]
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']

xadmin.site.register(RunDdos, RunDdosAdmin)

# 创建供应商的管理类
class RunDockerAdmin(object):
    list_display = ['Name', 'Number', 'env', 'images', 'liveness']
    search_fields = ['Name']
    actions =[MyAction,]
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(RunDocker, RunDockerAdmin)


# 创建供应商的管理类
class GongShangXinXiAdmin(object):
    list_display = ['gong_shang_ming_chen', 'lian_xi_ren', 'lian_xi_dian_hua', 'lian_xi_di_zhi', 'bei_zhu']
    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(GongShangXinXi, GongShangXinXiAdmin)


# 创建水泥管理类
class ShuiNiXinXiAdmin(object):
    list_display = ['shui_ni_bian_hao', 'chang_jia', 'pin_pai', 'xing_hao', 'gui_ge', 'bei_zhu']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(ShuiNiXinXi, ShuiNiXinXiAdmin)


# 创建客户管理的管理类
class KeHuXinXiAdmin(object):
    list_display = ['ke_hu_bian_hao', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']
    search_fields = ['ke_hu_bian_hao', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']
    list_filter = ['ke_hu_bian_hao', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(KeHuXinXi, KeHuXinXiAdmin)


# 创建装卸工管理类
class ZhuangXieGongAdmin(object):
    list_display = ['zhuang_xie_gong', 'dianhua1', 'dianhua2', 'bei_zhu']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(ZhuangXieGong, ZhuangXieGongAdmin)


# 创建单位管理类
class DanWeiAdmin(object):
    list_display = ['dan_wei_ming_cheng', 'lian_xi_ren', 'lian_xi_dian_hua', 'lian_xi_di_zhi', 'bei_zhu']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(DanWei, DanWeiAdmin)


# 创建车辆管理类
class CheLiangAdmin(object):
    list_display = ['che_hao', 'si_ji', 'dian_hua1', 'dian_hua2', 'bei_zhu']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(CheLiang, CheLiangAdmin)


# 创建采购管理类
class CaiGouAdmin(object):
    list_display = ['cai_gou_ri_qi', 'chang_jia', 'chang_ku_ming_cheng', 'cai_gou_fang_shi', 'pin_pai', 'xing_hao', 'gui_ge', 'dan_jia', 'shu_liang', 'jin_e', 'che_chuan_hao', 'yun_jia', 'yun_fei', 'cao_zuo_yuan', 'bei_zhu']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(CaiGou, CaiGouAdmin)


# 创建采购损耗管理类
class CaiGouSunHaoAdmin(object):
    list_display = ['ri_qi', 'cang_ku_ming_cheng', 'cang_jia', 'pin_pai', 'xing_hao', 'gui_ge', 'sun_hao_shu_liang', 'cao_zuo_yuan', 'bei_zhu']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(CaiGouSunHao, CaiGouSunHaoAdmin)


# 创建销售登记管理类
class XiaoShouDengJiAdmin(object):
    list_display = ['dan_hao', 'ri_qi', 'qu_yu', 'ke_hu_ming_cheng', 'che_pai_hao', 'si_ji', 'si_ji_dian_hua', 'fu_kuan_fang_shi', 'jin_e', 'you_hui_jin_e', 'shi_shou_jin_e', 'cao_zuo_yuan', 'bei_zhu' ,'da_yin']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(XiaoShouDengJi, XiaoShouDengJiAdmin)


# 创建司机结算管理类
class SiJiJieSuanAdmin(object):
    list_display = ['ri_qi', 'che_pai_hao', 'si_ji_xing_ming', 'si_ji_dian_hua', 'dang_qian_yun_fei', 'fu_yun_fei', 'fu_kuan_fang_shi', 'wei_fu_yun_fei', 'cao_zuo_yuan', 'bei_zhu', 'da_yin']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(SiJiJieSuan, SiJiJieSuanAdmin)


# 创建装卸管理类
class ZhuangXieJieSuanAdmin(object):
    list_display = ['ri_qi', 'zhuang_xie_gong', 'dang_qian_zhuang_xie', 'fu_zhuang_xie_fei', 'wei_fu_zhuang_xie', 'cao_zuo_yuan', 'bei_zhu' ,'da_yin']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(ZhuangXieJieSuan, ZhuangXieJieSuanAdmin)


# 创建采购损耗管理类
class CaiGouYunFeiJieSuanAdmin(object):
    list_display = ['ri_qi', 'che_pai_hao', 'dang_qian_yun_fei', 'jie_suan_yun_fei', 'cao_zuo_yuan', 'bei_zhu']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(CaiGouYunFeiJieSuan, CaiGouYunFeiJieSuanAdmin)


# 创建水泥货款管理类
class ShuiNiAdmin(object):
    list_display = ['ri_qi', 'qu_yu', 'ke_hu_ming_cheng', 'wei_fu_huo_kuan', 'fu_kuan_jin_e', 'da_xie', 'fu_kuan_fang_shi' ,'sheng_yu_huo_kuan', 'cao_zuo_yuan', 'da_yin']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(ShuiNi, ShuiNiAdmin)


# 创建采购付款管理类
class CaiGouFuKuanAdmin(object):
    list_display = ['ri_qi', 'cang_jia', 'qian_kuan_jin_e', 'fu_kuan_jin_e', 'cao_zuo_yuan', 'da_yin']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(CaiGouFuKuan, CaiGouFuKuanAdmin)


# 创建库存管理类
class DangQianKuCunAdmin(object):
    list_display = ['chang_ku_ming_cheng', 'cang_jia', 'pin_pai', 'xing_hao', 'gui_ge', 'cai_gou_shu_liang', 'song_huo_shu_liang', 'sun_hao_shu_liang', 'ku_cun_shu_liang']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(DangQianKuCun, DangQianKuCunAdmin)


# 创建域名管理类
class DnsAdmin(object):
    list_display = ['name']


# 创建域名ip管理类
class DnsIpAdmin(object):
    list_display = ['yu_ming','zhu_ji_ji_lu', 'ji_lu_zhi', 'ip']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(Dns, DnsAdmin)
xadmin.site.register(DnsIp, DnsIpAdmin)



# 创建机房管理类
class JiFangGuanLiAdmin(object):
    list_display = ['ji_fang_biao_shi', 'ji_fang_ming_chen', 'ji_fang_di_zhi']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(JiFangGuanLi, JiFangGuanLiAdmin)


# 创建宿组管理类
class ShuZuGuanliAdmin(object):
    list_display = ['fu_wu_qi_zu', ['miao_su'],['ke_xuan_fu_wu_qi']]


# 创建主机管理类
class ZhuJiGuanLiAdmin(object):
    list_display = ['zu_ji_ming','guan_li_ip', 'suo_zai_ji_fang', 'qi_ta_ip', 'zi_can', 'she_bei_lei_xing', 'shang_jia_shi_jian', 'cpu_xing_hao', 'cpu_shu_liang', 'nei_cun_da_xiao', 'ying_pan_xin_xi', 'SN_hao_ma', 'suo_zai_wei_zhi', 'bei_zhu_xin_xi']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


#xadmin.site.register(ShuZuGuanli, ShuZuGuanLiAdmin)
xadmin.site.register(ZhuJiGuanLi, ZhuJiGuanLiAdmin)


# 创建产品管理类
class ChanPinGuanLiAdmin(object):
    list_display = ['zhu_ji_ming', 'guan_li_ip']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(ChanPinGuanLi, ChanPinGuanLiAdmin)


# 创建项目管理类
class XiangMuGuanLiAdmin(object):
    list_display = ['xiang_mu_ming_chen', 'xiang_mu_miao_su', 'yu_yan_lei_xing', 'cheng_xu_lei_xing']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']


xadmin.site.register(XiangMuGuanLi, XiangMuGuanLiAdmin)


# 创建负责人管理类
class FuZeRenAdmin(object):
    list_display = ['fu_ze_ren', 'shou_ji', 'qq', 'wechat']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']

xadmin.site.register(FuZeRen, FuZeRenAdmin)


# 创建负责人管理类
class ChiXuJiaoFuAdmin(object):
    pass
#    list_display = ['fu_ze_ren', 'shou_ji', 'qq', 'wei_chat']
#    search_fields = ['gong_shang_ming_chen']
#    list_filter = ['gong_shang_ming_chen', 'qu_yu', 'ke_hu_ming_chen', 'fu_ze_ren']

xadmin.site.register(ChiXuJiaoFu, ChiXuJiaoFuAdmin)


# 将model与admin管理器进行关联注册
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)

# 将Xadmin全局管理器与我们的view绑定注册。
xadmin.site.register(views.BaseAdminView, BaseSetting)

# 将头部与脚部信息进行注册:
xadmin.site.register(views.CommAdminView, GlobalSettings)