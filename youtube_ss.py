#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
capture_every_second.py

EN:
 Capture one frame per second from a YouTube video segment using yt-dlp and OpenCV.
KR:
 yt-dlp와 OpenCV를 사용하여 유튜브 동영상 특정 구간에서 매 초마다 한 프레임을 추출합니다.
"""

import cv2                       # EN: OpenCV library for video capture and image processing
                                 # KR: 비디오 캡처 및 이미지 처리를 위한 OpenCV 라이브러리
from yt_dlp import YoutubeDL     # EN: yt-dlp for extracting direct video stream URLs from YouTube
                                 # KR: YouTube 스트림 URL을 추출하기 위한 yt-dlp 모듈
import os                        # EN: OS module for directory creation and file path operations
                                 # KR: 디렉터리 생성 및 파일 경로 조작을 위한 OS 모듈


def capture_every_second(
    youtube_url: str,
    output_dir: str = "frames",
    start_sec: int = 0,
    end_sec: int = None
):
    """
    EN:
    Captures one frame per second from a YouTube video between start_sec and end_sec.
    KR:
    유튜브 동영상에서 start_sec부터 end_sec까지 매 초마다 프레임을 추출합니다.

    :param youtube_url: full YouTube URL (https://www.youtube.com/watch?v=...)
                          # KR: 전체 유튜브 링크
    :param output_dir: directory to save JPEG frames
                         # KR: JPEG 프레임을 저장할 디렉터리
    :param start_sec: first second (inclusive) to grab (default=0)
                        # KR: 추출 시작 초 (포함)
    :param end_sec: last second (inclusive) to grab; if None, runs till video end
                      # KR: 마지막 추출 초 (포함); None이면 동영상 끝까지
    """
    os.makedirs(output_dir, exist_ok=True)  # EN: Create output directory if it does not exist
                                            # KR: 출력 디렉터리가 없으면 생성

    # 1) Configure yt-dlp to select the best MP4 stream without downloading
    ydl_opts = {
        'format': 'best[ext=mp4]',   # EN: select highest quality MP4 format
                                      # KR: 최고 화질 MP4 포맷 선택
        'quiet': True,               # EN: suppress yt-dlp console output
                                      # KR: yt-dlp 출력 최소화
        'noplaylist': True           # EN: ensure single video only
                                      # KR: 재생목록 없이 단일 비디오만
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)  # EN: get metadata and stream URL
                                                            # KR: 메타데이터와 스트림 URL 추출
        stream_url = info['url']                              # EN: direct video stream URL
                                                            # KR: 실제 비디오 스트림 URL

    # 2) Open the video stream with OpenCV
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise RuntimeError("Unable to open video stream! / 비디오 스트림을 열 수 없습니다!")

    # 3) Retrieve video properties
    fps = cap.get(cv2.CAP_PROP_FPS)                         # EN: frames per second
                                                            # KR: 초당 프레임 수
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    # EN: total frame count
                                                            # KR: 총 프레임 수
    duration = frame_count / fps                            # EN: total duration in seconds
                                                            # KR: 전체 재생 시간(초)
    print(f"Video duration: {duration:.1f}s @ {fps:.2f} FPS") # EN: log duration and fps
                                                               # KR: 재생 시간과 FPS 출력

    # 4) Validate and adjust time range
    start_sec = max(0, start_sec)                           # EN: ensure start_sec >= 0
                                                            # KR: start_sec가 0 이상인지 확인
    if end_sec is None or end_sec > duration:
        end_sec = int(duration)                             # EN: default to video end if end_sec not specified
                                                            # KR: end_sec 미지정 시 동영상 끝으로 설정
    if start_sec > end_sec:
        raise ValueError("start_sec must be <= end_sec / start_sec는 end_sec 이하이어야 합니다")

    # 5) Loop through each second and capture a frame
    for sec in range(start_sec, end_sec + 1):
        cap.set(cv2.CAP_PROP_POS_MSEC, sec * 1000)          # EN: seek to exact millisecond position
                                                            # KR: 밀리초 단위로 영상 위치 지정
        ret, frame = cap.read()                             # EN: read frame at this position
                                                            # KR: 해당 위치에서 프레임 읽기
        if not ret:
            print(f"[!] No frame at {sec}s, stopping early. / {sec}초에서 프레임을 찾을 수 없습니다.")
            break

        fname = os.path.join(output_dir, f"frame_{sec:04d}.jpg")  # EN: construct filename e.g. frame_0948.jpg
                                                                    # KR: 파일명 생성 예시: frame_0948.jpg
        cv2.imwrite(fname, frame)                                 # EN: save frame as JPEG
                                                                    # KR: JPEG로 프레임 저장
        print(f"✔ Saved {fname} / 저장 완료")

    # 6) Release resources
    cap.release()                                             # EN: close the capture and free resources
                                                            # KR: VideoCapture 해제 및 자원 반환
    print("Done! All specified frames have been saved. / 완료! 모든 지정된 프레임이 저장되었습니다.")


if __name__ == "__main__":
    YOUTUBE_URL = "url here"  # EN: example YouTube URL
                                                                  # KR: 예시 유튜브 링크
    # e.g. capture from 948s through 1110s:
    capture_every_second(
        youtube_url=YOUTUBE_URL,
        output_dir="output_frames",
        start_sec=948,
        end_sec=1110
    )
