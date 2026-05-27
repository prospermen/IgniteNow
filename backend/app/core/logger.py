import json
import logging
import os
from logging.handlers import RotatingFileHandler

import structlog

from ..database import SessionLocal
from ..models import SystemLog


class DatabaseLogHandler(logging.Handler):
    def emit(self, record):
        if record.levelno < logging.WARNING:
            return  # 过滤，仅记录 WARNING 和 ERROR 级别至数据库

        try:
            # Structlog JSONRenderer 会将输出转为 JSON 字符串
            log_data = json.loads(record.msg)
            
            with SessionLocal() as db:
                sys_log = SystemLog(
                    request_id=log_data.get("request_id", ""),
                    user_id=str(log_data.get("user_id", "")),
                    episode_id=str(log_data.get("episode_id", "")),
                    job_id=str(log_data.get("job_id", "")),
                    level=record.levelname.lower(),
                    message=log_data.get("event", ""),
                    error_stack=log_data.get("exception", ""),
                    context_json=record.msg
                )
                db.add(sys_log)
                db.commit()
        except Exception as e:
            # Fallback 避免日志递归崩溃
            print(f"Failed to write log to Database: {e}")


def setup_logger():
    log_dir = os.environ.get("LOG_DIR", "/app/backend/logs")
    try:
        os.makedirs(log_dir, exist_ok=True)
    except OSError:
        # Fallback for local testing outside Docker
        log_dir = "./backend/logs"
        os.makedirs(log_dir, exist_ok=True)

    # 重置根 Logger
    logging.basicConfig(format="%(message)s", level=logging.INFO, handlers=[])
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # 1. Stdout 控制台 Handler (Docker logs)
    stream_handler = logging.StreamHandler()
    root_logger.addHandler(stream_handler)

    # 2. 文件 Handler (持久化映射到宿主机)
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "ignitenow.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5
    )
    root_logger.addHandler(file_handler)

    # 3. 数据库 Handler (过滤高优先级)
    db_handler = DatabaseLogHandler()
    root_logger.addHandler(db_handler)

    # 配置 structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

def get_logger(name="ignitenow"):
    return structlog.get_logger(name)
