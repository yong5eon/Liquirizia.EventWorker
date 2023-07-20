# Liquirizia.EventWorker
이벤트 처리를 위한 이벤트 워커

## 사용 방법

### 이벤트 처리 어플리케이션 정의
```python
from Liquirizia.EventRunner import EventRunner


class SampleEventRunner(EventRunner):
	def __init__(self, event: str, headers: dict = None):
		# TODO : do something
		return
	
	def run(self, body=None):
		# TODO : do something
		return
```

### 이벤트 처리 어플리케이션의 속성 정의
```python
from Liquirizia.EventRunner import EventRunnerProperties
from Liquirizia.EventRunner.Types import EventWorker


properties = EventRunnerProperties(
	SampleEventRunner,
	type=EventWorker(
		event='${EVENT_STRING}',
		name='${BROKER_NAME}',
		queue='${QUEUE_NAME}',
	)
)
```

### 이벤트 워커 실행
```python
from Liquirizia.EventWorker import EventWorker

worker = EventWorker()
worker.add(properties)
worker.load('${PATH_OF_PROPERTIES}')
worker.run(${MAX_CONCURRENCY_WORK})
```

### 이벤트 호출

#### 발행
```python
from Liquirizia.EventBroker import EventBrokerHelper

EventBrokerHelper.Publish(
	'${BROKER_NAME}',
	'${EVENT_STRING}',
	headers=${HEADERS},
	body=${BODY}
)
```

#### 호출
```python
from Liquirizia.EventBroker import EventBrokerHelper

res = EventBrokerHelper.Call(
	'${BROKER_NAME}',
	'${EVENT_STRING}',
	headers=${HEADERS},
	body=${BODY}
)
```