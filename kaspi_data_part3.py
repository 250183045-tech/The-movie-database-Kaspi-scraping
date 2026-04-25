import asyncio
import pandas as pd
import random
from playwright.async_api import async_playwright
from rich.console import Console

console = Console()

async def semi_auto_scraper_pro():
    all_data = []
    seen_urls = set()
    
    async with async_playwright() as p:
        # Запускаем браузер
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(
            viewport={'width': 1280, 'height': 900}
        )
        page = await context.new_page()
        
        console.print("[bold green]🚀 ИНСТРУКЦИЯ:[/bold green]")
        console.print("1. В открывшемся окне зайди на kaspi.kz/shop/")
        console.print("2. Перейди в любую категорию украшений или одежды.")
        console.print("3. Просто листай страницы вниз и нажимай 'Следующая'.")
        console.print("[yellow]Я буду собирать 8 колонок данных автоматически![/yellow]\n")

        try:
            while True:
                # Проверяем, есть ли карточки на экране
                try:
                    await page.wait_for_selector(".item-card", timeout=2000)
                    cards = await page.query_selector_all(".item-card")
                    
                    new_items = 0
                    for card in cards:
                        # Собираем расширенные данные
                        item = await card.evaluate("""(node) => {
                            const title = node.querySelector('.item-card__name-link')?.innerText || "NA";
                            const url = node.querySelector('.item-card__name-link')?.href || "";
                            const currentPrice = node.querySelector('.item-card__prices-price')?.innerText.replace(/[^0-9]/g, '') || "0";
                            
                            // Ищем старую цену (обычно зачеркнутая)
                            const oldPriceRaw = node.querySelector('.item-card__prices-old-price')?.innerText || "";
                            const oldPrice = oldPriceRaw.replace(/[^0-9]/g, '') || currentPrice;
                            
                            // Считаем скидку в %
                            let discount = "0%";
                            if (oldPrice !== "0" && oldPrice !== currentPrice) {
                                const discVal = Math.round(((parseInt(oldPrice) - parseInt(currentPrice)) / parseInt(oldPrice)) * 100);
                                discount = discVal + "%";
                            }

                            const ratingClass = node.querySelector('.item-card__rating')?.className || "";
                            const reviews = node.querySelector('.item-card__rating-count')?.innerText.replace(/[^0-9]/g, '') || "0";
                            
                            // Категория из хлебных крошек или URL (попробуем вытащить из URL)
                            const pathParts = window.location.pathname.split('/');
                            const category = pathParts[pathParts.length - 2] || "unknown";

                            return {
                                "Название": title,
                                "Текущая цена": currentPrice,
                                "Старая цена": oldPrice,
                                "Скидка": discount,
                                "Рейтинг": ratingClass.includes('rating_') ? ratingClass.split('rating_')[1] : "0",
                                "Отзывы": reviews,
                                "Категория": category,
                                "Ссылка": url
                            };
                        }""")

                        if item["Ссылка"] not in seen_urls:
                            seen_urls.add(item["Ссылка"])
                            all_data.append(item)
                            new_items += 1
                    
                    if new_items > 0:
                        console.print(f"[cyan]✅ Поймал {new_items} новых товаров. Всего в базе: {len(all_data)}[/cyan]")
                        # Сохраняем в CSV
                        pd.DataFrame(all_data).to_csv('kaspi_8_columns.csv', index=False, encoding='utf-8-sig')
                
                except:
                    pass # Ждем, пока страница загрузится или ты перейдешь в категорию
                
                await asyncio.sleep(1.5) # Проверка каждые 1.5 сек

        except Exception as e:
            console.print(f"[red]Остановка: {e}[/red]")
        
        finally:
            if all_data:
                df = pd.DataFrame(all_data)
                df.to_csv('kaspi_8_columns_FINAL.csv', index=False, encoding='utf-8-sig')
                console.print(f"\n[bold green]Готово! Файл 'kaspi_8_columns_FINAL.csv' содержит {len(df)} строк по 8 колонок.[/bold green]")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(semi_auto_scraper_pro())