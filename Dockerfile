FROM python:3.12-slim-bookworm as python3
WORKDIR /mibiao_data
COPY ./src /mibiao_data/src
COPY ./pyproject.toml /mibiao_data/pyproject.toml
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

WORKDIR /mibiao_data

COPY --from=python3 /mibiao_data/dist /mibiao_data/dist

RUN python -m pip install --no-cache-dir /mibiao_data/dist/*.whl && rm -rf /mibiao_data/dist


# docker build -f Dockerfile -t mibiao .

# docker run --rm -it mibiao bash
