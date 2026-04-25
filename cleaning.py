import pandas as pd

def enrich_data():
    df = pd.read_csv('kaspi_8_columns.csv')
    
    # 1. Чистим цену
    df['Price'] = pd.to_numeric(df['Текущая цена'].astype(str).str.replace(r'\D', '', regex=True), errors='coerce').fillna(0)
    
    # 2. Вытаскиваем МАТЕРИАЛ (Золото, Серебро, Сплав)
    def detect_material(text):
        text = str(text).lower()
        if 'золото' in text or 'brilliant' in text: return 'Luxury (Gold/Gem)'
        if 'серебро' in text: return 'Silver'
        if 'сплав' in text or 'бижутерный' in text or 'латунь' in text: return 'Fashion (Alloy)'
        return 'Other/Not Specified'
    
    df['Material'] = df['Название'].apply(detect_material)

    # 3. Вытаскиваем ТИП ИЗДЕЛИЯ
    def detect_type(text):
        text = str(text).lower()
        if 'зажим' in text: return 'Clip'
        if 'гребень' in text: return 'Comb'
        if 'диадема' in text or 'корона' in text: return 'Tiara'
        if 'заколка' in text: return 'Hairpin'
        return 'Accessory'

    df['Type'] = df['Название'].apply(detect_type)

    # 4. Вытаскиваем БРЕНД (первое слово)
    df['Brand'] = df['Название'].apply(lambda x: str(x).split()[0].upper())

    df.to_csv('kaspi_smart_data.csv', index=False, encoding='utf-8-sig')
    print("Данные обогащены! Теперь есть Material, Type и Brand.")

enrich_data()