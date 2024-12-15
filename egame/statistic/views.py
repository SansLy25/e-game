from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from practice.models import Exam


class ExamStatisticView(TemplateView):
    template_name = "statistic/exam_stats.html"


class GetExamStatisticAPIView(APIView):
    def get(self, request, exam_slug):
        user = request.user
        exam = get_object_or_404(Exam, slug=exam_slug)
        response = {
            "average_score": user.get_exam_average_score(exam_slug),
            "max_score": exam.themes.filter(is_answered=True).count(),
            "average_duration": user.get_exam_average_duration(exam_slug),
            "max_duration": 19_200,
            "average_variant_size": user.get_average_variant_size(exam_slug),
            "variant_count": user.get_solutions(
                exam_slug,
                full_variant=False,
            ).count(),
            "max_variant_size": exam.themes.all().count(),
            "all_users_average_score": user.get_all_users_average_score(
                exam_slug,
            ),
            "all_users_average_duration": user.get_all_users_average_duration(
                exam_slug,
            ),
            "score_dynamic": user.get_score_dynamic(exam_slug),
            "duration_dynamic": user.get_time_dynamic(exam_slug),
            "friends_average_scores": user.get_friends_average_scores(
                exam_slug,
            ),
        }

        return Response(response, status=status.HTTP_200_OK)
