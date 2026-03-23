import sys
sys.stdout.reconfigure(encoding="utf-8")

videos = [
 {"title": "동문 주변 맛집", "views": 128000, "likes": 4300, "saved": True},
 {"title": "응정 2학년의 하루 VLOG", "views": 54000, "likes": 1800, "saved": False},
 {"title": "GLC 동아리 홍보", "views": 210000, "likes": 9200, "saved": True},
 {"title": "응정 개강총회 3월 18일 18시 양푼이 주막", "views": 330000, "likes": 90000, "saved": False},
 {"title": "진로특강 3월 24일 11:30 이윤재관 801호", "views": 870000, "likes": 31300, "saved": True},]


if __name__ == "__main__":
#문제 1
    for video in videos:
        print(video["title"], video["views"])
#문제 2
    for popular in videos: 
        if popular["views"] > 100000:
            print(popular["title"])
#문제 3
    for well_received in videos:
        like_ratio = well_received["likes"] / well_received["views"] * 100
        print(well_received["title"], f"의 종아요율: {like_ratio:.2f}")
#문제 4
    saved_videos = []
    for saved in videos:
        if saved["saved"] == True:
            saved_videos.append(saved["title"])
    print(saved_videos)
#문제 5
    sums = 0
    for sum_views in videos:
        sums = sums + sum_views["views"]
    print(sums)
#문제 6
    most_views = [0]
    for most_popular in videos:
        if most_popular["views"] > int(most_views[0]):
         most_views.clear()
         most_views.append(most_popular["views"])
    print(most_views)
#문제 4 / B 
    saved_videos2 = [saved2["title"] for saved2 in videos if saved2["saved"]]
    print(saved_videos2)
#문제 5 / B
    print(sum(sum_views2["views"] for sum_views2 in videos))
#문제 6 / B 
    print(max(most_views2["views"] for most_views2 in videos))