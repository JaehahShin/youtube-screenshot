# Frame-Grabber for YouTube Videos  
유튜브 동영상 초당 프레임 추출기

---

## Description  
**EN:** This script captures one frame per second from any YouTube video and saves them as individual JPEG files.  
**KR:** 이 스크립트는 유튜브 동영상에서 매 초마다 하나의 프레임을 추출하여 JPEG 파일로 저장합니다.

---

## Requirements / 사전 요구사항

- Python 3.6+  
- [opencv-python](https://pypi.org/project/opencv-python/)  
- [pafy](https://pypi.org/project/pafy/)  
- A YouTube downloader backend:  
  - either `youtube_dl` **or** `yt-dlp`  

```bash
pip install opencv-python pafy youtube_dl
# 또는, yt-dlp 사용 시
pip install opencv-python pafy yt-dlp
