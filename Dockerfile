FROM python:3.12-slim-bookworm

WORKDIR /opt/mibiao

COPY ./pyproject.toml /opt/mibiao/pyproject.toml
RUN mkdir -p /opt/mibiao/src && pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple -e .

COPY . /opt/mibiao
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple -e .


# docker build -f Dockerfile -t mibiao .

# docker run --rm -it mibiao bash
