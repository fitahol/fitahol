# coding=utf-8
import base64
import datetime
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import list_route

from account.models import Coach, Member
from fitness.models import GoalRecord, InBodyRecords, Muscle, \
    ExerciseCategory, FitnessExercise, FitnessEquipment, ExerciseMuscle, \
    ExerciseRecord, ExpertTag, FitGoal
from fitness.serializers import GoalRecordSerializer, InBodyRecordsSerializer, \
    ExerciseCategorySerializer, FitnessExerciseSerializer, \
    FitnessEquipmentSerializer, FitnessDetailExerciseSerializer, \
    MuscleSerializer, FitnessCreateExerciseSerializer, FitGoalSerializer, \
    GoalRecordCreateSerializer, ExerciseRecordSerializer, \
    ExerciseRecordCreateSerializer, ExpertTagSerializer, FitGoalCreateSerializer


class InBodyRecordsViewSet(viewsets.ModelViewSet):
    """
    InBody 体测记录
    """
    queryset = InBodyRecords.objects.all()
    serializer_class = InBodyRecordsSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user")
        if user_id:
            return InBodyRecords.objects.filter(user_id=user_id)
        return []


class ExerciseCategoryViewSet(viewsets.ModelViewSet):
    queryset = ExerciseCategory.objects.all()
    serializer_class = ExerciseCategorySerializer
    pagination_class = None

    def get_queryset(self):
        user_custom = ExerciseCategory.objects.filter(user=self.request.user)
        default = ExerciseCategory.objects.filter(user=None)
        if self.request.method == "DELETE":
            return user_custom
        return default | user_custom

    def create(self, request, *args, **kwargs):
        request.data["user"] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,
                        status=status.HTTP_201_CREATED, headers=headers)


class MuscleViewSet(viewsets.ModelViewSet):
    queryset = Muscle.objects.all()
    serializer_class = MuscleSerializer
    pagination_class = None


class FitnessExerciseViewSet(viewsets.ModelViewSet):
    queryset = FitnessExercise.objects.all()
    serializer_class = FitnessExerciseSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.kwargs.get("pk"):
            return FitnessDetailExerciseSerializer
        if self.request.method == "POST":
            return FitnessCreateExerciseSerializer
        return FitnessExerciseSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get("category_id")
        muscle_id = self.request.query_params.get("muscle_id")
        if category_id:
            return FitnessExercise.objects.filter(category_id=category_id)
        if muscle_id:
            return FitnessExercise.objects.filter(
                exercisemuscle__muscle_id=muscle_id)
        return FitnessExercise.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = serializer.data
        for muscle in result["muscles"]:
            ex_muscle_ref = ExerciseMuscle.objects.get(
                exercise_id=result["id"], muscle_id=muscle["id"])
            muscle["level"] = ex_muscle_ref.level
        return Response(result)


class FitnessEquipmentViewSet(viewsets.ModelViewSet):
    queryset = FitnessEquipment.objects.all()
    serializer_class = FitnessEquipmentSerializer


class ExerciseRecordViewSet(viewsets.ModelViewSet):
    queryset = ExerciseRecord.objects.all()
    pagination_class = None
    
    def create(self, request, *args, **kwargs):
        request_data = self.request.data.copy()
        request_data["user"] = request.data["user_id"]
        request_data["event"] = request.data["event_id"]
        request_data["exercise"] = request.data["exercise_id"]
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "创建成功"}, status=status.HTTP_201_CREATED)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return ExerciseRecordSerializer
        return ExerciseRecordCreateSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params["user_id"]
        event_id = self.request.query_params["event_id"]
        return ExerciseRecord.objects.filter(user_id=user_id, event_id=event_id)


class ExpertTagViewSet(viewsets.ModelViewSet):
    """擅长领域, 仅教练自己可编辑"""
    model = ExpertTag
    queryset = ExpertTag.objects.all()
    serializer_class = ExpertTagSerializer
    permission_classes = (IsAuthenticated,)
    
    def get_queryset(self):
        self.pagination_class = None
        if self.request.user.profile.u_type == 1:
            coach = self.request.user.coach
        else:
            user_id = self.request.query_params.get("user_id")
            try:
                coach = Coach.objects.get(user_id=user_id)
            except Coach.DoesNotExist:
                return None
        return coach.expert_tags.all()
    
    @list_route()
    def public(self, request, *args, **kwargs):
        queryset = self.model.objects.filter(is_public=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["pk"])
    
    def create(self, request, *args, **kwargs):
        expert_tag_id = self.request.data.get("expert_tag")
        if not expert_tag_id:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            expert_tag = serializer.save()
        else:
            expert_tag = get_object_or_404(ExpertTag, id=expert_tag_id)
        try:
            coach = Coach.objects.get(user=self.request.user)
            coach.expert_tags.add(expert_tag)
            coach.save()
        except Coach.DoesNotExist:
            return Response({"detail": "用户异常"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "创建成功"},
                        status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        coach = Coach.objects.get(user=self.request.user)
        coach.expert_tags.remove(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FitGoalViewSet(viewsets.ModelViewSet):
    """
    健身目标, 学员及学员的教练均可编辑
    """
    model = FitGoal
    queryset = FitGoal.objects.all()
    serializer_class = FitGoalSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = None
    
    def get_serializer_class(self):
        if self.request.method == "GET":
            return FitGoalSerializer
        return FitGoalCreateSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        return FitGoal.objects.filter(user_id=user_id)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        request_data = self.request.data.copy()
        request_data["user"] = self.request.data["user_id"]
        serializer = self.get_serializer(instance, data=request_data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs["pk"])
    
    @list_route()
    def public(self, request, *args, **kwargs):
        queryset = self.model.objects.filter(is_public=True)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)
    
    @list_route()
    def last(self, request, *args, **kwargs):
        user_id = self.request.query_params["user_id"]
        last_record = GoalRecord.objects.filter(user_id=user_id).last()
        if not last_record:
            return Response({})
        fit_goal_obj = last_record.fit_goal
        serializer = self.get_serializer(fit_goal_obj)
        result = serializer.data
        result["goal_record"] = GoalRecordSerializer(last_record).data
        return Response(result)
    
    def list(self, request, *args, **kwargs):
        response = super(FitGoalViewSet, self).list(request, *args, **kwargs)
        user_id = self.request.query_params.get("user_id")
        rsp_data = response.data
        for each in rsp_data:
            fit_goal_id = each["id"]
            queryset = GoalRecord.objects.filter(
                user_id=user_id, fit_goal_id=fit_goal_id).order_by("-cdate")[:7]
            each["goal_record"] = GoalRecordSerializer(queryset, many=True).data
        return Response(rsp_data)
    
    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        user_id = request.data["user_id"]
        request_data["user"] = user_id
        user_obj = self.request.user
        member = Member.objects.get(user_id=user_id)
        try:
            if user_obj.profile.u_type == 1 and \
                    not member.coach.filter(user=request.user).exists():
                return Response({"detail": "用户%s不是您的学员" % user_id},
                                status=status.HTTP_400_BAD_REQUEST)
            serializer = FitGoalCreateSerializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Coach.DoesNotExist:
            return Response({"detail": "用户异常"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "创建成功"},
                        status=status.HTTP_201_CREATED)
    
    def destroy(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user_id")
        if not user_id:
            return Response({"detail": "参数user_id缺失"},
                            status=status.HTTP_400_BAD_REQUEST)
        instance = self.get_object()
        member = Member.objects.get(user_id=user_id)
        if self.request.user.id != int(user_id) and \
                not member.coach.filter(user=self.request.user).exists():
            return Response({"msg": "您没有权限删除数据"},
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GoalRecordViewSet(viewsets.ModelViewSet):
    """
    健身记录
    """
    queryset = GoalRecord.objects.all()
    serializer_class = GoalRecordSerializer
    pagination_class = None

    def get_serializer_class(self):
        if self.request.method == "POST":
            return GoalRecordCreateSerializer
        return GoalRecordSerializer

    def create(self, request, *args, **kwargs):
        request_data = request.data.copy()
        figure_file = request_data.get("figure_file")
        pic_data = request_data.get("figure")
        if figure_file:
            # 支持文件上传
            request_data["figure"] = figure_file
        if pic_data:
            # 支持base64 数据压缩值上传
            filename = "figure_" + str(
                request_data["user_id"]) + "." + self.request.data.get("type",
                                                                       "png")
            buffer = BytesIO(base64.decodebytes(
                pic_data.split('base64,')[1].encode('ascii')))
            filebuffer = InMemoryUploadedFile(
                buffer, None, filename, 'image/png', len(buffer.getvalue()),
                None)
            request_data["figure"] = filebuffer
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        fit_goal_id = self.request.query_params.get("fit_goal_id")
        interval = self.request.query_params.get("interval", 30)
        if not user_id:
            return []
        queryset = GoalRecord.objects.filter(user_id=user_id)
        if fit_goal_id:
            queryset = queryset.filter(fit_goal_id=fit_goal_id)
        return queryset[:interval]
