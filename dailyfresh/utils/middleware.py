class UrlPathRecordMiddleWare(object):
    exclide_url = ['/user/login/','/user/register/','/user/login_out/']
    # process_view中间件函数在每次调用视图函数之前都会被调用，在这里用来记录请求路径

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        if request.path not in UrlPathRecordMiddleWare.exclide_url and not request.is_ajax() and request.method=='GET':
            request.session['url_path'] = request.path
