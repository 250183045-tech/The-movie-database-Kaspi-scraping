import pandas as pd

def run_deep_analysis():
    df = pd.read_csv('kaspi_smart_data.csv')
    
    # Убираем товары с нулевой ценой (ошибки скрапинга)
    df = df[df['Price'] > 0]

    print("\n" + "="*40)
    print("   РЕАЛЬНЫЙ АНАЛИЗ РЫНКА (EDA)   ")
    print("="*40)

    # 1. СТРУКТУРА ЦЕН ПО МАТЕРИАЛАМ (Самое важное)
    # Считаем, сколько товаров каждого вида и их среднюю цену
    mat_stats = df.groupby('Material')['Price'].agg(['count', 'mean', 'median']).sort_values('mean', ascending=False)
    print("\n[1] АНАЛИЗ МАТЕРИАЛОВ (Где деньги?):")
    print(mat_stats.round(0))

    # 2. ТИТАНЫ РЫНКА (Бренды)
    # Посмотрим, какие бренды самые дорогие, а какие самые массовые
    brand_analysis = df.groupby('Brand')['Price'].agg(['count', 'mean']).sort_values('count', ascending=False).head(10)
    print("\n[2] ТОП-10 БРЕНДОВ ПО ПРИСУТСТВИЮ:")
    print(brand_analysis.round(0))

    # 3. ГИПОТЕЗЫ (То, что нужно для отчета)
    print("\n[3] ПРОВЕРКА АНАЛИТИЧЕСКИХ ГИПОТЕЗ:")
    
    # Гипотеза 1: Золото занимает мизерную долю рынка, но концентрирует весь капитал.
    gold_share = (len(df[df['Material'] == 'Luxury (Gold/Gem)']) / len(df)) * 100
    gold_money_share = (df[df['Material'] == 'Luxury (Gold/Gem)']['Price'].sum() / df['Price'].sum()) * 100
    print(f"- Г1: Доля Luxury товаров: {gold_share:.1f}% от количества, но {gold_money_share:.1f}% от всей стоимости рынка.")

    # Гипотеза 2: Диадемы (Tiaras) — самый дорогой тип аксессуаров.
    type_prices = df.groupby('Type')['Price'].mean()
    most_expensive_type = type_prices.idxmax()
    print(f"- Г2: Самый дорогой тип изделия: {most_expensive_type} (средняя цена {type_prices.max():.0f} ₸).")

    # 4. ВЫБРОСЫ (IQR метод)
    Q1 = df['Price'].quantile(0.25)
    Q3 = df['Price'].quantile(0.75)
    IQR = Q3 - Q1
    outliers_count = len(df[df['Price'] > (Q3 + 1.5 * IQR)])
    print(f"\n[4] ВЫБРОСЫ:")
    print(f"- Найдено {outliers_count} аномально дорогих товаров. Это 'бриллиантовое ядро' твоего датасета.")

run_deep_analysis()