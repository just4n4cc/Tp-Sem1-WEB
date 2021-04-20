from django.contrib import admin

# Register your models here.
from app.models import Profile, Tag, Question, Answer, LikeQuestion, LikeAnswer

admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(LikeQuestion)
admin.site.register(LikeAnswer)
