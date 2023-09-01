#!/bin/bash

# SPDX-FileCopyrightText: 2023 UnionTech Software Technology Co., Ltd.

# SPDX-License-Identifier: GPL-2.0-only
# pylint: disable=C0114
tag=$(echo "$(cat ./CURRENT | grep "tag = ")" | cut -d "=" -f2 | python3 -c "s=input();print(s.strip())")

ROOT_DIR=`pwd`
config_pwd=$(cat ./setting/globalconfig.ini | grep "PASSWORD = ")
PASSWORD=$(echo "${config_pwd}" | cut -d "=" -f2 | python3 -c "s=input();print(s.strip())")
DISPLAY_SERVER=$(cat ~/.xsession-errors | grep XDG_SESSION_TYPE | head -n 1 | cut -d "=" -f2)
flag_feel="\n**** (・_・) ****\n"
whitelist="/usr/share/deepin-elf-verify/whitelist"
pypi_mirror="https://pypi.tuna.tsinghua.edu.cn/simple"
echo "${PASSWORD}" | sudo -S su  > /dev/null 2>&1


sources_list(){
cat > "sources.list" <<- EOF
deb [by-hash=force] https://professional-packages.chinauos.com/desktop-professional eagle main contrib non-free
deb-src https://professional-packages.chinauos.com/desktop-professional eagle main contrib non-free
deb http://pools.corp.deepin.com/ppa/dde-eagle eagle main contrib non-free
deb-src http://pools.corp.deepin.com/ppa/dde-eagle eagle main contrib non-free
deb http://pools.corp.deepin.com/ppa/dde-eagle experimental main contrib non-free
EOF
}

community_sources_list(){
cat > "sources.list" <<- EOF
deb https://community-packages.deepin.com/deepin apricot main contrib non-free
EOF
}

#install_wayland_depends(){
# libkf5wayland-dev经常出现依赖关系问题，尝试修复依赖关系，
# 但此举可能引入兼容性问题。
#/usr/bin/expect << EOF
#set timeout -1
#spawn sudo aptitude install libkf5wayland-dev
#expect {
#        "是否接受该解决方案" { send "N\n"}
#}
#expect {
#        "是否接受该解决方案" { send "Y\n" }
#}
#expect {
#        "您要继续吗" { send "Y\n" }
#}
#expect eof
#EOF
#}

check_status(){
    if [ $? = 0 ]; then
        echo -e "$1\t安装成功 √"
    else
        echo -e "$1\t安装失败 ×"
        env_retry=true
        cat /tmp/env.log
    fi
}

wayland_env(){
    echo -e "${flag_feel}安装 Wayland 上键鼠工具\n"
    deb_array=(g++ build-essential cmake qt5-default qt5-qmake libqt5gui5 libqt5core5a)
    for deb in ${deb_array[*]}
    do
        sudo apt install -y ${deb} > /tmp/env.log 2>&1
        check_status ${deb}
        apt policy ${deb} > /tmp/_yqdebversion.txt 2>&1
        cat /tmp/_yqdebversion.txt | grep "已安装"
    done
    sudo apt install -y libkf5wayland-dev > /tmp/env.log 2>&1
    check_status libkf5wayland-dev
    # libkf5wayland-dev 可能存在依赖报错，解决方法：
    # 方案一.添加镜像对应的ppa仓库源，重新执行；
    # 方案二.sudo aptitude install libkf5wayland-dev,先输 n,再输 y,再输 y
    # 方案二可能引入兼容性问题，慎用。
    # if [ $? != 0 ]; then
    #     install_wayland_depends
    # fi
    # 编译工具
    cd ${ROOT_DIR}/src/depends/wayland_autotool/
    mkdir -p build && cd build
    cmake .. > /dev/null 2>&1
    make -j4 > /dev/null 2>&1
    sudo make install > /dev/null 2>&1
    [ $? = 0 ] && tool_status="成功 √" || tool_status="失败 ×"
    echo -e "${flag_feel}wayland_autotool 安装${tool_status}"
    # 添加一下wayland下有用的环境变量，其实框架执行的时候底层也会自动判断并添加，这里咱们先打个提前量；
    cat $HOME/.bashrc | grep 'export GDMSESSION=Wayland' > /dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo "export QT_WAYLAND_SHELL_INTEGRATION=kwayland-shell" >> $HOME/.bashrc
        echo "export XDG_SESSION_DESKTOP=Wayland" >> $HOME/.bashrc
        echo "export XDG_SESSION_TYPE=wayland" >> $HOME/.bashrc
        echo "export WAYLAND_DISPLAY=wayland-0" >> $HOME/.bashrc
        echo "export GDMSESSION=Wayland" >> $HOME/.bashrc
        echo 'export DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus"' >> $HOME/.bashrc
    fi
    # 将 wayland_autotool 写入到安全管控白名单
    wayland_cmd_path="/usr/local/bin/wayland_autotool"
    result=`sudo cat ${whitelist} | grep ${wayland_cmd_path}`
    if [ -z "$result" ]; then
        sudo sed -i '$a\'"${wayland_cmd_path}"'' ${whitelist} && echo "wayland_autotool 白名单已写入 ${whitelist}" || echo "白名单设置失败"
        sudo systemctl restart deepin-elf-verify.service || true

    else
        echo "wayland_autotool 白名单已写入 ${whitelist}"
    fi

    if [ ! -f "$HOME/.Xauthority" ]; then
        touch $HOME/.Xauthority
    fi

    nohup wayland_autotool > /dev/null 2>&1 &
}

env_retry=false

system_env(){
    # 添加一些有用的环境变量
    echo "${PASSWORD}" | sudo -S su  > /dev/null 2>&1
    sudo sed -i "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/g" /etc/ssh/sshd_config > /dev/null 2>&1
    sudo sed -i "s/#   StrictHostKeyChecking ask/   StrictHostKeyChecking no/g" /etc/ssh/ssh_config  > /dev/null 2>&1
    cat $HOME/.bashrc | grep 'export DISPLAY=":0"' > /dev/null 2>&1
    if [ $? -ne 0 ]; then
         echo 'export DISPLAY=":0"' >> $HOME/.bashrc
         echo 'export QT_QPA_PLATFORM=' >> $HOME/.bashrc
         echo 'export QT_ACCESSIBILITY=1' >> $HOME/.bashrc
         echo 'export QT_LINUX_ACCESSIBILITY_ALWAYS_ON=1' >> $HOME/.bashrc
    fi
    source $HOME/.bashrc

    sudo rm -rf /usr/local/lib/python3.7/dist-packages/*.pth
    echo "cd ${ROOT_DIR}/src/depends/sniff/;python3 sniff" | sudo tee /usr/bin/sniff > /dev/null 2>&1
    sudo chmod +x /usr/bin/sniff

    gsettings set org.gnome.desktop.interface toolkit-accessibility true  > /dev/null 2>&1
    sudo systemctl enable ssh  > /dev/null 2>&1
    sudo systemctl start ssh  > /dev/null 2>&1
}
