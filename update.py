import requests

SOURCE_URL = https://raw.githubusercontent.com/abusaeeidx/Mrgify-BDIX-IPTV/refs/heads/main/playlist.m3u
PLAYLIST_FILE = "playlist.m3u"


def get_source_playlist():
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()
    return response.text.strip()


def get_stream_urls(text):
    urls = set()

    for line in text.splitlines():
        line = line.strip()

        if line.startswith(("http://", "https://")):
            urls.add(line)

    return urls


try:
    with open(PLAYLIST_FILE, "r", encoding="utf-8") as file:
        old_playlist = file.read().strip()
except FileNotFoundError:
    old_playlist = "#EXTM3U"


source_playlist = get_source_playlist()

old_urls = get_stream_urls(old_playlist)

lines = source_playlist.splitlines()
new_entries = []
i = 0

while i < len(lines):
    line = lines[i].strip()

    if line.startswith("#EXTINF:") and i + 1 < len(lines):
        stream_url = lines[i + 1].strip()

        if stream_url.startswith(("http://", "https://")):
            if stream_url not in old_urls:
                new_entries.append(line)
                new_entries.append(stream_url)

        i += 2
    else:
        i += 1


if new_entries:
    with open(PLAYLIST_FILE, "a", encoding="utf-8") as file:
        file.write("\n" + "\n".join(new_entries) + "\n")

    print(f"Added {len(new_entries) // 2} new channel(s).")
else:
    print("No new channels found.")
