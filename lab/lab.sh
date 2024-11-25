#!/bin/bash

get_os_info() {
    echo "ОС: $(uname -o)"
    echo "Версия: $(uname -v)"
    echo "Версия ядра: $(uname -r)"
    echo "Архитектура ядра: $(uname -m)"
}

get_cpu_info() {
    echo -e "\nИнформация о процессоре:"
    lscpu | grep "Model name" | sed 's/Model name:/Модель процессора:/'
    lscpu | grep "CPU MHz" | sed 's/CPU MHz:/Частота:/'
    lscpu | grep "^CPU(s)" | sed 's/CPU(s):/Количество ядер:/'
    echo "Размер кэш-памяти:"
    lscpu | grep "cache" | grep -v "Vulnerability"
}

get_memory_info() {
    echo -e "\nИнформация о размере оперативной памяти:"
    free -m | awk 'NR==2{printf "Доступный размер: %.2f MB\n", $7}'
    free -m | awk 'NR==2{printf "Общий размер ОП: %.2f MB\n", $2}'
    free -m | awk 'NR==2{printf "Использованный размер: %.2f MB\n", $3}'
}

get_network_info() {
    echo -e "\nСетевые интерфейсы:"
    for interface in $(ls /sys/class/net/); do
        # Проверяем, существует ли файл для MAC-адреса
        if [[ -f "/sys/class/net/$interface/address" ]]; then
            ip_addr=$(ip addr show $interface | grep "inet " | awk '{print $2}')
            mac_addr=$(cat /sys/class/net/$interface/address)
            # Проверяем, существует ли файл для скорости сети
            if [[ -f "/sys/class/net/$interface/speed" ]]; then
                speed=$(cat /sys/class/net/$interface/speed 2>/dev/null || echo "Неизвестно")
            else
                speed="Неизвестно"
            fi
            echo "Сетевой интерфейс: $interface"
            echo "IP адрес: ${ip_addr:-Неизвестно}"
            echo "MAC адрес: $mac_addr"
            echo "Скорость сети: ${speed} Mбит/с"
            echo ""
        fi
    done
}

get_disk_info() {
    echo -e "\nИнформация о системных разделах:"
    df -h --output=target,fstype,size,used,avail | tail -n +2 | while read line; do
        echo "Точка монтирования: $(echo $line | awk '{print $1}')"
        echo "Файловая система: $(echo $line | awk '{print $2}')"
        echo "Общий размер: $(echo $line | awk '{print $3}')"
        echo "Использовано: $(echo $line | awk '{print $4}')"
        echo "Свободно: $(echo $line | awk '{print $5}')"
        echo ""
    done
}

get_os_info
get_cpu_info
get_memory_info
get_network_info
get_disk_info



# Команды для проверки верности вывода 
# uname -a
# lscpu
# free -m
# ip addr show
# ethtool eth0 | grep "Speed"
# df -h