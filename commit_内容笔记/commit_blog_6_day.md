#搭建MVC 
#编写具体的url处理函数,,时候get和post 进行绑定
    小测试helloworld ,需要修改return .因为还没建立模板处理
    还需要在运行开始时加入数据库连接池
#根据jinjia2 模板
    
#如何将函数返回值转化为web.response对象呢？
```
    使用拦截器,在执行完成handler函数后,拦截器自动对把return的结果转换为 web.response
```
```
    拦截器的功能 类似装饰器解释的多层函数调用
    拦截器的原理相当于多层函数参数的调用
    app =10
    request =10
    def func(request):
        print("func")
    def log1(app,func):
       print("log1")
       def handler_log1(request):
            print("handler_log1_start")
            func(requset)        #也可以写成fun(request) 先执行函数,后面可以在加入prnit 语句
            print("handler_log1_end")
       return handler_log1
    
    def log2(app,func):
       print("log2")
       def handler_log2(request):
            print("handler_log2")
            return func(requset)
       return handler_log2
    log2(app,log1(app,func))(request)       执行语句
    
    1: log1(app,handler) 语句执行后,输出'log1',返回一个执行函数 handler_log1
    2: handler  = handler_log1    函数名赋值
    3: log2(app,handler) 语句执行后,输出'log2',返回一个执行函数 handler_log2
    4: handler  = handler_log2    函数名赋值
    5: 执行函数 handler, 等于执行函数 handler_log2, 输出'handler_log2',执行函数handler_log1,输出'handler_log1',最后调用函数func(request)
    6:在使用return func  这表示: 在func 函数之前执行,使用func(),后面再加处理,可以做到 先处理func,在对func的返回值进行修改的中间件功能
```