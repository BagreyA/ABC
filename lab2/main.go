// main.go
package main

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
    "time"
)

func main() {
    fmt.Println("Приложение запущено, ожидаем сигналы")

    // Создаем канал для сигналов
    signals := make(chan os.Signal, 1)
    signal.Notify(signals, syscall.SIGINT, syscall.SIGTERM)

    // Основной цикл работы
    go func() {
        for {
            fmt.Println("Работаю...")
            time.Sleep(2 * time.Second)
        }
    }()

    // Ожидание сигнала
    sig := <-signals
    fmt.Println("Получен сигнал:", sig)
    fmt.Println("Завершаем работу")
}
