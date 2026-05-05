import os

from dotenv import load_dotenv
import redis

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")

# redis client 생성
# redis 에서 가져온 값을 bytes 가 아니라 문자열로 다루기 쉽게 함
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)