#!/usr/bin/env python3

import json
import re

from tornado.web import RequestHandler

from config import REGION_COLLECTION, MONGODB_NAME
from crawl_info import crawl_administrative_region
from db_motor import BaseMotor


class BaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(BaseHandler, self).__init__(application, request, **kwargs)

    def write_response(self, response, code=0, message='SUCCESS'):
        self.set_header('Content-type', 'application/json')
        _response = {
            "code": code,
            "data": response,
            "message": message
        }
        self.write(json.dumps(_response))
        self.finish()


class QueryApiHandler(BaseHandler):
    async def get(self):
        region_id = self.get_argument('id', None)
        depth = self.get_argument('depth', 1)
        keywords = self.get_argument('keywords', None)
        query_condition = {}

        if not (region_id or keywords):
            self.write_response('', -1, '请输入区域编号或者区域名称的关键字')
            return
        try:
            if region_id:
                region_id = int(region_id)
                if region_id < 110000 or region_id > 820000:
                    self.write_response('', -1, '区域编号参数错误，应该在110000-820000之间')
                    return
                query_condition['_id'] = str(region_id)

            depth = int(depth)
            if depth <= 0 or depth > 3:
                self.write_response('', -1, '层级深度参数错误，最大层级深度数为3且默认为1')
                return
            query_condition['depth'] = 1

            if keywords:
                keywords = str(keywords)
                if len(keywords) > 20 and re.match('^[\u4e00-\u9fa5]+$', keywords) is None:
                    self.write_response('', -1, '请输入合理的区域名称关键字')
                    return
                query_condition['name'] = {'$regex': '^{}'.format(keywords)}

        except (TypeError, ValueError):
            self.write_response('', -1, '传递参数类型有误')
            return

        try:
            coll = BaseMotor().client[MONGODB_NAME][REGION_COLLECTION]
            count = await coll.count_documents({})
            if not count:
                status = await crawl_administrative_region()
                if not status:
                    self.write_response('', -1, '爬取数据失败')
                    return
            data, code, msg = await self.query_data(coll, query_condition, depth)
            self.write_response(data, code, msg)
        except Exception:
            self.write_response('', -1, '数据库操作异常')

    @staticmethod
    async def query_data(collection, query_condition, depth):
        res = await collection.find_one(query_condition)
        if res:
            data = {
                'id': res['_id'],
                'name': res['name'],
                'districts': []
            }

            if depth > 1:
                province_num = res['_id'][:2]
                docs = await collection.find({'depth': {'$lte': depth, '$gt': 1}, '_id': {'$regex': '^{}'.format(
                    province_num)}}).sort('_id', 1).to_list(length=10000)
                if docs:
                    _data = {}
                    for doc in docs:
                        region_num = doc['_id'][:4]
                        item = {
                            'id': doc['_id'],
                            'name': doc['name'],
                            'districts': []
                        }
                        if doc['depth'] == 2:
                            _data[region_num] = item

                        elif doc['depth'] == 3 and region_num not in _data:
                            _data[region_num] = {
                                'id': '{}00'.format(region_num),
                                'name': '地级行政区',
                                'districts': []
                            }
                        else:
                            _data[region_num]['districts'].append(item)

                    data['districts'] = list(_data.values())

            return data, 0, 'SUCCESS'

        else:
            return '', -1, '查询数据错误，请检查区域编号或区域关键字，区域关键字必须是省级行政区'
