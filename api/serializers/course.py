from rest_framework import serializers
from api import models

class DegreeCourseTeacherModelSerializer(serializers.ModelSerializer):
    # level_name = serializers.CharField(source='get_level_display')
    # hours = serializers.CharField(source='coursedetail.hours')
    # course_slogan = serializers.CharField(source='coursedetail.course_slogan')
    # # recommend_courses = serializers.CharField(source='coursedetail.recommend_courses.all')
    #
    teachers = serializers.SerializerMethodField()
    class Meta:
        model = models.DegreeCourse
        fields = ['id', 'name','teachers' ]
    def get_teachers(self,row):
        teachers_list = row.teachers.all()
        return [ {'id':item.id,'name':item.name} for item in teachers_list]


class DegreeCourseScholarshiprModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = ['id', 'name',]


class CourseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Course
        fields = ['id', 'name','total_scholarship']


class DegreeCourseTemplateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DegreeCourse
        fields = ['id', 'name',]


class DegreeCourseDetaileModelSerializer(serializers.ModelSerializer):
    level_choices= serializers.CharField(source='get_level_display')
    why_study = serializers.CharField(source='coursedetail.why_study')
    what_to_study_brief  = serializers.CharField(source='coursedetail.what_to_study_brief')
    recommend_courses = serializers.SerializerMethodField()
    class Meta:
        model = models.DegreeCourse
        fields = ['id', 'name','brief','level_choices','why_study','what_to_study_brief','recommend_courses']

    def get_recommend_courses(self,row):
        recommend_list = row.coursedetail.recommend_courses.all()
        return [ {'id':item.id,'name':item.name} for item in recommend_list]



class DegreeCourseOftenAskedQuestionModelSerializer(serializers.ModelSerializer):

    question = serializers.CharField(source='oftenaskedquestion_set.question')

    class Meta:
        model = models.Course
        fields = ['id', 'name','question']



class CoursesCourseoutlineViewModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CourseOutline
        fields = ['content','title']


    # def get_courseoutline(self, row):
    #     courseoutline_list = row.coursedetail.courseoutline_set.all()
    #     return [{'content': item.content, 'title': item.title} for item in courseoutline_list]




class CoursesChapterViewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CourseChapter
        fields = ['id', 'name']

