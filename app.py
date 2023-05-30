from adindex import all_ad_index


def handler():
    all_ad_index()
    return "Hello World!"

if __name__ == '__main__':
    handler()