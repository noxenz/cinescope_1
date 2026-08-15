"""Песочница. Запуск: python -m sandbox.playground"""
import sys

from pydantic import ConfigDict, ValidationError

from sandbox import payloads
from sandbox.models import Movie, MovieDetails, MoviesPage, TestUser, Card, CardType, TypeCard

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def title(text):
    print(f"\n{'=' * 15} {text} {'=' * 15}")

title("1. Один вызов разбирает всё дерево")
page = MoviesPage(**payloads.MOVIES_PAGE)

print("тип page.movies         :", type(page.movies).__name__)
print("тип page.movies[0]      :", type(page.movies[0]).__name__)
print("тип page.movies[0].genre:", type(page.movies[0].genre).__name__)
print("доступ через точку      :", page.movies[0].genre.name)
print(f"id жанра: {page.movies[0].genre.id}")  # Выведет None

title("2. Три уровня вложенности")
details = MovieDetails(**payloads.MOVIE_DETAILS)

print("фильм               :", details.name)
print("жанр (уровень 2)    :", details.genre.name)
print("автор отзыва (ур. 3):", details.reviews[0].user.fullName)
print("createdAt стал      :", type(details.createdAt).__name__)
print("location стал       :", repr(details.location))

title("3. Ошибка внутри вложенной модели")
try:
    MoviesPage(**payloads.BROKEN_TYPES)
except ValidationError as e:
    print(e)
    print("\nloc-кортежи:")
    for err in e.errors():
        print("   ", err["loc"], "->", err["type"])

title("4. Поломка на третьем уровне")
try:
    MovieDetails(**payloads.BROKEN_DEEP)
except ValidationError as e:
    for err in e.errors():
        print("   ", ".".join(str(p) for p in err["loc"]), "->", err["msg"])

title("5. Пропала вложенная модель")
try:
    MoviesPage(**payloads.MISSING_NESTED)
except ValidationError as e:
    for err in e.errors():
        print("   ", err["loc"], "->", err["msg"])

print(page.movies[1].genre.name)

title('6. TestUser без verified и banned')
user = TestUser(
    email='smthufj@gmail.com',
    fullName='Test User',
    password='password123321',
    passwordRepeat='password123321',
    roles=['USER']
)

print(f'verified: {user.verified}')
print(f'banned: {user.banned}')

print(user.model_dump())
print(user.model_dump_json())
print(user.model_dump_json(exclude_unset=True))
print(user.model_dump_json(exclude_none=True))

print("\n=============== Сравнение model_dump и model_dump_json ===============")
print("model_dump():")
print(user.model_dump())
print("\nТип roles в model_dump():", type(user.model_dump()['roles'][0]))

print("\nmodel_dump_json():")
print(user.model_dump_json())
print("\nТип roles в model_dump_json():", type(user.model_dump_json()))

title("6. extra: что делать с лишними полями")

print("-- ignore (по умолчанию) --")
p_ignore = MoviesPage(**payloads.WITH_EXTRA_FIELDS)
print("   объект создался, totalRevenue доступен?", hasattr(p_ignore, "totalRevenue"))

class MoviesPageAllow(MoviesPage):
    model_config = ConfigDict(extra="allow")

print("-- allow --")
p_allow = MoviesPageAllow(**payloads.WITH_EXTRA_FIELDS)
print("   model_extra          :", p_allow.model_extra)
print("   доступ .totalRevenue :", p_allow.totalRevenue)

class MoviesPageForbid(MoviesPage):
    model_config = ConfigDict(extra="forbid")

print("-- forbid --")
try:
    MoviesPageForbid(**payloads.WITH_EXTRA_FIELDS)
except ValidationError as e:
    for err in e.errors():
        print("   ", err["loc"], "->", err["msg"])

title("7. strict: запрещаем приведение типов")

class StrictMovie(Movie):
    model_config = ConfigDict(strict=True)

sample = dict(payloads.MOVIES_PAGE["movies"][0])
sample["price"] = "130"          # цена пришла строкой

print("-- lax --")
print("   price ->", Movie(**sample).price, type(Movie(**sample).price).__name__)

print("-- strict --")
try:
    StrictMovie(**sample)
except ValidationError as e:
    for err in e.errors():
        print("   ", err["loc"], "->", err["msg"])

title("8. strict=True для поля id")

# Проверяем, что MOVIES_PAGE разбирается с strict id
try:
    page_strict = MoviesPage(**payloads.MOVIES_PAGE)
    print("✅ MOVIES_PAGE успешно разобран")
    print(f"   ID первого фильма: {page_strict.movies[0].id} (тип: {type(page_strict.movies[0].id).__name__})")
except ValidationError as e:
    print("❌ Ошибка валидации:")
    for err in e.errors():
        print(f"   {err['loc']} -> {err['msg']}")

# Проверяем, что строка в id вызовет ошибку
print("\n-- Проверка со строковым id --")
bad_sample = dict(payloads.MOVIES_PAGE["movies"][0])
bad_sample["id"] = "110"  # строка вместо числа

try:
    Movie(**bad_sample)
except ValidationError as e:
    print("❌ Ошибка валидации для id='110':")
    for err in e.errors():
        print(f"   {err['loc']} -> {err['msg']}")

title("9. strict=True на всю модель Movie")

print("-- Проверка с первым фильмом из MOVIES_PAGE --")
sample = dict(payloads.MOVIES_PAGE["movies"][0])  # Берём первый фильм

try:
    StrictMovie(**sample)
except ValidationError as e:
    print("Ошибок:", len(e.errors()))
    for err in e.errors():
        print(f"   {'.'.join(str(p) for p in err['loc'])} -> {err['msg']}")

title('Проверка валидатора')
try:
    Card(pan="1111ABCD33334444", cvc="123")
except ValidationError as e:
    print(e)

print(CardType.VISA.value)

# title('Проверка model_validator')
# TypeCard(pan="ABC", cvc="1", card_type="MIR")

title('Проверка валидации повтора пароля TestUser')
TestUser(
    email='ewfe12313f@gmail.com',
    fullName='Grig Grog',
    password='qwertyuiop',
    passwordRepeat='qwertyuiop'
)

title('Проверка валидации почты TestUser')
try:
    TestUser(
        email='не-почта',
        fullName='Grig Grog',
        password='qwertyuiop',
        passwordRepeat='qwertyuiop'
    )
except ValidationError as e:
    print(e)

import requests

title('RANDOM')
AUTH_BASE_URL = 'https://auth.dev-cinescope.coconutqa.ru'
REGISTER = '/register'

def check_real_response():
    response = requests.post(
        f"{AUTH_BASE_URL}{REGISTER}",  # Собираем полный URL
        json={
            "email": "testkfgebhrjuwhkubwefkhi@example.com",
            "fullName": "Test User",
            "password": "SecurePass123",
            "passwordRepeat": "SecurePass123"
        }
    )
    print(f"Статус: {response.status_code}")
    print(response.json())

check_real_response()