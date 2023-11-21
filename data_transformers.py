"""
Модуль для преобразования и обработки данных из API.

Данный модуль содержит функции, предназначенные для извлечения,
обработки и преобразования данных из API в структурированный формат.

Функции в модуле:
- get_persons: извлекает информацию о профессиях и идентификаторах персон.
- get_fees: извлекает информацию о сборах фильма.
- get_watchability: извлекает информацию о доступности просмотра фильма.
- get_videos: извлекает информацию о видео, связанных с фильмом.
- get_movies: преобразует JSON-данные о фильмах в список словарей.
- make_persons_movies_dict: создает словарь, связывающий персон и фильмы, в которых они участвовали.
"""

from typing import List, Dict, Optional, Union, Any


def get_persons(persons: List[Dict[str, Union[str, int]]]) -> Dict[str, List[Union[str, int]]]:
    """
    Получает информацию о профессиях персон и их идентификаторах.

    Параметры:
    - persons (List[Dict[str, Union[str, int]]]): список словарей, содержащих информацию о персонах.

    Возвращает:
    - Dict[str, List[Union[str, int]]]: словарь с профессиями в качестве ключей и списками имен/идентификаторов в качестве значений.
    """
    professions = [person['profession'] for person in persons]
    persons_dict = {profession: [] for profession in set(professions)}
    persons_id_dict = {profession + "_id": []
                       for profession in set(professions)}

    for person in persons:
        persons_dict[person['profession']].append(person['name'])
        persons_id_dict[person['profession'] + "_id"].append(person.get('id'))

    persons_dict.update(persons_id_dict)
    return persons_dict


def get_fees(key: str, fees_data: Optional[Dict[str, str]]) -> Dict[str, str]:
    """
    Извлекает информацию о сборах фильма.

    Параметры:
    - key (str): ключ для поиска в fees_data.
    - fees_data (Optional[Dict[str, str]]): данные о сборах.

    Возвращает:
    - Dict[str, str]: словарь с информацией о сборах.
    """
    if fees_data and key in fees_data:
        return {
            f'fees_{key}': str(fees_data[key].get('value', '')),
            f'fees_{key}_currency': str(fees_data[key].get('currency', ''))
        }
    return {}


def get_watchability(movie: Dict[str, Any]) -> List[str]:
    """
    Извлекает информацию о доступности просмотра фильма.

    Параметры:
    - movie (Dict[str, Any]): словарь с данными о фильме.

    Возвращает:
    - List[str]: список платформ для просмотра.
    """
    watchability = movie.get('watchability', {})
    if watchability is None:
        return []

    items = watchability.get('items')
    if items is None:
        return []

    return [watch['name'] for watch in items if 'name' in watch]


def get_videos(current_movie: Dict[str, Any]) -> Dict[str, Union[int, List[str]]]:
    """
    Извлекает информацию о видео, связанных с фильмом.

    Параметры:
    - current_movie (Dict[str, Any]): словарь с данными о фильме.

    Возвращает:
    - Dict[str, Union[int, List[str]]]: словарь с информацией о видео.
    """
    video_data = {}
    for video_type, video_list in (current_movie.get('videos')
                                   or {}).items():
        video_urls = [video['url'] for video in video_list]
        video_sites = [video['site'] for video in video_list]
        video_data['videos_' + video_type + '_number'] = len(
            set(video_urls))
#         video_data['videos_' + video_type + '_sites'] = list(
#             set(video_sites))
    return video_data


def get_movies(movies_json: List[Dict[str, Any]]) -> List[Dict[str, Union[str, int, List[str]]]]:
    """
    Преобразует JSON-данные о фильмах в список словарей.

    Параметры:
    - movies_json (List[Dict[str, Any]]): JSON-данные о фильмах.

    Возвращает:
    - List[Dict[str, Union[str, int, List[str]]]]: список словарей с данными о фильмах.
    """
    movies_dicts = []

    for movie in movies_json:
        data = {
            'movie_id': movie.get('id'),
            'movie_name': movie.get('name'),
            'year': movie.get('year'),
            'votes_kp': movie.get('votes', {}).get('kp'),
            'votes_imdb': movie.get('votes', {}).get('imdb'),
            'votes_filmCritics': movie.get('votes', {}).get('filmCritics'),
            'votes_await': movie.get('votes', {}).get('await'),
            'rating_kp': movie.get('rating', {}).get('kp'),
            'rating_imdb': movie.get('rating', {}).get('imdb'),
            'rating_filmCritics': movie.get('rating', {}).get('filmCritics'),
            'movieLength': movie.get('movieLength'),
            'ageRating': movie.get('ageRating'),
            'ratingMpaa': movie.get('ratingMpaa'),
            'type': movie.get('type'),
#             'seasonsInfo': movie.get('seasonsInfo', []),
#             'seriesLength': movie.get('seriesLength'),
#             'totalSeriesLength': movie.get('totalSeriesLength'),

            'genres': [genre['name'] for genre in movie.get('genres', [])],
            'countries': [
                country['name'] for country in movie.get('countries', [])
            ],
#             'watchability': get_watchability(movie),
#             'similarMovies_ids': [
#                 similarMovie['id']
#                 for similarMovie in movie.get('similarMovies', [])
#             ],
#             'similarMovies_names': [
#                 similarMovie['name']
#                 for similarMovie in movie.get('similarMovies', [])
#             ],
#             'seq_preqs_ids': [
#                 seq_preq.get('id')
#                 for seq_preq in movie.get('sequelsAndPrequels', [])
#                 if seq_preq.get('id')],

#             'seq_preqs_names': [
#                 seq_preq['name']
#                 for seq_preq in movie.get('sequelsAndPrequels', [])
#             ]
        }

        data.update(get_persons(movie.get('persons', [])))

#         data.update(
#             {f'premiere_{k}': v
#              for k, v in movie.get('premiere', {}).items()})

        data.update(get_fees('world', movie.get('fees')))
        data.update(get_fees('usa', movie.get('fees')))
        data.update(get_fees('russia', movie.get('fees')))

        audience_data = {
            f'audience_{a["country"]}': a['count']
            for a in movie.get('audience', [])
        }
        data.update(audience_data)

        if budget := movie.get('budget'):
            data['budget'] = str(budget.get('value', ''))
            data['budget_currency'] = str(budget.get('currency', ''))

        data.update(get_videos(movie))

        movies_dicts.append(data)

    return movies_dicts


def make_persons_movies_dict(persons: List[Dict[str, Any]]) -> List[Dict[str, Union[str, int]]]:
    """
    Создает словарь, связывающий персон и фильмы, в которых они участвовали.

    Параметры:
    - persons (List[Dict[str, Any]]): список словарей с данными о персонах.

    Возвращает:
    - List[Dict[str, Union[str, int]]]: список словарей, связывающий персон и фильмы.
    """
    data = []

    for person in persons:
        base_data = {
            'person_id': person.get('id'),
            'person_name': person.get('name'),
            'age': person.get('age'),
            'countAwards': person.get('countAwards'),
            'death': person.get('death')
        }

        person_movies = person.get('movies')

        if person_movies:
            for movie in person_movies:
                movie_data = {
                    'movie_id': movie.get('id'),
                    'movie_name': movie.get('name'),
                    'movie_rating': movie.get('rating'),
                    'movie_profession': movie.get('enProfession')
                }
                data.append({**base_data, **movie_data})
        else:
            data.append(base_data)

    return data
