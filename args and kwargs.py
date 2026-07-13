# def print_users(*names):
#     for i, name in enumerate(names, start=1):
#         print(f'{i}. {name}')
#
# print_users('Alice', 'Bob', 'Carol')

# def total(*args):
#     return sum(args)
#
# print(total(a = 1, b = 2))


# def describe_request(**kwargs):
#     for key, value in kwargs.items():
#         print(f"  {key}: {value}")
#
# describe_request(method="POST", url="/users", timeout=5)


# def build_headers(**kwargs):
#     return dict(kwargs)
#
# headers = build_headers(content_type='application/json', authorization='Bearer token123')
# print(headers)


# def broken(**kwargs, *args):
#     pass


def wrapper(*args, **kwargs):
    print("до вызова")
    result = target(*args, **kwargs)
    print("после вызова")
    return result

def target(method, url, timeout=30):
    print(f"{method} {url} (timeout={timeout})")

wrapper("GET", "/users", timeout=5)