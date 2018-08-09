import json
import redis
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.parsers import JSONParser,FormParser

from api import models
from api.utils.response import BaseResponse

CONN = redis.Redis(host='10.0.0.128', port=6379)  # CONN全局变量要大写
USER_ID = 1
class ShoppingCarView(ViewSetMixin,APIView):
    # parser_classes = [JSONParser,]  #解析器,可以再setting中配置
    # parser_classes = [JSONParser,FormParser,]
    def list(self, request, *args, **kwargs):
        """
        查看购物车信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        ret = {'code': 10000, 'data': None, 'error': None}
        try:
            shopping_car_course_list = []
            # pattern = "shopping_car_%s_*" % (USER_ID,)
            pattern = settings.LUFFY_SHOPPING_CAR % (USER_ID, '*',)
            user_key_list = CONN.keys(pattern)
            for key in user_key_list:
                temp = {
                    'id': CONN.hget(key, 'id').decode('utf-8'),
                    'name': CONN.hget(key, 'name').decode('utf-8'),
                    'img': CONN.hget(key, 'img').decode('utf-8'),
                    'default_price_id': CONN.hget(key, 'default_price_id').decode('utf-8'),
                    'price_policy_dict': json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))
                }
                shopping_car_course_list.append(temp)

            ret['data'] = shopping_car_course_list
        except Exception as e:
            ret['code'] = 10005
            ret['error'] = '获取购物车数据失败'

        return Response(ret)


    def create(self, request, *args, **kwargs):
        '''
        相关问题：
                a. 如果让你编写一个API程序，你需要先做什么？
                    - 业务需求
                    - 统一数据传输格式
                    - 表结构设计
                    - 程序开发
                b. django restful framework的解析器的parser_classes的作用？
                    根据请求中Content-Type请求头的值，选择指定解析器对请求体中的数据进行解析。
                    如：
                        请求头中含有Content-type: application/json 则内部使用的是JSONParser，JSONParser可以自动去请求体request.body中
                        获取请求数据，然后进行 字节转字符串、json.loads反序列化；

                c. 支持多个解析器（一般只是使用JSONParser即可）

        '''

        course_id = request.data.get('courseid')
        policy_id = request.data.get('policyid')
        # 判断合法性
        #   - 课程是否存在？
        #   - 价格策略是否合法？
        course = models.Course.objects.filter(id=course_id,degree_course__isnull=True).first()
        if not course:  #   - 课程是否存在？
            return Response({'code': 10001, 'error': '亲，课程不存在哟！'})#简单逻辑往上放
        price_policy_queryset = course.price_policy.all()
        # 价格策略是否合法？
        price_policy_dict = {} #这里写字典更好，查找速度更快
        for item in price_policy_queryset:
            temp = {
                'id': item.id,
                'price': item.price,
                'valid_period': item.valid_period,
                'valid_period_display': item.get_valid_period_display() #获取到中文
            }
            #在之所以要给字典赋值，是因为以后判断用户价格策略存不存在，就可以通过price_policy_dict来判断
            price_policy_dict[item.id] = temp # 字典中有5对值 key=item.id value=temp
        if policy_id not in price_policy_dict: #判断用户价格策略存不存在
            return Response({'code': 10002, 'error': '对不起没有该价格策略！'})
        # print(request.data)
        #request_request  (这样才是原生的django的request)

        # 把商品和价格策略信息放入购物车 SHOPPING_CAR
        '''
        购物车中要放：
            课程ID
            课程名称
            课程图片
            默认选中的价格策略
            所有价格策略
    redis 中数据存放格式：不支持字典嵌套字典，故方式1不好
     方式1 {
        1（用户id）:{
                1(课程id):{ #详细信息#
                            课程ID
                            课程名称
                            课程图片
                            1
                            所有价格策略
                },
                2(课程id):{
                            课程ID
                            课程名称
                            课程图片
                            默认选中的价格策略
                            所有价格策略
                }
            },
            

        方式2{比上面的嵌套更好
            shopping_car_（用户id）_(课程id)
            shopping_car_1_1:{
                id:课程ID
                name:课程名称
                img:课程图片
                defaut:默认选中的价格策略
                price_list:所有价格策略
            },
            shopping_car_1_3:{
                id:课程ID
                name:课程名称
                img:课程图片
                defaut:默认选中的价格策略
                price_list:所有价格策略
            },
            shopping_car_2_3:{
                id:课程ID
                name:课程名称
                img:课程图片
                defaut:默认选中的价格策略
                price_list:所有价格策略
            }
        }

        '''
        key = "shopping_car_%s_%s" % (USER_ID,course_id) #拼接构造字典的key
        CONN.hset(key, 'id', course_id)
        CONN.hset(key, 'name', course.name)
        CONN.hset(key, 'img', course.course_img)
        CONN.hset(key, 'default_price_id', policy_id)
        CONN.hset(key, 'price_policy_dict', json.dumps(price_policy_dict)) # 这里json.dumps，是因为不能字典套字典

        return Response({'code': 10000, 'data': '购买成功'})

    def destroy(self, request, *args, **kwargs):
        """
        删除购物车中的某个课程
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        response = BaseResponse()
        try:
            courseid = request.GET.get('courseid')
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, courseid,)#构造一个key，添加一个要删除的courseid
            CONN.delete(key)  #delete()删除全部把key传过去就可以了，是redis中的方法
            response.data = '删除成功'
        except Exception as e:
            response.code = 10006
            response.error = '删除失败'
        return Response(response.dict)

    def update(self, request, *args, **kwargs):
        """
        修改只支持用户选中的价格策略的修改
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        """
        修改时，用户需要给后台发数据，要修改的课程和价格策略
        1. 获取课程ID、要修改的价格策略ID
        2. 校验合法性（去redis中）（一定要校验，只是不用去数据库，直接去redis中处理）
        """
        response = BaseResponse()
        try:
            course_id = request.data.get('courseid')
            policy_id = str(request.data.get('policyid')) if request.data.get('policyid') else None
            #request.data.get('policyid') 得到的是int类型而json 是str类型，故需要转换
            key = settings.LUFFY_SHOPPING_CAR % (USER_ID, course_id,)

            if not CONN.exists(key): #exists（）存在
                response.code = 10007
                response.error = '课程不存在'
                return Response(response.dict)

            price_policy_dict = json.loads(CONN.hget(key, 'price_policy_dict').decode('utf-8'))#获取所有的价格策略
            if policy_id not in price_policy_dict:  #判断价格策略id是否存在
                response.code = 10008
                response.error = '价格策略不存在'
                return Response(response.dict)

            CONN.hset(key, 'default_price_id', policy_id)  # 用hset,修改default_price_id，在设置一次就可以
            CONN.expire(key, 20 * 60)
            response.data = '修改成功'
        except Exception as e:
            response.code = 10009
            response.error = '修改失败'
        return Response(response.dict)