from os import path
from uuid import uuid4
from django.db import models


def object_directory_path(instance, filename):
    _, ext = path.splitext(filename)
    return f'objects/object_{instance.object.id}/{uuid4().hex + ext}'


def room_directory_path(instance, filename):
    _, ext = path.splitext(filename)
    return f'objects/object{instance.base_object.id}/{uuid4().hex + ext}'


class ObjectImage(models.Model):
    media = models.ImageField(
        verbose_name='Изображение', upload_to=object_directory_path,
    )
    object = models.ForeignKey(
        'Object', verbose_name='Объект', on_delete=models.CASCADE,
        related_name='images',
    )
    order = models.PositiveSmallIntegerField(
        verbose_name='Порядок картинки',
    )

    class Meta:
        verbose_name = 'Изображение объекта'
        verbose_name_plural = 'Изображения объектов'


class ObjectVideo(models.Model):
    media = models.URLField(
        verbose_name='Ссылка на видео',
    )
    object = models.ForeignKey(
        'Object', verbose_name='Объект', on_delete=models.CASCADE,
        related_name='videos',
    )
    order = models.PositiveSmallIntegerField(
        verbose_name='Порядок видео',
    )

    class Meta:
        verbose_name = 'Видео объекта'
        verbose_name_plural = 'Видео объектов'


class RoomImage(models.Model):
    media = models.ImageField(
        verbose_name='Изображение', upload_to=room_directory_path
    )
    object = models.ForeignKey(
        'Room', verbose_name='Комната', related_name='images',
        on_delete=models.CASCADE,
    )
