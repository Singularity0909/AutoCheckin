得益于 [zhl 同学](https://piggyzhl.top/) 提供的灵感和核心代码，我们实现了微校园每日健康打卡脚本。

这几天闲来无事，我给代码增加了 MySQL 模块，使得批量打卡高度自动化。

其实原理很简单，就是利用 Python Selenium 库控制浏览器自动操作，可以把它理解为高级的按键精灵。

保存信息的数据库表结构也很简单：

<img src = "https://cdn.jsdelivr.net/gh/singularity0909/cdn/img/screenshot/check_in_mysql.png" width = "600"/>

感兴趣的同学可以自己动手调试，日后若问卷页面结构发生变化，可以一起讨论改进方案。

想要体验打卡的同学可以在 [博文](https://www.macrohard.cn/archives/19/) 下方备注自己的学号，为了便于数据库读取，**仅学号即可**。

最后，希望疫情早日结束，武汉加油，中国加油！