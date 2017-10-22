#新增coroweb.py
#编写web框架
```
    原因:aiohttp太底层.对应URL编写函数,需要自己解析,并自己登记函数
    async def handle_url_xxx(request):
        #需要自己解析request,还记得flask的@app.route('/', methods=['GET', 'POST'])
        url_param = request.match_info['key']  
        query_params = parse_qs(request.query_string)   
        #需要自己构造返回的html 太麻烦了,还记得模板吗?
        text = render('template', data)             
        return web.Response(text.encode('utf-8'))   
```
##编写GET,POST的装饰器
```
    原理:自动解析request中的method 和path,生成属性,绑定到装饰的url处理函数上.
```
##编写RequestHandler
```
    目的就是从URL函数中分析其需要接收的参数，从request中获取必要的参数，调用URL函数。
    准备:用于检查reques中的参数的函数
         http://docs.python-requests.org/zh_CN/latest/index.html
         在request中包含了各种参数
         http://blog.csdn.net/iloveyin/article/details/21444613
```
##编写add_route   将单个函数和 url 进行绑定
##编写add_routes  批量的整个模块的和函数和 url 进行绑定
##编写add_static  静态文件请求,直接返回,不需要绑定
#新增ApiErrorType.py
##自定义ERROR
```
    用于 raise 异常
```


