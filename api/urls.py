from django.conf.urls import url
from api.views import course
from api.views import auth
from api.views import shoppingcar
urlpatterns = [
    url(r'auth/$',auth.AuthView.as_view({'post':'login'})),
    url(r'DegreeCourseTeacher/$', course.DegreeCourseTeacherView.as_view()),
    url(r'DegreeCourseScholarshipr/$', course.DegreeCourseScholarshiprView.as_view()),
    url(r'Course/$', course.CourseView.as_view({'get':'list'})),
    url(r'DegreeCourseTemplate/$', course.DegreeCourseTemplateView.as_view()),
    url(r'DegreeCourseDetaile/$', course.DegreeCourseDetaileView.as_view()),
    url(r'DegreeCourseOftenAskedQuestion/$', course.DegreeCourseOftenAskedQuestionView.as_view()),
    url(r'DegreeCourseCourseOutlinen/$', course.CoursesCourseoutlineView.as_view()),
    url(r'CoursesChapter/$', course.CoursesChapterView.as_view()),


    url(r'shoppingcar/$',shoppingcar.ShoppingCarView.as_view({'get':'list','post':'create','delete':'destroy','put':'update'})),
    # url(r'shoppingcar/$',shoppingcar.ShoppingCarView.as_view({'get':'list','post':'create',})),

    # url(r'shoppingcar/(?P<pk>\d+)$',shoppingcar.ShoppingCarView.as_view({'delete':'destroy'}))
    # url(r'courses/(?P<pk>\d+)/$',course.DegreeCourseScholarshiprView.as_view())
]