from rest_framework import serializers

class UsernameLengthSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=[("generate", "Generate"), ("check", "Check")])
    length = serializers.IntegerField(required=False, help_text="Desired length for generated username")
    username = serializers.CharField(required=False, help_text="Username to check for length validity")

class UsernameComplexitySerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=[("generate", "Generate"), ("check", "Check")])
    username = serializers.CharField(required=False, help_text="Username to check for complexity")

class CustomUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Custom username submitted by user")

class RandomUsernameIdeaSerializer(serializers.Serializer):
    length = serializers.IntegerField(required=False, help_text="Desired length for random username")

class UsernameFeedbackSerializer(serializers.Serializer):
    feedback = serializers.CharField(help_text="Feedback text regarding the username")

class AvoidSpecialCharactersSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username to be checked for special characters")

class FilterInappropriateWordsSerializer(serializers.Serializer):
    username = serializers.CharField(help_text="Username to check for inappropriate words")
