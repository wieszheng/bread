FROM python:3.12.0-slim as builder
WORKDIR /bread
COPY ./requirements.txt .

RUN python -m venv /bread/venv \
    && /bread/venv/bin/pip install --upgrade pip \
    && /bread/venv/bin/pip install --index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    --no-cache-dir -r requirements.txt

RUN apt update -y \
    && apt install -y tzdata wget \
    && apt clean



FROM python:3.12.0-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /bread
COPY . .
COPY --from=builder /bread/venv/ /bread/venv/
COPY --from=builder /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 5021
CMD ["/bread/venv/bin/supervisord", "-c", "/bread/supervisord.conf"]