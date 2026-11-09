from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Course, Lesson
from .validators import validate_youtube_url


class LessonSerializer(serializers.ModelSerializer):
    video_link = serializers.URLField(
        validators=[validate_youtube_url],
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    @extend_schema_field(serializers.IntegerField)
    def get_lessons_count(self, obj):
        return obj.lessons.count()

    @extend_schema_field(serializers.BooleanField)
    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.subscriptions.filter(user=user).exists()
        return False

