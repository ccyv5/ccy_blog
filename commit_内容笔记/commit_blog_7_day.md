#了解前端模板的实现jinjia2 
```angular2html
    开始时调用init_jinjia2 函数,对app 绑定模板属性.
    在拦截去中web.reposens 时,参数用app.template 属性进行渲染模块.自己去匹配html中的内容.
    通过env 创建一个实例,实现加载模板,
    option是用于指定的 规制的 模板编写规制的
```
#构建前端的功能画面
```angular2html
    不建议理解太多,直接看demo,抄下来
```
```angular2html
    直接使用廖大github上的文件,保持文件一致.
    static/
        +- css/
        |  +- addons/
        |  |  +- uikit.addons.min.css
        |  |  +- uikit.almost-flat.addons.min.css
        |  |  +- uikit.gradient.addons.min.css
        |  +- awesome.css
        |  +- uikit.almost-flat.addons.min.css
        |  +- uikit.gradient.addons.min.css
        |  +- uikit.min.css
        +- fonts/
        |  +- fontawesome-webfont.eot
        |  +- fontawesome-webfont.ttf
        |  +- fontawesome-webfont.woff
        |  +- FontAwesome.otf
        +- js/
           +- awesome.js
           +- html5.js
           +- jquery.min.js
           +- uikit.min.js
```