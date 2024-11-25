FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    openssh-server \
    python3 \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Настройка пароля для пользователя ansible_user
RUN useradd -m ansible_user && \
    echo 'ansible_user:password' | chpasswd && \
    adduser ansible_user sudo && \
    mkdir /var/run/sshd && \
    echo "ansible_user ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Настройка SSH для разрешения доступа пользователю ansible_user
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config && \
    sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Открытие порта 22
EXPOSE 22

# Запуск SSH-сервера в фоне
CMD ["/usr/sbin/sshd", "-D"]
