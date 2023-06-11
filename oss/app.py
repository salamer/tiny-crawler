import requests

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Referer": "https://ossinsight.io/",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
    'origin': 'https://ossinsight.io',
    'authority': 'api.ossinsight.io',
}

def get_collections():
    url = "https://api.ossinsight.io/collections"
    response = requests.get(url, headers=header)
    print(response.text, response.status_code)
    return response.json()

def get_collection(collection_id):
    url = "https://api.ossinsight.io/q/collection-stars-history-rank"
    response = requests.get(url, headers=header, params={
        "collectionId": collection_id,
    })
    print(response.text, response.status_code)
    return response.json()


if __name__ == "__main__":
    collections = get_collections()
    for collection in collections["data"]:
        get_collection(collection["id"])