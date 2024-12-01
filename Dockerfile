FROM python:3.12-slim-bookworm as python3
WORKDIR /opt/mibiao
COPY ./src /opt/mibiao/src
COPY ./pyproject.toml /opt/mibiao/pyproject.toml
RUN  python -m pip install --upgrade build  && python -m build


FROM python:3.12-slim-bookworm


RUN apt update \
    && apt install --no-install-recommends -y vim \
    && apt install --no-install-recommends -y procps  \
    && apt install --no-install-recommends -y iputils-ping \
    && apt install --no-install-recommends -y net-tools \
    && apt install --no-install-recommends -y telnet \
    && apt install --no-install-recommends -y htop  \
    && apt install --no-install-recommends -y curl  \
    && apt install --no-install-recommends -y zip  \
    && apt install --no-install-recommends -y unzip \
    && echo done

WORKDIR /opt/mibiao

COPY --from=python3 /opt/mibiao/dist /opt/mibiao/dist

RUN python -m pip install --no-cache-dir /opt/mibiao/dist/*.whl && rm -rf /opt/mibiao/dist


# docker build -f Dockerfile -t mibiao .

# docker run --rm -it mibiao bash
