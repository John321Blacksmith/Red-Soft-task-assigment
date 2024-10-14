FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /vm_manager
COPY . /vm_manager

CMD ["python", "launch.py"]