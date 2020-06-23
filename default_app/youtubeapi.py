import requests
# from pprint import pprint


class YouTubeApi:
    SEARCH_URL = 'https://www.googleapis.com/youtube/v3/search'
    VIDEO_DETAIL_URL = 'https://www.googleapis.com/youtube/v3/videos'

    def __init__(self, api_key):
        self.api_key = api_key

    def find_videos(self, query):
        params = {
            'key': self.api_key,
            'type': 'video',
            'part': 'snippet',
            'q': query
        }

        response = requests.get(self.SEARCH_URL, params=params)

        if not response.ok:
            return []

        result = response.json()
        video_list = result['items']
        videos = []

        for video in video_list:
            video_data = {
                'video_id': video['id']['videoId'],
                'title': self._clean_string(
                    video['snippet']['title']
                ),
                'description': self._clean_string(
                    video['snippet']['description']
                ),
                'channel_title': video['snippet']['channelTitle'],
                'channel_id': video['snippet']['channelId']
            }

            videos.append(video_data)

        return videos

    def get_videos_by_ids(self, videos_ids):
        videos_ids_str = ','.join(videos_ids)
        params = {
            'key': self.api_key,
            'part': 'snippet',
            'id': videos_ids_str
        }

        response = requests.get(self.VIDEO_DETAIL_URL, params=params)

        if not response.ok:
            return []

        result = response.json()

        video_list = result['items']
        videos = []

        for video in video_list:
            video_data = {
                'video_id': video['id'],
                'title': self._clean_string(
                    video['snippet']['title']
                ),
                'description': self._clean_string(
                    video['snippet']['description']
                ),
                'channel_title': video['snippet']['channelTitle'],
                'channel_id': video['snippet']['channelId']
            }

            videos.append(video_data)

        return videos

    def _clean_string(self, target):
        pattern = {
            '&quot;': '"',
            '&nbsp;': ' ',
            '&#39;': '\'',
            '&yen;': '¥',
            '&euro;': '€',
            '&copy;': '©',
            '&gt;': '>',
            '&lt': '<',
            '&pound;': '£',
            '&reg;': '®',
            '&amp;': '&',
            '&apos;': '\'',
            '&cent;': '¢'
        }

        for expression, spec_char in pattern.items():
            target = target.replace(expression, spec_char)

        return target
