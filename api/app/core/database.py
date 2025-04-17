import pandas as pd
from app.config import Config
from loguru import logger


def load_data():
    """Загрузка данных из CSV."""
    try:
        df = pd.read_csv(Config.DATA_PATH, encoding='utf-8')
        df.fillna("", inplace=True)
        df["Отзывы"] = df["Отзывы"].astype(str)
        logger.success(f"Данные загружены ({len(df)} записей)")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        raise


def get_top_brands(flavor: str, limit: int = 5) -> list[dict]:
    """Топ брендов для указанного вкуса."""
    df = load_data()
    return (
        df[df["Вкус"].str.lower() == flavor.lower()]
        .sort_values("Рейтинг", ascending=False)
        .head(limit)
        .to_dict(orient="records")
    )


def get_top_flavors(brand: str, limit: int = 5) -> list[dict]:
    """Топ вкусов для указанного бренда."""
    df = load_data()
    return (
        df[df["Бренд"].str.lower() == brand.lower()]
        .sort_values("Рейтинг", ascending=False)
        .head(limit)
        .to_dict(orient="records")
    )