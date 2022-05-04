from rest_framework import serializers
from .models import *



class LoaderBook(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"
        read_only_fields = ['category']
        extra_kvargs = {
            'category': {'read_only': True},
            }


class LoaderAudioBook(serializers.ModelSerializer):
    class Meta:
        model = AudioBook
        fields = "__all__"


class LoaderCategory(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class LoaderLanguage(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = "__all__"


class LoaderHistoryBook(serializers.ModelSerializer):
    class Meta:
        model = HistoryBook
        fields = "__all__"


class LoaderHistoryAudioBook(serializers.ModelSerializer):
    class Meta:
        model = HistoryAudioBook
        fields = "__all__"

class LoaderReytingAudioBook(serializers.ModelSerializer):
    class Meta:
        model = ReytingAudioBook
        fields = "__all__"

class LoaderReytingBook(serializers.ModelSerializer):
    class Meta:
        model = ReytingBook
        fields = "__all__"

class LoaderHistoryBook(serializers.ModelSerializer):
    class Meta:
        model = HistoryBook
        fields = "__all__"
