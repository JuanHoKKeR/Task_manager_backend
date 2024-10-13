from rest_framework import serializers
from .models import Task, Tag
from django.contrib.auth.models import User

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ('id',)
        

class TaskSerializer(serializers.ModelSerializer):
    attachment = serializers.FileField(required=False, allow_null=True)
    tags = TagSerializer(many=True, required=False)
    
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ('user',)
        
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        task = Task.objects.create(**validated_data)
        
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(user=self.context['request'].user, name=tag_data['name'])
            task.tags.add(tag)  
        return task
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', [])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags_data:
            instance.tags.clear()
            for tag_data in tags_data:
                tag, created = Tag.objects.get_or_create(user=self.context['request'].user, name=tag_data['name'])
                instance.tags.add(tag)
        return instance
        
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User 
        fields = ('id', 'username', 'email', 'password')
        
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('El email ya esta en uso')
        return value
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
