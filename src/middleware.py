import time
from uuid import uuid4
from fastapi import Request
from logger import Logger
from endpoints import REQUEST_COUNT, REQUEST_DURATION, REQUEST_SIZE, RESPONSE_SIZE
from tasks import _generate_fake_user


async def middleware(request: Request, call_next):
    REQUEST_SIZE.labels(request.url.path).observe(len(await request.body()))

    start_time = time.time()

    try:
        rid = str(uuid4())
        logger = Logger(rid)
        # request.state.logger = logger
        logger.debug("Incoming request...", remote_addr=request.client.host, url=request.url, method=request.method)
        response = await call_next(request)
        if response.status_code < 400:
            logger.debug("Request completed", remote_addr=request.client.host, url=request.url, method=request.method, status_code=response.status_code)

        return response
    except Exception as err:
        print(err)
    finally:
        try:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(request.url.path, request.method).observe(duration)
            content_length = response.headers.get('Content-Length')
            if content_length:
                RESPONSE_SIZE.labels(request.url.path).observe(int(content_length))
            REQUEST_COUNT.labels(str(response.status_code)).inc()
        except Exception as err:
            print(err)