import arrow
import aiohttp
import asyncio

import json
import redis
import uuid

from aiohttp import web
from email_validator import validate_email
from pymongo import MongoClient


client = MongoClient()
db = client['allyfocus']
rs = redis.StrictRedis(decode_responses=True)

ALLOWED_HEADERS = ','.join((
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-requested-with',
    'x-csrftoken',
))


def set_cors_headers(request, response):
    response.headers['Access-Control-Allow-Origin'] = request.headers.get(
        'Origin', '*')
    response.headers['Access-Control-Allow-Methods'] = request.method
    response.headers['Access-Control-Allow-Headers'] = ALLOWED_HEADERS
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response


@web.middleware
async def md_cors_factory(request, handler):
    if request.method == 'OPTIONS':
        return set_cors_headers(request, web.Response())
    else:
        response = await handler(request)
        return set_cors_headers(request, response)


def find(**kwargs):
    result = [x for x in db.find_one(kwargs)]
    return result


async def api_get(request):
    collection = request.match_info['collection']
    if collection == 'emails':
        return web.json_response({}, status=403)
    key = request.match_info['key']
    result = db[collection].find_one({'_id': key})
    if result:
        result.pop('_id')
        return web.json_response(result)
    return web.json_response({}, status=404)


async def api_search(request):
    collection = request.match_info['collection']
    if collection == 'emails':
        return web.json_response({}, status=403)
    limit = request.rel_url.query.get('limit', 100)
    skip = request.rel_url.query.get('skip', 0)
    search = request.rel_url.query.get('search')
    order_by = request.rel_url.query.get('order_by', '-created')
    direction = -1 if order_by.startswith('-') else 1
    order_by = order_by[1:] if direction == -1 else order_by
    args = request.rel_url.query.get('args')
    args = json.loads(args) if args else {}
    if search:
        result = [x for x in db[collection].find(
            {'$text': {'$search': search}, **args}).limit(limit).skip(skip)]
        # result = [x for x in db[collection]
        #           .find({'$or': [
        #               {'title': {'$regex': search}},
        #               {'text': {'$regex': search}}
        #           ], **args})
        #           .limit(limit).skip(skip)]
    elif args:
        result = [x for x in db[collection]
                  .find(args)
                  .limit(limit)
                  .skip(skip)
                  .sort(order_by, direction)]
    else:
        result = [x for x in db[collection]
                  .find()
                  .limit(limit)
                  .skip(skip)
                  .sort(order_by, direction)]
    return web.json_response(result)


async def api_set(request):
    uid = request.rel_url.query.get('uid')
    allowed = []
    if uid not in allowed:
        return web.json_response({}, status=403)
    collection = request.match_info['collection']
    if collection == 'emails':
        return web.json_response({}, status=403)
    obj = await request.json()
    if obj['key'] != '':
        db[collection].update_one({'_id': obj['key']}, {
                                  '$set': obj}, upsert=True)
    else:
        return web.json_response({'error': 'Empty key.'}, status=400)
    return web.json_response({})


async def api_delete(request):
    uid = request.rel_url.query.get('uid')
    allowed = []
    if uid not in allowed:
        return web.json_response({}, status=403)
    collection = request.match_info['collection']
    key = request.match_info['key']
    result = db[collection].delete_one({'_id': key})
    if result:
        return web.json_response({})
    return web.json_response({}, status=404)


async def api_ping(request):
    return web.json_response({'msg': 'pong'})


async def api_submit_email(req):
    address = req.rel_url.query.get('address')
    email = req.match_info['email'].strip()
    try:
        validate_email(email)
    except:
        return web.json_response({'msg': 'Invalid email'}, status=400)
    popup_coupons_uid = str(uuid.uuid4())
    now = arrow.now().format('YYYY-MM-DD HH:mm:ss')
    db['emails'].update_one({'_id': popup_coupons_uid}, {'$set': {
                            'email': email, 'address': address, 'date': now, 'campaign': 'popup_coupons', }}, upsert=True)
    return web.json_response({'popup_coupons_uid': popup_coupons_uid, 'coupon_id': '123', 'coupon_text': 'Coupon 2021!'})


async def api_db_emails(request):
    uid = request.rel_url.query.get('uid')
    allowed = []
    if uid not in allowed:
        return web.json_response({}, status=403)
    result = ['{},{},{},{},{}'.format(
        x['date'], x['email'], x['address'], x['campaign'], x['_id']) for x in db['emails'].find()]
    if result:
        return web.Response(text='\n'.join(result))
    return web.json_response({}, status=404)


async def payments_checker():
    # TODO check etherscan txs (eth+xyr), send coupons
    pass


app = web.Application(middlewares=[md_cors_factory])

app.router.add_route('GET', '/api/ping', api_ping)
app.router.add_route('GET', '/api/search/{collection}', api_search)
app.router.add_route('GET', '/api/get/{collection}/{key}', api_get)
app.router.add_route('POST', '/api/set/{collection}', api_set)
app.router.add_route('POST', '/api/delete/{collection}/{key}', api_delete)
app.router.add_route('POST', '/api/submit/email/{email}', api_submit_email)
app.router.add_route('GET', '/api/db/emails', api_db_emails)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=3005)
