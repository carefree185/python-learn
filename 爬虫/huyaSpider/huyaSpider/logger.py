import logging

streamLogger = logging.getLogger('stream')
streamLogger.setLevel(logging.INFO)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter(fmt='%(asctime)s -- %(name)s -- %(filename)s -- %(levelname)s -- %(message)s')  # 日志格式控制
streamHandler.setFormatter(formatter)
streamLogger.addHandler(streamHandler)
