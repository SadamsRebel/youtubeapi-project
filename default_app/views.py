from django.shortcuts import render, redirect
from .youtubeapi import YouTubeApi
from .youtubeapi_key import YOUTUBE_API_KEY
from default_project.settings import CACHING_STATUS
from .models import LikedVideos
from .models import SearchQuery
from .models import CacheResult


def index(request):
    return render(request, 'default_app/index.html')


def search(request):
    search_query = request.GET.get('search_query')
    if search_query is not None:
        new_query = None
        if CACHING_STATUS:
            cached_query = SearchQuery.objects.filter(query=search_query).first()
            if cached_query is not None:
                cached_videos_list = cached_query.cached_videos.all()
                videos_list = []
                for cached_video in cached_videos_list:
                    video_data = {
                        'video_id': cached_video.video_id,
                        'title': cached_video.title,
                        'description': cached_video.description,
                        'channel_title': cached_video.channel_title,
                        'channel_id': cached_video.channel_id
                    }
                    videos_list.append(video_data)
                return render(request, 'default_app/search.html', {
                    'videos_list': videos_list,
                    'search_query': search_query,
                    'cached_result': 'This is Cached Result'
                })
            else:
                new_query = SearchQuery(query=search_query)
                new_query.save()
        yta = YouTubeApi(YOUTUBE_API_KEY)
        videos_list = yta.find_videos(search_query)
        for video in videos_list:
            target = LikedVideos.objects.filter(video_id=video['video_id'])
            video['liked'] = target.exists()
            if CACHING_STATUS:
                new_cache_result = CacheResult(
                    query_id=new_query,
                    video_id=video['video_id'],
                    title=video['title'],
                    description=video['description'],
                    channel_title=video['channel_title'],
                    channel_id=video['channel_id']
                )
                new_cache_result.save()
        return render(request, 'default_app/search.html', {
            'videos_list': videos_list,
            'search_query': search_query
        })
    else:
        return render(request, 'default_app/search.html')


def liked(request):
    if request.method == 'GET':
        yta = YouTubeApi(YOUTUBE_API_KEY)
        liked_videos_ids = LikedVideos.objects.all().values_list(
            'video_id',
            flat=True
        )
        liked_videos_list = yta.get_videos_by_ids(liked_videos_ids)
        return render(request, 'default_app/liked.html', {
            'liked_videos_list': liked_videos_list
        })
    elif request.method == 'POST':
        video_id = request.POST.get('video_id')
        if video_id is not None:
            target = LikedVideos.objects.filter(video_id=video_id)
            if not target.exists():
                liked_video = LikedVideos(video_id=video_id)
                liked_video.save()
            else:
                target.first().delete()
            return redirect('default_app:liked')
