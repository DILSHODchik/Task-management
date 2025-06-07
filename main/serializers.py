from rest_framework import serializers
from .models import Task, User, Label, SyncStatus, Category
class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    title = serializers.CharField(max_length = 100)
    description = serializers.CharField(max_length = 500, allow_blank = True)
    due_date = serializers.DateField(required = False, allow_null = True)
    is_completed = serializers.BooleanField(default = False)
 
    user = serializers.PrimaryKeyRelatedField(queryset = User.objects.all())
    labels = serializers.PrimaryKeyRelatedField(many = True, queryset = Label.objects.all())
    category = serializers.PrimaryKeyRelatedField(queryset = Category.objects.all(), required = False, allow_null = True)
    
    
    def create(self, validated_data):
        label_data = validated_data.pop('labels', [])
        task = Task.objects.create(**validated_data)
        task.labels.set(label_data)
        return task
    
    def update(self, instance, validated_data):
        label_data = validated_data.pop('labels', None)
        category_data = validated_data.pop('category', None)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.user = validated_data.get('user', instance.user)
        
        if label_data is not None:
            instance.labels.set(label_data)
        if category_data is not None:
            instance.category = category_data
            
        instance.save()
        return instance


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    username = serializers.CharField(max_length = 100)
    email = serializers.EmailField()
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
            password = validated_data.get('password', None)
        )
        return user
    
    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance
    
class LabelSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 100)
    
    def create(self, validated_data):
        return Label.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
    
class SyncStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    task = serializers.PrimaryKeyRelatedField(queryset=Task.objects.all())
    status = serializers.CharField(max_length=50)
    last_synced = serializers.DateTimeField(read_only=True)
    
    def create(self, validated_data):
        return SyncStatus.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(max_length = 100)
    
    def create(self, validated_data):
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance
