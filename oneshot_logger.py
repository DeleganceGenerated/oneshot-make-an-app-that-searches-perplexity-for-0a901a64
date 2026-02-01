import json
import os
from datetime import datetime, timezone

import redis

_redis = redis.from_url(os.environ.get('REDIS_LOGS_URL') or os.environ.get('REDIS_URL'))
_app_name = os.environ.get('APP_NAME', 'unknown')

def log(level: str, message: str, **context):
    _redis.xadd(
        f'logs:{_app_name}',
        {
            'level': level,
            'message': message,
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'context': json.dumps(context),
        },
        maxlen=10000,
        approximate=True,
    )
