## Debian 12 安装 Python3 及相关依赖软件

### 安装必备软件

    apt update && apt upgrade -y && apt install --no-install-recommends -y git

### 安装 Python3 相关软件

    apt install --no-install-recommends -y python3 python3-pip python3-venv

### 检查 Python3 是否安装成功

    python3 -V 