#!/usr/bin/env python3
"""
성남시 분당구 날씨 + 미세먼지 수집기
사용 API: Open-Meteo (무료, API 키 불필요)
저장 위치: ~/Documents/claude-workspace/weather.txt
Discord: .env 의 DISCORD_WEBHOOK_URL 로 전송
"""

import urllib.request
import urllib.error
import json
import os
from datetime import datetime, timezone

LAT       = 37.3595
LON       = 127.1052
WORKSPACE = os.path.expanduser("~/Documents/claude-workspace")
OUTPUT    = os.path.join(WORKSPACE, "weather.txt")
ENV_FILE  = os.path.join(WORKSPACE, ".env")

WEATHER_CODES = {
    0: "맑음", 1: "대체로 맑음", 2: "구름 조금", 3: "흐림",
    45: "안개", 48: "짙은 안개",
    51: "가벼운 이슬비", 53: "이슬비", 55: "짙은 이슬비",
    61: "약한 비", 63: "비", 65: "폭우",
    71: "약한 눈", 73: "눈", 75: "폭설",
    80: "소나기", 81: "강한 소나기", 82: "폭풍 소나기",
    95: "뇌우", 96: "우박 동반 뇌우", 99: "강한 우박 뇌우",
}

WEATHER_EMOJI = {
    0: "☀️", 1: "🌤️", 2: "⛅", 3: "☁️",
    45: "🌫️", 48: "🌫️",
    51: "🌦️", 53: "🌦️", 55: "🌦️",
    61: "🌧️", 63: "🌧️", 65: "🌊",
    71: "🌨️", 73: "❄️", 75: "❄️",
    80: "🌦️", 81: "🌧️", 82: "⛈️",
    95: "⛈️", 96: "⛈️", 99: "⛈️",
}

# embed 왼쪽 컬러 (날씨 기준)
WEATHER_COLOR = {
    0: 0xFFD700, 1: 0xFDB347, 2: 0x87CEEB, 3: 0x778899,
    45: 0xB0B0B0, 48: 0xB0B0B0,
    51: 0x6DAEDB, 53: 0x6DAEDB, 55: 0x6DAEDB,
    61: 0x2B7A9E, 63: 0x2B7A9E, 65: 0x1A5276,
    71: 0xADD8E6, 73: 0xADD8E6, 75: 0xD6EAF8,
    80: 0x4682B4, 81: 0x2E86C1, 82: 0x1B4F72,
    95: 0x4B0082, 96: 0x4B0082, 99: 0x4B0082,
}

PM10_LEVELS = [(30, "좋음", "🟢"), (80, "보통", "🟡"), (150, "나쁨", "🟠")]
PM25_LEVELS = [(15, "좋음", "🟢"), (35, "보통", "🟡"), (75,  "나쁨", "🟠")]
AQI_LEVELS  = [(50, "좋음"), (100, "보통"), (150, "민감군 주의"), (200, "나쁨")]


def load_env():
    env = {}
    if not os.path.exists(ENV_FILE):
        return env
    with open(ENV_FILE, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def grade(value, levels):
    for threshold, label, icon in levels:
        if value <= threshold:
            return label, icon
    return "매우나쁨", "🔴"


def aqi_label(aqi):
    for threshold, label in AQI_LEVELS:
        if aqi <= threshold:
            return label
    return "매우나쁨"


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "weather-script/1.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def send_discord(webhook_url, embed):
    payload = json.dumps({"embeds": [embed]}).encode()
    req = urllib.request.Request(
        webhook_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "DiscordBot (weather-script, 1.0)",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"Discord 전송 완료 (HTTP {resp.status})")
    except urllib.error.HTTPError as e:
        print(f"[오류] Discord 전송 실패: HTTP {e.code} — {e.read().decode()}")


def main():
    weather_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={LAT}&longitude={LON}"
        "&current=temperature_2m,apparent_temperature,"
        "relative_humidity_2m,weather_code,wind_speed_10m,precipitation"
        "&timezone=Asia%2FSeoul"
    )
    air_url = (
        "https://air-quality-api.open-meteo.com/v1/air-quality"
        f"?latitude={LAT}&longitude={LON}"
        "&current=pm10,pm2_5,us_aqi"
        "&timezone=Asia%2FSeoul"
    )

    try:
        w = fetch_json(weather_url)
        a = fetch_json(air_url)
    except Exception as e:
        print(f"[오류] 데이터 수집 실패: {e}")
        raise

    cur = w["current"]
    air = a["current"]

    temp     = cur["temperature_2m"]
    feels    = cur["apparent_temperature"]
    humidity = cur["relative_humidity_2m"]
    wind     = cur["wind_speed_10m"]
    wcode    = cur["weather_code"]
    precip   = cur.get("precipitation", 0)
    pm10     = air["pm10"]
    pm25     = air["pm2_5"]
    aqi      = air.get("us_aqi", 0)

    condition  = WEATHER_CODES.get(wcode, f"코드 {wcode}")
    emoji      = WEATHER_EMOJI.get(wcode, "🌡️")
    color      = WEATHER_COLOR.get(wcode, 0x7289DA)
    now        = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")
    now_short  = datetime.now().strftime("%-m월 %-d일 (%a) %p %-I시")  # 예: 7월 3일 (Thu) 오전 8시

    pm10_label,  pm10_icon  = grade(pm10,  PM10_LEVELS)
    pm25_label,  pm25_icon  = grade(pm25,  PM25_LEVELS)

    # ── weather.txt 저장 ──────────────────────────────────
    block = (
        f"\n{'='*45}\n"
        f"  {now}  성남시 분당구\n"
        f"{'='*45}\n"
        f"  날씨         {condition}\n"
        f"  기온         {temp}°C  (체감 {feels}°C)\n"
        f"  습도         {humidity}%\n"
        f"  풍속         {wind} km/h\n"
        f"  강수량       {precip} mm\n"
        f"{'-'*45}\n"
        f"  미세먼지     PM10  {pm10:.1f} µg/m³  {pm10_icon} {pm10_label}\n"
        f"  초미세먼지   PM2.5 {pm25:.1f} µg/m³  {pm25_icon} {pm25_label}\n"
        f"  AQI (미국)   {aqi}  ({aqi_label(aqi)})\n"
        f"{'='*45}\n"
    )
    with open(OUTPUT, "a", encoding="utf-8") as f:
        f.write(block)
    print(block)
    print(f"저장 완료 → {OUTPUT}")

    # ── Discord 전송 ──────────────────────────────────────
    env = load_env()
    webhook_url = env.get("DISCORD_WEBHOOK_URL", "")

    if not webhook_url or webhook_url == "YOUR_WEBHOOK_URL":
        print("Discord 전송 건너뜀 (.env 에 DISCORD_WEBHOOK_URL 미설정)")
        return

    # 강수량은 0일 때 숨김
    precip_value = f"**{precip} mm**" if precip > 0 else "없음"

    # 한국 요일
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]
    weekday  = weekdays[datetime.now().weekday()]
    date_str = datetime.now().strftime(f"%-m월 %-d일 ({weekday})")

    embed = {
        "author": {
            "name": "📍 경기도 성남시 분당구 정자동",
        },
        "title": f"{emoji}  {condition}  ·  {date_str}",
        "description": (
            f"> 🌡️  현재 기온 **{temp}°C** (체감 **{feels}°C**) · "
            f"💧 습도 **{humidity}%** · 💨 풍속 **{wind} km/h**"
        ),
        "color": color,
        "fields": [
            # 구분선 역할
            {
                "name": "─────────────── 🌫️  대기질 ───────────────",
                "value": "​",
                "inline": False,
            },
            # 미세먼지 3컬럼
            {
                "name": f"미세먼지  PM10",
                "value": f"**{pm10:.1f}** µg/m³\n{pm10_icon}  {pm10_label}",
                "inline": True,
            },
            {
                "name": f"초미세먼지  PM2.5",
                "value": f"**{pm25:.1f}** µg/m³\n{pm25_icon}  {pm25_label}",
                "inline": True,
            },
            {
                "name": "AQI  (미국기준)",
                "value": f"**{aqi}**\n📊  {aqi_label(aqi)}",
                "inline": True,
            },
            # 강수량 (별도 행)
            {
                "name": "🌂  강수량",
                "value": precip_value,
                "inline": False,
            },
        ],
        "footer": {
            "text": "⏰ 매일 오전 8시 자동 업데이트  ·  Open-Meteo 제공  ·  분당구 정자동 기준",
        },
        "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    send_discord(webhook_url, embed)


if __name__ == "__main__":
    main()
