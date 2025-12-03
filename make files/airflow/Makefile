# مسار البيئة الافتراضية
VENV_PATH=/home/eyad/data_eng/venv/bin/activate

# إعادة تسلسل الـ DAGs
serialize:
	. $(VENV_PATH) && airflow dags reserialize

# تشغيل الـ scheduler في الخلفية وحفظ PID و log
scheduler:
	mkdir -p logs
	. $(VENV_PATH) && nohup airflow scheduler > logs/scheduler.log 2>&1 &
	echo $$! > logs/scheduler.pid

# تشغيل الـ API server في الخلفية وحفظ PID و log
api:
	mkdir -p logs
	. $(VENV_PATH) && setsid airflow api-server > logs/api.log 2>&1 < /dev/null &
	echo $$! > logs/api.pid

# تشغيل الثلاثة مع بعض
start: serialize
	mkdir -p logs
	. $(VENV_PATH) && nohup airflow scheduler > logs/scheduler.log 2>&1 &
	echo $$! > logs/scheduler.pid
	. $(VENV_PATH) && setsid airflow api-server > logs/api.log 2>&1 < /dev/null &
	echo $$! > logs/api.pid

# إيقاف الخدمات باستخدام PID
stop:
	@if [ -f logs/scheduler.pid ]; then kill -9 `cat logs/scheduler.pid`; rm logs/scheduler.pid; fi
	@if [ -f logs/api.pid ]; then kill -9 `cat logs/api.pid`; rm logs/api.pid; fi

# عرض آخر 10 أسطر من الـ logs
logs-scheduler:
	tail -n 10 -f logs/scheduler.log

logs-api:
	tail -n 10 -f logs/api.log
