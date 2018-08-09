from api.models import CourseCategory,CourseSubCategory,\
    DegreeCourse,Teacher,Scholarship,Course,CourseDetail,OftenAskedQuestion,\
    CourseOutline,CourseChapter,CourseSection,CourseSection,CourseSection
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from rest_framework.response import Response
from rest_framework.versioning import URLPathVersioning
from rest_framework.pagination import PageNumberPagination
from api import models
from api.serializers.course import DegreeCourseTeacherModelSerializer, DegreeCourseScholarshiprModelSerializer
from api.serializers.course import DegreeCourseTemplateModelSerializer,DegreeCourseDetaileModelSerializer
from api.serializers.course import DegreeCourseOftenAskedQuestionModelSerializer,CoursesCourseoutlineViewModelSerializer
from api.serializers.course import CoursesChapterViewModelSerializer
from api.utils.response import BaseResponse

class DegreeCourseTeacherView(APIView):

    def get(self,request,*args,**kwargs):
        # response = {'code':1000,'data':None,'error':None}
        ret = BaseResponse()
        try:
            # 从数据库获取数据,查看所有学位课并打印学位课名称以及授课老师
            queryset = models.DegreeCourse.objects.all()
            # 分页
            page = PageNumberPagination()
            degree_course_teacher = page.paginate_queryset(queryset,request,self)
            # 分页之后的结果执行序列化
            ser = DegreeCourseTeacherModelSerializer(instance=degree_course_teacher,many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)


class DegreeCourseScholarshiprView(APIView):
    def get(self, request,  *args, **kwargs):
        ret = BaseResponse()
        try:
            # 查看所有学位课并打印学位课名称以及学位课的奖学金

            degree_course_scholarshipr = DegreeCourse.objects.all()
            ser = DegreeCourseScholarshiprModelSerializer(instance=degree_course_scholarshipr,many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)

class CourseView(ViewSetMixin,APIView):
    def list(self, request,  *args, **kwargs):
        ret = BaseResponse()
        try:
            # 展示所有的专题课
            Course_list = Course.objects.filter(degree_course__isnull=True)
            ser = DegreeCourseScholarshiprModelSerializer(instance=Course_list,many=True,context={'request': request})
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict,)


class DegreeCourseTemplateView(APIView):
    def get(self, request,  *args, **kwargs):
        ret = BaseResponse()
        try:
            # 查看id=1的学位课对应的所有模块名称
            DegreeCourse_list = Course.objects.filter(degree_course_id=1)
            ser = DegreeCourseTemplateModelSerializer(instance=DegreeCourse_list ,many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)


class DegreeCourseDetaileView(APIView):
    def get(self, request,  *args, **kwargs):
        ret = BaseResponse()
        try:
            # 获取id = 1的专题课，并打印：课程名、级别(中文)、why_study、what_to_study_brief、所有recommend_courses
            DegreeCourse_info= Course.objects.filter(id=1)
            ser = DegreeCourseDetaileModelSerializer(instance=DegreeCourse_info,many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)


class DegreeCourseOftenAskedQuestionView(APIView):
    def get(self, request,*args, **kwargs):
        ret = BaseResponse()
        try:
            # 获取id = 1的专题课，并打印该课程相关的所有常见问题
            obj = Course.objects.get(id=1)
            ask_list = obj.asked_question.all()
            ser = DegreeCourseOftenAskedQuestionModelSerializer(instance=ask_list,many=True)
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)

class CoursesCourseoutlineView(APIView):

    def get(self, request, *args, **kwargs):
        ret = BaseResponse()
        try:
            # 获取id = 1的专题课，并打印该课程相关的课程大纲
            obj = models.Course.objects.get(id=1).coursedetail.courseoutline_set.all()
            ser = CoursesCourseoutlineViewModelSerializer(instance=obj,many=True,context={'request': request})
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)


class CoursesChapterView(APIView):

    def get(self, request,  *args, **kwargs):
        ret = BaseResponse()
        try:
            # 获取id = 1的专题课，并打印该课程相关的所有章节
            obj = models.CourseChapter.objects.filter(course_id=1).all()
            ser = CoursesChapterViewModelSerializer(instance=obj,many=True,context={'request': request})
            ret.data = ser.data
        except Exception as e:
            ret.code = 500
            ret.error = '获取数据失败'
        return Response(ret.dict)
