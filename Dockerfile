FROM python:3.12.4

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /vm_manager
COPY . /vm_manager

EXPOSE 8000

CMD ["python", "server_side/launch.py"]