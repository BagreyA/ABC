FROM golang:1.20 AS builder

WORKDIR /app

# Копируем go.mod и go.sum (если есть) для установки зависимостей
COPY go.mod go.sum ./
RUN go mod download

# Копируем остальной код
COPY . .

# Компилируем приложение
RUN go build -o myapp

# Используем минимальный образ для запуска приложения
FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/myapp .

CMD ["./myapp"]
