from redis import Redis
from rq import Worker

from .config import settings


def main() -> None:
    connection = Redis.from_url(settings.redis_url)
    worker = Worker([settings.rq_queue_name], connection=connection)
    worker.work()


if __name__ == "__main__":
    main()
