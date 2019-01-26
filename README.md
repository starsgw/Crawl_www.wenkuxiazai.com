# Crawl_www.wenkuxiazai.com
该网站具有较强的反爬机制，体现在封ip严重，高频验证。所以采用高匿代理ip（将请求间隔时间延长）或者动态ip解决。

1.多进程爬取
2.请求方式：requests.get()
3.python开发版本：python3
4.随机从代理池中取出ip(这里使用的方法仅仅是放在列表中，可能存在被封ip不能及时被删除),另一种方法可以将ip存入MongoDB中，如果某个ip被封，就修改该ip的状态码，在下次从MongoDB中取出ip时只取没有被修改状态码的ip
