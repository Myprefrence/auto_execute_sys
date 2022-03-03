import datetime
import logging

from common.normal import get_root_path, get_config


class Logger:
    """
    @desc
    创建 logging 对象
    日志等级: NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

    :param console_level    控制台输出的日志等级
    :param logfile_level    输出到文件的日志等级
    :param write_file       是否输出日志到文件, 0-关闭, 1-开启
    :param file_path        开启输出日志到文件的位置
    :param console_log      开启输出日志到控制台, 0-关闭, 1-开启
    """

    def __init__(self, console_level=None, logfile_level=None, write_file=None, file_path=None, console_log=None):
        root_path = get_root_path()
        config = get_config(r'config\utils.ini')
        today = datetime.datetime.now().__format__('%Y-%m-%d')

        self.console_level = config.get('logger', 'console_level') if console_level is None else console_level
        self.logfile_level = config.get('logger', 'logfile_level') if logfile_level is None else logfile_level
        self.console_log = config.get('logger', 'console_log') if console_log is None else console_log
        self.write_file = config.get('logger', 'write_file') if write_file is None else write_file
        self.file_path = rf'{root_path}\logs\{today}.log' if file_path is None else file_path

        self.logger = logging.getLogger(__name__)

    def get_logger(self):
        logger_level = {
            'NOTSET': logging.NOTSET,
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }[self.console_level]

        self.logger.setLevel(logger_level)
        formatter = '%(asctime)s %(levelname)s %(funcName)s %(message)s'

        if str(self.console_log) == '1':
            console = logging.StreamHandler()
            console.setLevel(logger_level)
            console.setFormatter(logging.Formatter(formatter))
            self.logger.addHandler(console)

        if str(self.write_file) == '1':
            logfile = logging.FileHandler(self.file_path, encoding='utf-8')
            logfile.setLevel(self.logfile_level)
            logfile.setFormatter(logging.Formatter(formatter))
            self.logger.addHandler(logfile)

        return self.logger
