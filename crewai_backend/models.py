from pydantic import BaseModel
from typing import List

class NamedUrls(BaseModel):
    name: str
    url: str

class ResultInfo(BaseModel):
    course: str
    subject: str
    name: str
    blog_articles_urls: List[str]
    youtube_videos_urls: List[NamedUrls]

class ResultInfoList(BaseModel):
    results: List[ResultInfo]
