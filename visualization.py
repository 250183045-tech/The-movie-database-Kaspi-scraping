import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import os

# Скрываем лишние предупреждения
import warnings
warnings.filterwarnings('ignore')

def generate_all():
    # 1. Загрузка и принудительная очистка
    if not os.path.exists('kaspi_8_columns.csv'):
        print("Файл kaspi_8_columns_FINAL.csv не найден!")
        return
    
    df = pd.read_csv('kaspi_8_columns.csv')
    
    # Чистим данные прямо здесь, чтобы точно не было ошибок с KeyError
    df['Price'] = pd.to_numeric(df['Текущая цена'].astype(str).str.replace(r'\D', '', regex=True), errors='coerce').fillna(0)
    df = df[df['Price'] > 0]
    
    # Feature Engineering (Добавляем недостающие колонки)
    df['Luxury_Index'] = df['Price'] / df['Price'].median()
    df['Brand'] = df['Название'].apply(lambda x: str(x).split()[0].upper())
    
    def get_mat(x):
        x = str(x).lower()
        if 'золото' in x or 'gold' in x: return 'Gold'
        if 'серебро' in x: return 'Silver'
        return 'Alloy'
    df['Material'] = df['Название'].apply(get_mat)

    def get_type(x):
        x = str(x).lower()
        if 'зажим' in x: return 'Clip'
        if 'гребень' in x: return 'Comb'
        if 'диадема' in x: return 'Tiara'
        return 'Hairpin'
    df['Type'] = df['Название'].apply(get_type)

    # Настройка стиля
    sns.set_theme(style="whitegrid")
    plt.rcParams['figure.figsize'] = (10, 6)

    # --- ГЕНЕРАЦИЯ 12 ГРАФИКОВ ---
    
    # 1. Bar Chart
    plt.figure(); sns.barplot(x='Material', y='Price', data=df); plt.title('Avg Price by Material'); plt.savefig('v1.png')
    
    # 2. Pie Chart
    plt.figure(); df['Material'].value_counts().plot.pie(autopct='%1.1f%%'); plt.title('Market Share'); plt.savefig('v2.png')
    
    # 3. Histogram
    plt.figure(); sns.histplot(df['Price'], bins=30, log_scale=True, kde=True); plt.title('Price Distribution'); plt.savefig('v3.png')
    
    # 4. Box Plot
    plt.figure(); sns.boxplot(x='Material', y='Price', data=df[df['Price'] < df['Price'].quantile(0.9)]); plt.title('Price Outliers'); plt.savefig('v4.png')
    
    # 5. Scatter Plot (Interactive)
    fig5 = px.scatter(df, x="Price", y="Material", color="Type", log_x=True, title="Price vs Material"); fig5.write_html("v5.html")
    
    # 6. Heatmap
    plt.figure(); sns.heatmap(df[['Price', 'Luxury_Index']].corr(), annot=True); plt.title('Correlation'); plt.savefig('v6.png')
    
    # 7. Treemap (Interactive)
    fig7 = px.treemap(df, path=['Material', 'Type'], values='Price', title="Market Hierarchy"); fig7.write_html("v7.html")
    
    # 8. Violin Plot
    plt.figure(); sns.violinplot(x='Type', y='Price', data=df[df['Price'] < 50000]); plt.title('Price Density'); plt.savefig('v8.png')
    
    # 9. Donut Chart
    fig9 = px.pie(df, names='Type', hole=0.5, title="Product Types"); fig9.write_html("v9.html")
    
    # 10. Count Plot
    plt.figure(); sns.countplot(y='Brand', data=df, order=df['Brand'].value_counts().iloc[:10].index); plt.title('Top 10 Brands'); plt.savefig('v10.png')
    
    # 11. Strip Plot
    plt.figure(); sns.stripplot(x='Material', y='Price', data=df, alpha=0.5); plt.title('Individual Prices'); plt.savefig('v11.png')
    
    # 12. DASHBOARD (4 in 1)
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    sns.barplot(ax=axes[0,0], x='Material', y='Price', data=df)
    sns.countplot(ax=axes[0,1], x='Type', data=df)
    sns.scatterplot(ax=axes[1,0], x='Price', y='Luxury_Index', data=df)
    df['Material'].value_counts().plot.pie(ax=axes[1,1])
    plt.tight_layout(); plt.savefig('v12_dashboard.png')

    plt.close('all')
    print("Готово! 12 графиков сохранены (v1-v12). Ошибок нет.")

if __name__ == "__main__":
    generate_all()
