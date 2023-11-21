"""
api_fetcher.py

Модуль, содержащий инструменты для извлечения данных из API.
В частности, предоставляет класс APIFetcher для выполнения запросов к API
и получения данных о фильмах и персонах.

"""

import logging
import requests
import time
from typing import List, Dict, Any
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


def split_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Разбивает список на части (chunks) заданного размера.

    Параметры:
    - lst (List[Any]): Исходный список.
    - chunk_size (int): Размер каждой части.

    Возвращает:
    - List[List[Any]]: Список из частей исходного списка.
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


class APIFetcher:
    def __init__(self, headers: Dict[str, str]):
        """
        Инициализатор класса APIFetcher.

        Параметры:
        - headers (Dict[str, str]): Заголовки для запроса.
        """
        self.headers = headers

    @retry(stop=stop_after_attempt(5),
           wait=wait_fixed(20),
           retry=retry_if_exception_type(requests.exceptions.ReadTimeout))
    def fetch_data(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет GET запрос к API и возвращает ответ в формате JSON.

        Параметры:
        - url (str): URL для запроса.
        - params (Dict[str, Any]): Параметры для запроса.

        Возвращает:
        - Dict[str, Any]: Ответ от API в формате JSON.
        """
        try:
            response = requests.get(url,
                                    params=params,
                                    headers=self.headers,
                                    timeout=60)
            response.raise_for_status()
            return response.json()
        except (requests.HTTPError, requests.exceptions.ReadTimeout) as e:
            logging.error(f"Ошибка при запросе: {e}")
            raise

    def get_json_docs(self, url: str,
                      params: Dict[str, Any],
                      ids_key: str,
                      ids_list: List[Any],
                      ids_chunk: int,
                      pause: int = 20) -> List[Dict[str, Any]]:
        """
        Загружает данные из API по частям, разбивая список IDs на меньшие части.

        Параметры:
        - url (str): URL для запроса.
        - params (Dict[str, Any]): Параметры для запроса.
        - ids_key (str): Ключ в словаре params для списков ID (фильмы или персоны).
        - ids_list (List[Any]): Список всех ID, информацию о которых нужно получить.
        - ids_chunk (int): Количество элементов в одной части при разбиении списка ID.
        - pause (int): Пауза между запросами в секундах.

        Возвращает:
        - List[Dict[str, Any]]: Список результатов от API для всех переданных ID.
        """

        def pause_requests(count: int) -> None:
            """Останавливает выполнение на определенное время каждые 5 запросов."""
            if count % 5 == 0:
                time.sleep(pause)

        # Разбиваем входной список ID на чанки (меньшие части).
        ids = split_list(ids_list, ids_chunk)
        total_chunks = len(ids)
        all_data = []

        request_count = 0

        # Итерация по каждому чанку
        for i, chunk in enumerate(ids, 1):
            # Обновляем параметры запроса текущим чанком ID
            params[ids_key] = chunk

            # Запись в лог процесса загрузки первой страницы для текущего чанка
            logging.info(f'Загрузка страницы 1 для chunk {i} из {total_chunks}...')

            request_count += 1
            pause_requests(request_count)

            # Получаем данные первой страницы
            params['page'] = '1'
            first_page_data = self.fetch_data(url, params)

            # Добавляем полученные данные в итоговый список
            all_data.extend(first_page_data['docs'])

            # Определяем общее количество страниц для текущего чанка ID
            total_pages = first_page_data['pages']

            # Итерация по каждой странице, начиная со второй
            for page in range(2, total_pages + 1):
                params['page'] = str(page)

                # Запись в лог процесса загрузки текущей страницы
                logging.info(f'Загрузка страницы {page} из {total_pages} для chunk {i} из {total_chunks}...')

                request_count += 1
                pause_requests(request_count)

                # Получаем данные текущей страницы
                page_data = self.fetch_data(url, params)

                # Добавляем полученные данные в итоговый список
                all_data.extend(page_data['docs'])

        logging.info('Загрузка завершена успешно!')
        return all_data
