# Avito Final Generator v7.2 (master)

Авито-генератор v7.2 — скрипт для автоматической генерации объявлений для Авито:
- вариативные заголовки и описания;
- блок «Характеристики» (тасуется с сохранением ключевых пунктов);
- вариативная «Комплектация» (элементы тасуются);
- CTA / доставка с привязкой к городу и мягкий апселл/кросселл;
- логика подбора фотографий по префиксам (lg, gb, skl, kr, osb) и ракурсам (fr, r, l, b, mkr, cl);
- экспорт в Excel (`output_avito_ads_v7.xlsx`).

## Файлы репозитория
- `avito_final_generator_v7_2_master_full.py` — основной генератор (основной скрипт).
- `streamlit_app.py` — веб-интерфейс на Streamlit.
- `requirements.txt` — зависимости Python.
- `README.md` — этот файл.
- `photo_links_filled_AVITO.csv` — (опционально) CSV с базой фото (если нужно заполнение ImageUrls).

> **ВНИМАНИЕ:** не храните в репозитории секретные ключи (Google service json и т.п.). Используйте Streamlit Secrets или переменные окружения.

---

## Установка и запуск локально

1. Клонируйте репозиторий:
```bash
git clone https://github.com/iskanderAttack/avito_final_generator_v7.2_master.git
cd avito_final_generator_v7.2_master
