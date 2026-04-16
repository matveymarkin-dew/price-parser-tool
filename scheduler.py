import schedule
import time
from parser import PriceParser
from datetime import datetime

# Конфигурация
SEARCH_QUERIES = ["смартфон", "ноутбук", "наушники"]

BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"


def run_monitoring():
    """Запуск мониторинга цен"""
    print(f"\n{'=' * 80}")
    print(f"🕐 Запуск мониторинга: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 80}\n")

    for query in SEARCH_QUERIES:
        print(f"\n📦 Мониторинг: {query}")

        parser = PriceParser()
        parser.parse_wildberries(query)
        parser.parse_yandex_market(query)

        # Сохранение с временной меткой
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        parser.save_to_json(f"data/{query}_{timestamp}.json")
        parser.save_to_csv(f"data/{query}_{timestamp}.csv")

        # Отправка в Telegram
        if BOT_TOKEN != "YOUR_BOT_TOKEN":
            parser.send_to_telegram(BOT_TOKEN, CHAT_ID)

        time.sleep(5)  # Задержка между запросами

    print(f"\n✅ Мониторинг завершен: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")


def main():
    print("🤖 Автоматический мониторинг цен запущен")
    print("=" * 80)
    print("Товары для мониторинга:")
    for i, query in enumerate(SEARCH_QUERIES, 1):
        print(f"  {i}. {query}")
    print("\nРасписание: каждый день в 09:00 и 18:00")
    print("Нажмите Ctrl+C для остановки")
    print("=" * 80)

    # Настройка расписания
    schedule.every().day.at("09:00").do(run_monitoring)
    schedule.every().day.at("18:00").do(run_monitoring)

    # Запуск сразу при старте
    run_monitoring()

    # Основной цикл
    while True:
        schedule.run_pending()
        time.sleep(60)  # Проверка каждую минуту


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⛔ Мониторинг остановлен пользователем")
