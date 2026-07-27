# def multiply(a: int, b: int) -> int:
#     return a * b
#
# print(multiply('hero', 'storm'))

# def sum_numbers(numbers: list[int]) -> int:
#     return sum(numbers)
#
# print(sum_numbers(['one', 'two', 'three']))

# def find_user(user_id: int) -> str | None:
#     if user_id == 1:
#         return "Пользователь найден"
#     return None
#
# print(find_user(5))

def process_input(value: int | str) -> str:
    return f'Ты передал: {value}'

print(process_input(22))