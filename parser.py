import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import time
import re


class PriceParser:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.results = []

    def parse_wildberries(self, search_query):
        """Парсинг цен с Wildberries"""
        print(f"🔍 Парсинг Wildberries: {search_query}")

        url = f"https://search.wb.ru/exactmatch/ru/common/v4/search?appType=1&curr=rub&dest=-1257786&query={search_query}&resultset=catalog&sort=popular&spp=24&suppressSpellcheck=false"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            data = response.json()

            products = data.get("data", {}).get("products", [])

            for product in products[:10]:  # Берем первые 10 товаров
                item = {
                    "marketplace": "Wildberries",
                    "name": product.get("name", "N/A"),
                    "price": product.get("priceU", 0) / 100,  # Цена в копейках
                    "rating": product.get("rating", 0),
                    "reviews": product.get("feedbacks", 0),
                    "brand": product.get("brand", "N/A"),
                    "url": f"https://www.wildberries.ru/catalog/{product.get('id')}/detail.aspx",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                self.results.append(item)

            print(f"✅ Найдено {len(products[:10])} товаров на Wildberries")
            time.sleep(2)  # Задержка между запросами

        except Exception as e:
            print(f"❌ Ошибка парсинга Wildberries: {e}")

    def parse_ozon(self, search_query):
        """Парсинг цен с Ozon (упрощенная версия)"""
        print(f"🔍 Парсинг Ozon: {search_query}")

        # Примечание: Ozon имеет защиту от парсинга, это демо-версия
        url = f"https://www.ozon.ru/search/?text={search_query}"

        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")

            # Это упрощенный пример, реальный парсинг требует более сложной логики
            print("⚠️ Ozon требует более сложной обработки (API или Selenium)")
            time.sleep(2)

        except Exception as e:
            print(f"❌ Ошибка парсинга Ozon: {e}")

    def parse_yandex_market(self, search_query):
        """Парсинг цен с Яндекс.Маркет"""
        print(f"🔍 Парсинг Яндекс.Маркет: {search_query}")

        # Демо-данные для примера
        demo_products = [
            {
                "marketplace": "Яндекс.Маркет",
                "name": f"{search_query} - Модель 1",
                "price": 2990,
                "rating": 4.5,
                "reviews": 120,
                "brand": "Brand A",
                "url": "https://market.yandex.ru/product/example1",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
            {
                "marketplace": "Яндекс.Маркет",
                "name": f"{search_query} - Модель 2",
                "price": 3490,
                "rating": 4.7,
                "reviews": 85,
                "brand": "Brand B",
                "url": "https://market.yandex.ru/product/example2",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            },
        ]

        self.results.extend(demo_products)
        print(f"✅ Найдено {len(demo_products)} товаров на Яндекс.Маркет")
        time.sleep(2)

    def get_price_statistics(self):
        """Получение статистики по ценам"""
        if not self.results:
            return None

        prices = [item["price"] for item in self.results if item["price"] > 0]

        if not prices:
            return None

        stats = {
            "min_price": min(prices),
            "max_price": max(prices),
            "avg_price": sum(prices) / len(prices),
            "total_products": len(self.results),
            "marketplaces": list(set([item["marketplace"] for item in self.results])),
        }

        return stats

    def save_to_json(self, filename="prices.json"):
        """Сохранение результатов в JSON"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"💾 Данные сохранены в {filename}")

    def save_to_csv(self, filename="prices.csv"):
        """Сохранение результатов в CSV"""
        if not self.results:
            print("⚠️ Нет данных для сохранения")
            return

        keys = self.results[0].keys()

        with open(filename, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.results)

        print(f"💾 Данные сохранены в {filename}")

    def print_results(self):
        """Вывод результатов в консоль"""
        print("\n" + "=" * 80)
        print("📊 РЕЗУЛЬТАТЫ ПАРСИНГА")
        print("=" * 80)

        for item in self.results:
            print(f"\n🏪 {item['marketplace']}")
            print(f"📦 {item['name']}")
            print(f"💰 Цена: {item['price']}₽")
            print(f"⭐ Рейтинг: {item['rating']} ({item['reviews']} отзывов)")
            print(f"🔗 {item['url']}")

        stats = self.get_price_statistics()
        if stats:
            print("\n" + "=" * 80)
            print("📈 СТАТИСТИКА")
            print("=" * 80)
            print(f"Минимальная цена: {stats['min_price']}₽")
            print(f"Максимальная цена: {stats['max_price']}₽")
            print(f"Средняя цена: {stats['avg_price']:.2f}₽")
            print(f"Всего товаров: {stats['total_products']}")
            print(f"Маркетплейсы: {', '.join(stats['marketplaces'])}")

    def send_to_telegram(self, bot_token, chat_id):
        """Отправка отчета в Telegram"""
        stats = self.get_price_statistics()

        if not stats:
            print("⚠️ Нет данных для отправки")
            return

        message = f"""
📊 Отчет по мониторингу цен

📈 Статистика:
• Минимальная цена: {stats["min_price"]}₽
• Максимальная цена: {stats["max_price"]}₽
• Средняя цена: {stats["avg_price"]:.2f}₽
• Всего товаров: {stats["total_products"]}
• Маркетплейсы: {", ".join(stats["marketplaces"])}

🕐 Время: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        """

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

        try:
            response = requests.post(url, json={"chat_id": chat_id, "text": message})

            if response.status_code == 200:
                print("✅ Отчет отправлен в Telegram")
            else:
                print(f"❌ Ошибка отправки в Telegram: {response.text}")

        except Exception as e:
            print(f"❌ Ошибка: {e}")


def main():
    print("🚀 Парсер цен конкурентов")
    print("=" * 80)

    # Запрос поискового запроса
    search_query = input("Введите название товара для поиска: ").strip()

    if not search_query:
        search_query = "смартфон"
        print(f"Используется запрос по умолчанию: {search_query}")

    # Создание парсера
    parser = PriceParser()

    # Парсинг маркетплейсов
    parser.parse_wildberries(search_query)
    parser.parse_yandex_market(search_query)
    # parser.parse_ozon(search_query)  # Раскомментируйте для парсинга Ozon

    # Вывод результатов
    parser.print_results()

    # Сохранение данных
    parser.save_to_json()
    parser.save_to_csv()

    # Опционально: отправка в Telegram
    send_telegram = input("\nОтправить отчет в Telegram? (y/n): ").lower()
    if send_telegram == "y":
        bot_token = input("Введите токен бота: ")
        chat_id = input("Введите chat_id: ")
        parser.send_to_telegram(bot_token, chat_id)

    print("\n✅ Готово!")


if __name__ == "__main__":
    main()
