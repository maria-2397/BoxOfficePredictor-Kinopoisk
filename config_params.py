"""
Конфигурационный модуль, содержащий словари параметров для API запросов к Кинопоиску.
"""

# Словарь для парсинга фильмов для главной таблицы
params_movies_main = {
    'selectFields': [
        'id',
        'name',
        'enName',
        'year',
        'type', 
        'rating',
        'votes.await',
        'votes.imdb',
        'votes.kp',
        'votes.filmCritics',
        'movieLength',
        'ratingMpaa',
        'ageRating',
        'genres',
        'countries',
        'persons',
        'budget',
        'fees',
        'videos',
        'premiere',
        'similarMovies',
        'sequelsAndPrequels',
        'watchability',
        'audience.russia'
    ],
    'year': ['2000-2023'],  # Год выхода фильма 
    'type': ['movie', 'cartoon'],  # тип картины мультфильм или фильм
    'limit': '250',
    'votes.kp': '2000-20000000',  # количество оценок на Кинопоиске не менее 2000
    'isSeries': 'false',  # Не сериал
    'name': '!null',
    'fees.usa': '!null',
}

# Словарь для парсинга фильмов, в которых участвовали персоны 
params_movies_additional = {
    'selectFields': [
        'id',
        'name',
        'enName',
        'year',
        'type',  
        'shortDescription',
        'slogan',
        'rating',
        'votes.await',
        'votes.imdb',
        'votes.kp',
        'votes.filmCritics',
        'movieLength',
        'ratingMpaa',
        'ageRating',
        'videos',
        'genres',
        'countries',
        'persons',
        'budget',
        'fees',
        'premiere',
        'similarMovies',
        'sequelsAndPrequels',
        'watchability',
        'audience.russia',
        'seasonsInfo.episodesCount',
        'seasonsInfo.number',
        'seriesLength',
        'totalSeriesLength'
    ],
    'limit': '250',
    'votes.kp': '2000-20000000'  # количество оценок на Кинопоиске не менее 2000
}

# Словарь для парсинга персон - актеров, режиссеров, сценаристов
params_persons = {
    'selectFields': [
        'id',
        'enName',
        'name',
        'age',
        'death',
        'countAwards',
        'movies.id',
        'movies.name',
        'movies.rating',
        'movies.enProfession',
    ],
    'limit': '250'
}