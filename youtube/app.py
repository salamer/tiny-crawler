import requests
from leapcell import Leapcell, LeapcellField
import time
import logging
import datetime
import sys
import copy
import os
from flask import Flask, render_template, request, redirect
import random
app = Flask(__name__)

leapclient = Leapcell("https://leapcell.io", "xxx")
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

headers = {'Accept': 'application/json'}

key = os.environ.get("YOUTUBE_KEY", "")
if not key:
    raise Exception("YOUTUBE_KEY is not set")

category = {
    "1": "Film & Animation",
    "2": "Autos & Vehicles",
    "10": "Music",
    "15": "Pets & Animals",
    "17": "Sports",
    "18": "Short Movies",
    "19": "Travel & Events",
    "20": "Gaming",
    "21": "Videoblogging",
    "22": "People & Blogs",
    "23": "Comedy",
    "24": "Entertainment",
    "25": "News & Politics",
    "26": "Howto & Style",
    "27": "Education",
    "28": "Science & Technology",
    "29": "Nonprofits & Activism",
    "30": "Movies",
    "31": "Anime/Animation",
    "32": "Action/Adventure",
    "33": "Classics",
    "34": "Comedy",
    "35": "Documentary",
    "36": "Drama",
    "37": "Family",
    "38": "Foreign",
    "39": "Horror",
    "40": "Sci-Fi/Fantasy",
    "41": "Thriller",
    "42": "Shorts",
    "43": "Shows",
    "44": "Trailers",
}


def get_trends_video(region: str, category: str):
    url = "https://www.googleapis.com/youtube/v3/videos"
    response = requests.get(url, params={
        "part": "contentDetails",
        "chart": "mostPopular",
        "regionCode": region,
        "key": key,
        "videoCategoryId": category,
    })
    return response.json()


def get_video_info(id: str):
    url = "https://www.googleapis.com/youtube/v3/videos"
    response = requests.get(url, params={
        "part": "snippet",
        "id": id,
        "key": key
    })
    return response.json()


def get_region():
    url = "https://www.googleapis.com/youtube/v3/i18nRegions"
    response = requests.get(url, params={
        "part": "snippet",
        "key": key
    })
    return response.json()


def process_trends_video(region: str, category_id: str, region_name: str):
    now_dt = datetime.datetime.now() # TODAY
    now = datetime.datetime(now_dt.year, now_dt.month, now_dt.day)
    now_ts = time.mktime(now.timetuple())
    table = leapclient.table(
        "test1/youtube", table_id="1667928105347481600", field_type="name")

    count = table.select().where((LeapcellField("region") == region) & 
                                 (LeapcellField("category") == category[category_id]) & 
                                 (LeapcellField("retrieve_time") > now_ts)).count()
    if count >= 3:
        logging.info("Skip region %s, category %s", region, category[category_id])
        return

    trends = get_trends_video(region, category_id)
    if "items" not in trends:
        return
    if len(trends["items"]) == count:
        logging.info("Skip region %s, category %s", region, category[category_id])
        return
    
    images = []

    for item in trends["items"]:
        video_id = item["id"]
        video_info = get_video_info(video_id)
        time.sleep(1)
        if len(video_info["items"]) == 0:
            continue
        video_info = video_info["items"][0]
        response = requests.get(
            video_info["snippet"]["thumbnails"]["high"]["url"])
        if response.status_code != 200:
            logging.error("Failed to download image for video %s", video_id)
        images.append(copy.deepcopy(response.content))
        image = leapclient.upload(response.content)
        publishAt = datetime.datetime.strptime(
            video_info["snippet"]["publishedAt"], '%Y-%m-%dT%H:%M:%S%z')
        tags = []
        if "tags" in video_info["snippet"]:
            tags = video_info["snippet"]["tags"]
        table.upsert({
            "title": video_info["snippet"]["title"],
            "description": video_info["snippet"]["description"],
            "cover": image.raw(),
            "video_id": video_id,
            "publishAt": time.mktime(publishAt.timetuple()),
            "channel": video_info["snippet"]["channelTitle"],
            "tag": tags,
            "region": region_name,
            "category": category[category_id],
            "url": "https://www.youtube.com/watch?v=" + video_id,
            "retrieve_time": now_ts,
            "channelId": video_info["snippet"]["channelId"],
        }, on_conflict=["video_id", "retrieve_time", "region"])
    
    return trends

def retrieve():
    regions = get_region()
    for region in regions["items"]:
        for key in category.keys():
            # try:
            process_trends_video(region["snippet"]["gl"], key, region_name=region["snippet"]["name"])
            # except Exception as e:
            #     logger.error(
            #         "Failed to retrieve video for region %s, category %s", region["snippet"]["gl"], key)
            #     logger.error(e)
            time.sleep(1)

@app.route("/xx")
def xx():
    return {"qq":"xx"}

@app.route("/process_trends_video")
def process_trends_video_api():
    region = request.args.get("region")
    category_id = request.args.get("category_id")
    region_name = request.args.get("region_name")
    return process_trends_video(region, category_id, region_name)


@app.route("/retrieve")
def retrieve_api():
    regions = get_region()
    for region in regions["items"]:
        randint_val = random.randint(1, 100)
        if randint_val > 3:
            continue
        for key in category.keys():
            r = requests.get("https://test1-youtube.leapcell.app/process_trends_video", params={
                "region": region["snippet"]["gl"],
                "category_id": key,
                "region_name": region["snippet"]["name"]
            })
            print(r.json())

    return {"status": "ok"}

if __name__ == "__main__":
    # retrieve()
    app.run(port=5000, debug=True)
