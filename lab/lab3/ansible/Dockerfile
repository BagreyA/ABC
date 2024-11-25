FROM ubuntu:20.04

# Установка необходимых пакетов
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    openssh-server \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Создание необходимой директории
RUN mkdir /var/run/sshd

# Настройка пароля для пользователя root
RUN echo 'root:password' | chpasswd

# Разрешить вход по SSH
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Открытие порта 22
EXPOSE 22

# Запуск SSH-сервера в фоне
CMD ["/usr/sbin/sshd", "-D"]
