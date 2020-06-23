from django.db import models


class LikedVideos(models.Model):
    video_id = models.CharField(max_length=255, unique=True)


class SearchQuery(models.Model):
    query = models.CharField(max_length=255, unique=True)


class CacheResult(models.Model):
    query_id = models.ForeignKey(
        SearchQuery,
        related_name='cached_videos',
        on_delete=models.SET_NULL,
        null=True
    )
    video_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=65535)
    channel_title = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255)
