from typing import List, Type
from pydantic.v1 import BaseModel, Field
import os
import requests
from crewai_tools import BaseTool

class VideoSearchResult(BaseTool):
    title: str
    video_url: str

class YoutubeVideoSearchToolInput(BaseModel):
    '''Input for YoutubeVideoSearchTool.'''
    keyword: str = Field(..., description='Keyword to search for on Youtube.')
    max_results: int = Field(10, description='Maximum number of results to return.')

class YoutubeVideoSearchTool(BaseTool):
    name: str = 'Search YouTube Videos'
    description: str = 'Searches YouTube videos based on a keyword and returns a list of video search results.'
    arg_schema: Type[BaseModel] = YoutubeVideoSearchToolInput

    def _run(self, keyword: str, max_results: int = 10) -> List[VideoSearchResult]:
        api_key = os.getenv('YOUTUBE_API_KEY')
        api_url = 'https://www.googleapis.com/youtube/v3/search'
        params = {
            'part': 'snippet',
            'q': keyword,
            'type': 'video',
            'maxResults': max_results,
            'key': api_key
        }
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()
        items = data.get('items', [])

        results = []
        for item in items:
            video_id = item['id']['videoId']
            title = item['snippet']['title']
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            results.append(VideoSearchResult(title=title, video_url=video_url))

        return results
