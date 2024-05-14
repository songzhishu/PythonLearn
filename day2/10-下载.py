# 我想下载网上的视频用python
import requests


def download_video(url, save_path):
    response = requests.get(url)
    with open(save_path, 'wb') as f:
        f.write(response.content)
        print("视频下载完成")


# 示例使用
video_url = "https://www.kanmaoyy.com/29f13380-cab8-4759-9f44-285735f5bc94"
save_path = "E:/test/test.mp4"

download_video(video_url, save_path)