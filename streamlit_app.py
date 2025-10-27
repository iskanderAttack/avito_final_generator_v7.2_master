# streamlit_app.py
import streamlit as st
import pandas as pd
import io
import random
import importlib
import traceback

st.set_page_config(page_title="Avito Generator v7.2", layout="wide")
st.title("Avito Final Generator v7.2 — Streamlit UI")

st.markdown("""
Интерфейс запуска генерации объявлений.
1. Выберите модели, города и опции фото.
2. Нажмите Generate — получите таблицу и скачиваемый xlsx.
""")

# ---------- Ленивый импорт основного модуля ----------
gen = None
gen_import_error = None

def get_gen_module():
    """Попытка импортировать основной генератор на момент использования."""
    global gen, gen_import_error
    if gen is None and gen_import_error is None:
        try:
            gen_mod = importlib.import_module("avito_final_generator_v7_2_master_full")
            gen = gen_mod
        except Exception as e:
            gen_import_error = e
    return gen, gen_import_error

# Попытка получить модуль. При ошибке выводим трассировку и останавливаем страницу.
gen, err = get_gen_module()
if err:
    st.error("Ошибка при загрузке основного модуля генератора. Подробности:")
    st.code(traceback.format_exc())
    st.stop()

# ---------- Интерфейс ----------
model_ids = list(gen.MODELS.keys())
display_map = {mid: gen.MODELS[mid]["display_name"] for mid in model_ids}

sel = st.multiselect(
    "Выберите модели (минимум 1)",
    options=[display_map[m] for m in model_ids],
    default=[display_map[model_ids[0]]]
)

# переведём выбранные отображаемые названия обратно в id
chosen_ids = [mid for mid in model_ids if display_map[mid] in sel]

st.sidebar.header("Фото-настройки")
photo_mode = st.sidebar.radio("Режим выборки фото", ("auto", "manual"))
photo_min = st.sidebar.number_input("Мин фото на объявление", min_value=1, max_value=20, value=7)
photo_max = st.sidebar.number_input("Макс фото на объявление", min_value=1, max_value=20, value=10)
cl_on = st.sidebar.checkbox("Добавлять cl (без фона)", value=False)
cl_pct = st.sidebar.slider("Макс доля cl %", 0, 50, 15)
np_on = st.sidebar.checkbox("Включать фото без префиксов (none)", value=True)
np_pct = st.sidebar.slider("Вероятность none (%):", 0, 100, 10)

photo_cfg = {
    "mode": "manual" if photo_mode == "manual" else "auto",
    "photo_min": int(photo_min),
    "photo_max": int(photo_max),
    "cl_on": cl_on,
    "cl_pct": int(cl_pct),
    "np_on": np_on,
    "np_pct": int(np_pct)
}

st.sidebar.header("Города и адреса")
cities = st.multiselect("Выберите города", options=gen.TOP_CITIES, default=gen.TOP_CITIES[:5])
expand_addresses = st.text_input("Расширение адресов (пример: Москва=3, Казань=2)", value="")

# ---------- Генерация ----------
if st.button("Generate"):
    if not chosen_ids:
        st.error("Выберите хотя бы одну модель.")
    else:
        per_map = {}
        if expand_addresses:
            for part in expand_addresses.split(","):
                if "=" in part:
                    k, v = part.split("=", 1)
                    try:
                        per_map[gen.normalize_city(k.strip())] = int(v.strip())
                    except Exception:
                        st.warning(f"Неверный формат для '{part}' — пропускаю.")

        try:
            addresses = gen.generate_addresses(cities, per_map if per_map else None, default_per_city=1)
        except Exception as e:
            st.error(f"Ошибка при генерации адресов: {e}")
            st.exception(e)
            st.stop()

        prefixes = gen.generate_smart_prefixes(chosen_ids)
        prefix_map = {mid: prefixes.get(mid, gen.MODELS[mid]["fam"].upper()) for mid in chosen_ids}

        rows = []
        counters = {mid: 1 for mid in chosen_ids}
        seen = set()

        for mid in chosen_ids:
            for addr in addresses:
                try:
                    def pair():
                        title = gen.make_title(mid)
                        desc = gen.assemble_description(mid, addr, use_emojis=True)
                        return title, desc

                    title, desc = gen.generate_unique(pair, seen, max_tries=40)
                    nid = f"{prefix_map[mid]}{counters[mid]:03d}"
                    counters[mid] += 1
                    urls = gen.pick_photos_for_model(mid, photo_cfg, rnd=random.Random())
                    rows.append([nid, addr, title, desc, gen.join_photo_urls(urls)])
                except Exception as e:
                    st.error(f"Ошибка при обработке модели {mid} для адреса '{addr}': {e}")
                    st.exception(e)

        if rows:
            df = pd.DataFrame(rows, columns=["ID", "Адрес", "Новый заголовок", "Новое описание", "ImageUrls"])
            st.success(f"Сгенерировано {len(df)} объявлений.")
            st.dataframe(df)

            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine="openpyxl")
            towrite.seek(0)
            st.download_button(
                "Скачать XLSX",
                data=towrite,
                file_name="output_avito_ads_v7.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Не удалось сгенерировать ни одной строки. См. ошибки выше.")
