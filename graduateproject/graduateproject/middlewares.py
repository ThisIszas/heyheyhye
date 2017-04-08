import base64


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://127.0.0.1:1080'
        # proxy_user_pass = "us.bilibilitv.pw:PASSWORD"