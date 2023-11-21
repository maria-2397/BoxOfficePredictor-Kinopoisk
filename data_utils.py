"""
Утилиты для обработки данных, включая функции для работы с пропущенными данными и функции для чтения/записи JSON файлов.
"""

import pandas as pd
import json
from typing import Any, Union


def check_missing(df: pd.DataFrame) -> pd.DataFrame:
    """
    Поиск пропусков в DataFrame и подсчет их в процентах.

    Параметры:
    - df (pd.DataFrame): Исходный DataFrame для анализа пропусков.

    Возвращает:
    - pd.DataFrame: DataFrame с количеством и процентом пропусков по каждой колонке.
        Если пропусков нет, возвращает DataFrame с сообщением "Нет пропусков!".
    """
    missing = df.isnull().sum()
    missing_percent = (missing / df.shape[0]) * 100

    missing_df = pd.DataFrame({
        'пропущенных_строк': missing,
        'процент_пропусков': missing_percent
    })

    missing_df['процент_пропусков'] = missing_df['процент_пропусков'].apply(
        lambda x: f"{x:.2f}%")

    missing_df = missing_df.loc[
        missing_df['пропущенных_строк'] > 0].sort_values(
            by='пропущенных_строк')

    if missing_df.empty:
        return pd.DataFrame({"Сообщение": ["Нет пропусков!"]})
    else:
        return missing_df
    

def open_json(name: str) -> Any:
    """
    Открывает и читает содержимое JSON файла.

    Параметры:
    - name (str): Путь к JSON файлу, который необходимо прочитать.

    Возвращает:
    - Any: Данные из JSON файла.
    """
    with open(name, 'r', encoding='utf-8') as file:
        return json.load(file)
    

def save_json(name: str, json_data: Any) -> None:
    """
    Сохраняет данные в формате JSON в файл.

    Параметры:
    - name (str): Путь к файлу, в который будут сохранены данные.
    - json_data (Any): Данные для сохранения.

    Возвращает:
    - None
    """
    with open(name, 'w', encoding='utf-8') as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)
