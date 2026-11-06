from rest_framework import serializers
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

    class Meta:
        model = Course
        fields = '__all__'

    def get_lessons_count(self, obj):
        return obj.lessons.count()