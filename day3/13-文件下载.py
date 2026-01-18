import os
import sys
import random
import string

import yt_dlp


def generate_random_filename(length=16, ext="mp4"):
    """
    生成随机文件名
    参数:
        length: 随机字符长度（默认16位）
        ext: 文件扩展名（默认mp4）
    返回:
        随机文件名，如 "a897b23c987d1234.mp4"
    """
    # 随机字符集：字母+数字，避免特殊字符导致路径问题
    chars = string.ascii_lowercase + string.digits
    # 生成随机字符串
    random_str = ''.join(random.choice(chars) for _ in range(length))
    # 拼接文件名
    return f"{random_str}.{ext}"


def download_video(video_url, save_path=r"E:\DL", quality="best"):
    """
    根据视频链接下载视频

    参数:
        video_url (str): 视频的网络链接
        save_path (str): 视频保存的文件夹路径，默认是E盘的DL文件夹
        quality (str): 视频质量，可选值有 "best" (最佳质量), "worst" (最差质量), "720p", "1080p" 等
    """
    # 确保保存目录存在
    if not os.path.exists(save_path):
        os.makedirs(save_path)
        print(f"✅ 已自动创建保存目录: {save_path}")

    # 生成随机文件名（核心修改点）
    random_filename = generate_random_filename()
    # 拼接最终保存路径
    final_file_path = os.path.join(save_path, random_filename)

    # 自定义 yt-dlp 配置
    ydl_opts = {
        'outtmpl': final_file_path,  # 使用随机文件名
        'format': quality,
        'merge_output_format': 'mp4',
        'overwrites': False,
        'verbose': False,
        'ignoreerrors': False,
        # 自定义进度条和输出信息
        'progress_hooks': [lambda d: progress_hook(d)],
        'hls_prefer_native': True,
        'hls_chunk_size': 1024 * 1024,
        'concurrent_fragment_downloads': 16,
        'hls_allow_multiple_fragments_per_ts': True,
        'retries': 5,
        'fragment_retries': 5,
        'skip_unavailable_fragments': True,
    }

    try:
        print("=" * 60)
        print(f"📌 开始处理视频任务")
        print(f"🔗 视频链接: {video_url}")
        print(f"📂 保存路径: {save_path}")
        print(f"🎬 视频质量: {quality}")
        print(f"⚡ 分片并发数: {ydl_opts['concurrent_fragment_downloads']}")
        print(f"🆔 随机文件名: {random_filename}")
        print("=" * 60)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # 提取视频信息（仅用于获取分片数）
            info_dict = ydl.extract_info(video_url, download=False)
            fragment_count = info_dict.get('n_fragments', '未知')
            print(f"🧩 总分片数: {fragment_count}")
            print(f"🚀 开始下载...（并发数{ydl_opts['concurrent_fragment_downloads']}）")

            # 执行下载
            ydl.download([video_url])

        print("\n🎉 视频下载完成！")
        print(f"📁 文件位置: {final_file_path}")
        # 显示文件大小
        if os.path.exists(final_file_path):
            file_size = os.path.getsize(final_file_path) / (1024 * 1024)
            print(f"📊 文件大小: {file_size:.2f} MB")
        print("=" * 60)

    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ 下载失败: 链接无效或无法访问 - {str(e)}")
    except PermissionError:
        print(f"\n❌ 权限错误: 无法写入 {save_path}，请检查文件夹权限")
    except Exception as e:
        print(f"\n❌ 未知错误: {str(e)}")


def progress_hook(d):
    """自定义下载进度提示（适配分片下载）"""
    if d['status'] == 'downloading':
        # 格式化进度信息
        downloaded = d.get('_downloaded_bytes_str', '0MB')
        total = d.get('_total_bytes_str', '未知大小')
        speed = d.get('_speed_str', '0B/s')
        eta = d.get('_eta_str', '未知时间')
        fragment = d.get('fragment_index', '')
        if fragment:
            fragment_info = f" | 分片: {fragment}/{d.get('fragment_count', '?')}"
        else:
            fragment_info = ""
        print(f"\r⏳ 下载中: {downloaded}/{total} | 速度: {speed} | 剩余时间: {eta}{fragment_info}", end='')
    elif d['status'] == 'finished':
        print("\n✅ 分片下载完成，正在合并为 MP4 格式...")


def main():
    """主函数，处理用户输入并执行下载"""
    # 检查命令行参数
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        # 交互式输入
        print("===== 视频下载工具 =====")
        video_url = input("请输入视频链接: ").strip()

    # 验证链接
    if not video_url:
        print("❌ 错误：视频链接不能为空！")
        return

    # 用户输入
    save_path = input(f"请输入保存路径（默认: {r'E:\DL'}）: ").strip() or r"E:\DL"
    quality = input("请输入视频质量（默认: best | 可选: 1080p/720p/worst）: ").strip() or "best"

    # 执行下载
    download_video(video_url, save_path, quality)


if __name__ == "__main__":
    main()