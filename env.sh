#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
source ./_env_base.sh
echo "
 ██╗   ██╗  ██████╗      ███████╗ ███╗   ██╗ ██╗   ██╗
 ╚██╗ ██╔╝ ██╔═══██╗     ██╔════╝ ████╗  ██║ ██║   ██║
  ╚████╔╝  ██║   ██║     █████╗   ██╔██╗ ██║ ██║   ██║
   ╚██╔╝   ██║▄▄ ██║     ██╔══╝   ██║╚██╗██║ ╚██╗ ██╔╝
    ██║    ╚██████╔╝     ███████╗ ██║ ╚████║  ╚████╔╝
    ╚═╝     ╚══▀▀═╝      ╚══════╝ ╚═╝  ╚═══╝   ╚═══╝
    ${tag}
"

env(){
    sudo apt update

    deb_array=(
        python3-pip
        python3-tk
        sshpass
        scrot
        openjdk-8-jdk
        gir1.2-atspi-2.0
        libatk-adaptor
        at-spi2-core
        python3-opencv
    )
    # 裁剪基础环境
    cd ${ROOT_DIR}/src/utils
    BASICENV=$(python3 sub_env_cut.py)
    if [ "${BASICENV}" = "BASICENV" ]; then
        ENV_CUT_FLAG="cut"
        deb_array=(
            python3-pip
            sshpass
            openjdk-8-jdk
        )
    fi

    echo -e "${flag_feel}安装 deb 包\n"
    for deb in ${deb_array[*]}
    do
        sudo apt install -y ${deb} > /tmp/env.log 2>&1
        check_status ${deb}
    done

    if [ "${DISPLAY_SERVER}" = "wayland" ]; then
        wayland_env
    fi
}
env
if [ "${env_retry}" = "true" ]; then
    source /etc/os-release
    if [ "${NAME}" = "Deepin" ]; then
        community_sources_list
    else
        sources_list
    fi
    sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
    sudo cp sources.list /etc/apt/sources.list && rm -rf sources.list
    # 替换源之后再执行
    env
    sudo mv /etc/apt/sources.list.bak /etc/apt/sources.list
fi
echo -e "${flag_feel}安装 pip 包\n"

sudo pip3 config set global.timeout 10000 > /tmp/env.log 2>&1
sudo pip3 config set global.index-url ${pypi_mirror} > /tmp/env.log 2>&1
sudo pip3 config set global.extra-index-url https://it.uniontech.com/nexus/repository/pypi-public/simple
sudo pip3 install pipenv > /tmp/env.log 2>&1
if [ $? = 0 ]; then
    echo -e "pipenv\t安装成功 √"
else
    echo -e "pipenv\t安装失败 ×"
    cat /tmp/env.log
    exit 520
fi
cd ${ROOT_DIR}/
pipenv --python 3.7 > /tmp/env.log 2>&1
if [ $? != 0 ]; then
    echo -e "AT环境创建失败"
    exit 521
fi
python_virtualenv_path=$(pipenv --venv)
whitelist_path=`echo "${python_virtualenv_path}" | sed "s/\/home\/$USER\//\//"`
result=`sudo cat ${whitelist} | grep ${whitelist_path}`
if [ -z "$result" ]; then
    sudo sed -i '$a\'"${whitelist_path}"'' ${whitelist}
    sudo sed -i '$a\'"${python_virtualenv_path}"'' ${whitelist}
    sudo systemctl restart deepin-elf-verify.service || true
fi

py_debs=(
    python3-gi
    python3-pyatspi
    python3-dbus
    python3-cairo
    python3-pil
    python3-ptyprocess
    python3-pexpect
    python3-numpy
    python3-opencv
)
for pd in ${py_debs[*]}
do
    rm -rf ${pd}*
    apt download ${pd} > /tmp/env.log 2>&1
    if [ $? != 0 ]; then
        cat /tmp/env.log
        exit 520
    fi
    dpkg -x ${pd}*.deb ${pd}
    cp -r ./${pd}/usr/lib/python3/dist-packages/* ${python_virtualenv_path}/lib/python3.7/site-packages/
    rm -rf ${pd}*
done

apt download python3-gi-cairo > /tmp/env.log 2>&1
dpkg -x python3-gi-cairo*.deb python3-gi-cairo
cp -r ./python3-gi-cairo//usr/lib/python3/dist-packages/gi/* ${python_virtualenv_path}/lib/python3.7/site-packages/gi/
rm -rf python3-gi-cairo*

pip_array=(
    pyscreeze==0.1.28
    PyAutoGUI==0.9.53
    pytest==6.2.5
    pytest-rerunfailures==10.2
    pytest-timeout==2.1.0
    allure-pytest==2.9.45
    funnylog
    pdocr-rpc
    image-center
    allure-custom
    letmego
)

if [ "${ENV_CUT_FLAG}" = "cut" ]; then
    pip_array=(
        pytest==6.2.5
        pytest-rerunfailures==10.2
        pytest-timeout==2.1.0
        allure-pytest==2.9.45
        allure-custom
        funnylog
    )
fi

for p in ${pip_array[*]}
do
    pipenv run pip install ${p} -i ${pypi_mirror} > /tmp/env.log 2>&1
    check_status ${p}
    pip3 list | grep -v grep | grep ${p}
done
echo "${PASSWORD}" | sudo -S su > /dev/null 2>&1
cd ${ROOT_DIR}/src/utils/
requirements=$(python3 sub_depends.py)
if [ "${requirements}" != "" ]; then
    echo -e "\n应用库依赖:\n${requirements}\n"
    for requirement in ${requirements[*]}
    do
        echo -e "${flag_feel}安装应用库依赖: ${requirement}"
        pipenv run pip install -r ${requirement}
    done
fi
rm -rf Pipfile
echo "${python_virtualenv_path}"
pipenv run pip list
system_env
echo "pipenv run python \$*" | sudo tee /usr/bin/youqu > /dev/null 2>&1
sudo chmod +x /usr/bin/youqu
cd ${ROOT_DIR};youqu manage.py run -h
