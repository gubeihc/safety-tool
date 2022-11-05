class Config(object):
    import pathlib
    # 请求配置 这个下面都是req_mode 的配置

    enable_request_proxy = True  # 是否使用代理(全局开关，默认False)
    proxy_all_module = False  # 代理所有模块
    proxy_partial_module = ['iphackertarget', 'ipdnslytics', "ipfreeapirobtex", "iprapiddns",
                             "ipviewdns"]  # 代理自定义的模块

    request_proxy_pool = 'http://127.0.0.1:7890'  # 代理池地址
    # 请求超时
    Req_total = 60
    Req_connect = 60
    Req_sock_connect = 60
    Req_sock_read = 60
    # 路径设置
    src_list_directory = pathlib.Path(__file__).parent.parent


settings = Config()
