# Liquirizia.EventWorker

이벤트 처리를 위한 이벤트 워커

## 이벤트 러너 작성 및 등록

```python
from Liquirizia.EventWorker import (
  EventProperties,
  EventRunner,
  EventComplete,
  EventError,
)

class SampleComplete(EventRunnerComplete):
  def __call__(self, completion, *args, **kwargs):
    # 완료 처리
    ...
    return
  
class SampleError(EventRunnerError):
  def __call__(self, error: BaseException, *args, **kwargs):
    # 오류 처리
    ...
    return


@EventProperties(
  event='${EVENT}',
  completes=SampleComplete(),
  errors=SampleError(),
)
class SampleRunner(EventRunner):
  def run(self, *args, **kwargs):
    # 이벤트 처리
    ...
    return ... # 완료 처리를 위한 값 리턴
```

## 이벤트 인보커 작성

```python
from Liquirizia.EventWorker from Invoker, Pool, Parameters


class SampleInvoker(Invoker):
  def __init__(self, pool: Pool):
    self.pool = pool
    # 이벤트를 발생 시키기 위한 초기화
    ...
    return

  def run(self):
    ...
    self.pool.run('${EVENT}', Parameters(...)) # 이벤트를 발행
    ...
    return

  def stop(self):
    # 이벤트 발생을 종료 시킴
    ...
    return
```

## 이벤트 워커 작성 및 실행

```python
from Liquirizia.EventWorker import Worker
from signal import signal, SIGINT

worker = Worker(ThreadPool(), SampleInvoker)

def stop(signal, frame):
  worker.stop()
  return

signal(SIGINT, stop)

worker.run()
```

## 예제

- [이벤트 워커](sample/Sample.py)
- [이벤트 브로커로 부터 컨슈밍을 하여 처리 하는 이벤트 워커](sample/Sample.EventBroker.RabbitMQ.py)
- [다중 이벤트 브로커로 부터 컨슈밍을 하여 처리 하는 이벤트 워커](sample/Sample.EventBroker.RabbitMQ.MultipleSubscriptions.py)
- [인터발 방식의 이번트 워커](sample/Sample.EventInterval.py)
- [시간 스케줄 방식의 이벤트 워커](sample/Sample.EventScheduler.py)
