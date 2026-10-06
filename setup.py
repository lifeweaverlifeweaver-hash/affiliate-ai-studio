import os

# Структура на папките и файловете
structure = {
    "requirements.txt": """streamlit==1.38.0
requests==2.31.0
pandas==2.2.0
""",
    "README.md": """# AffiliateAI Studio 🚀

Затворена система за управление на афилейт линкове, генериране на AI видео сценарии на български език и автоматични еднопродуктови фунии за продажби.

## Технологичен стек
- Python & Streamlit
- SQLite
- HTML/CSS Sales Funnels
""",
    "modules/__init__.py": "",
    "modules/database.py": """import sqlite3

DB_NAME = "affiliate_studio.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            affiliate_link TEXT NOT NULL,
            short_code TEXT UNIQUE NOT NULL,
            clicks INTEGER DEFAULT 0,
            ai_script TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_product(title, category, affiliate_link, short_code, ai_script=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO products (title, category, affiliate_link, short_code, ai_script)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, category, affiliate_link, short_code, ai_script))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def get_all_products():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, category, affiliate_link, short_code, clicks, ai_script FROM products")
    rows = cursor.fetchall()
    conn.close()
    return rows
""",
    "modules/ai_generator.py": """def generate_bulgarian_script(title, category):
    script = f\"\"\"Търсите ли перфектното решение в категорията '{category}'? 
Вижте това: {title}! 
Този продукт спестява време и решава вашите ежедневни проблеми бързо и лесно. 
Не пропускайте да разгледате детайлите и специалната оферта. 
Линкът за поръчка или проверка е в описанието по-долу!\"\"\"
    return script
""",
    "modules/funnel_builder.py": """def generate_funnel_html(title, category, short_code, ai_script):
    html_content = f\"\"<!DOCTYPE html>
<html lang=\"bg\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{title} | Специална оферта</title>
    <style>
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }}
        .container {{ max-width: 600px; margin: 40px auto; background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        h1 {{ color: #2c3e50; font-size: 26px; text-align: center; margin-bottom: 10px; }}
        .badge {{ display: block; text-align: center; background: #e0f2fe; color: #0369a1; padding: 6px 12px; border-radius: 20px; font-size: 14px; margin-bottom: 25px; width: fit-content; margin-left: auto; margin-right: auto; }}
        .video-box {{ background: #000; width: 100%; height: 320px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #fff; margin-bottom: 25px; font-size: 16px; }}
        .description {{ font-size: 16px; line-height: 1.6; color: #555; background: #f8fafc; padding: 20px; border-radius: 8px; margin-bottom: 25px; white-space: pre-line; }}
        .cta-button {{ display: block; width: 100%; background: #10b981; color: white; text-align: center; padding: 15px 0; border-radius: 8px; font-size: 18px; font-weight: bold; text-decoration: none; transition: background 0.3s; box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3); }}
        .cta-button:hover {{ background: #059669; }}
        .footer {{ text-align: center; font-size: 12px; color: #888; margin-top: 30px; }}
    </style>
</head>
<body>
    <div class=\"container\">
        <span class=\"badge\">Категория: {category}</span>
        <h1>{title}</h1>
        
        <div class=\"video-box\">
            🎬 [Видео презентация на продукта]
        </div>
        
        <div class=\"description\">
            {ai_script}
        </div>
        
        <a href=\"#\" class=\"cta-button\" target=\"_blank\">Вземи с отстъпка / Поръчай сега</a>
        
        <div class=\"footer\">
            <p>Тази страница е създадена автоматично чрез AffiliateAI Studio.</p>
        </div>
    </div>
</body>
</html>
\"\"\"
    return html_content
""",
    "app.py": """import streamlit as st
import random
import string
from modules.database import init_db, add_product, get_all_products
from modules.ai_generator import generate_bulgarian_script
from modules.funnel_builder import generate_funnel_html

init_db()

st.set_page_config(page_title="AffiliateAI Studio", page_icon="🚀", layout="wide")

st.title("🚀 AffiliateAI Studio")
st.markdown("Вашата затворена система за афилейт линкове, AI сценарии и еднопродуктови фунии за продажби.")

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Добавяне на продукт", 
    "🎬 AI Видео Студио", 
    "🚀 Фунии за продажби", 
    "📊 Аналитика и Линк Тракер"
])

with tab1:
    st.header("Добавяне на нов афилейт продукт")
    
    with st.form("product_form"):
        title = st.text_input("Име на продукта / услугата")
        category = st.selectbox("Категория", ["Физически стоки (Amazon/eMAG/ProfitShare)", "Дигитален софтуер / Услуги", "Онлайн курсове"])
        affiliate_link = st.text_input("Оригинален афилейт линк (с вашия референтен ID)")
        
        submitted = st.form_submit_button("Генерирай линк и AI сценарий")
        
        if submitted:
            if title and affiliate_link:
                short_code = ''.join(random.choices(string.ascii_lowercase + string.digits, k=5))
                ai_script = generate_bulgarian_script(title, category)
                
                success = add_product(title, category, affiliate_link, short_code, ai_script)
                if success:
                    st.success(f"Продуктът е добавен успешно! Кратък код: `{short_code}`")
                else:
                    st.error("Възникна грешка или кодът вече съществува. Опитайте отново.")
            else:
                st.warning("Моля, попълнете заглавието и афилейт линка.")

with tab2:
    st.header("🎬 Автоматизирано AI Видео Студио (Български език)")
    products = get_all_products()
    
    if not products:
        st.info("Все още няма добавени продукти. Добавете продукт от първия таб.")
    else:
        product_titles = [p[1] for p in products]
        selected_title = st.selectbox("Изберете продукт за видео сценарий", product_titles, key="video_select")
        
        selected_product = next(p for p in products if p[1] == selected_title)
        
        st.subheader("Генериран рекламен текст (Сценарий):")
        st.info(selected_product[6] if selected_product[6] else "Няма наличен сценарий.")
        
        if st.button("🔊 Генерирай гласово озвучаване и видео файл"):
            st.warning("Модулът за Text-to-Speech и видео рендване (MoviePy) е готов за интеграция тук!")
            st.balloons()

with tab3:
    st.header("🚀 Генератор на фунии за продажби (Sales Funnel)")
    products = get_all_products()
    
    if not products:
        st.info("Няма налични продукти за създаване на фуния.")
    else:
        product_titles = [p[1] for p in products]
        selected_title = st.selectbox("Изберете продукт за генериране на фуния", product_titles, key="funnel_select")
        
        selected_product = next(p for p in products if p[1] == selected_title)
        
        funnel_html = generate_funnel_html(
            title=selected_product[1],
            category=selected_product[2],
            short_code=selected_product[4],
            ai_script=selected_product[6]
        )
        
        st.subheader("Превю на маркетинговия текст във фунията:")
        st.text_area("HTML код на готовата фуния:", funnel_html, height=200)
        
        st.download_button(
            label="📥 Изтегли HTML файл на фунията",
            data=funnel_html,
            file_name=f"funnel_{selected_product[4]}.html",
            mime="text/html"
        )

with tab4:
    st.header("📊 Управление на линкове и статистики")
    products = get_all_products()
    
    if not products:
        st.info("Няма активни линкове за показване.")
    else:
        for p in products:
            col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
            with col1:
                st.markdown(f"**{p[1]}**")
                st.caption(f"Категория: {p[2]}")
            with col2:
                st.text(f"Оригинален: {p[3][:30]}...")
            with col3:
                st.markdown(f"Код: `{p[4]}`")
            with col4:
                st.metric("Кликове", p[5])
            st.divider()
"""
}

for filepath, content in structure.items():
    dir_name = os.path.dirname(filepath)
    if dir_name and not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("Готово! Всички файлове и папки на AffiliateAI Studio бяха създадени успешно.")
