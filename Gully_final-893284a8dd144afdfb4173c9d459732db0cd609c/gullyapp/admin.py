from django.contrib import admin
from .models import Category
from .models import Userprofile
from .models import createTeam
from .models import Notification
from .models import Noti


from .models import ShownTeamsHistory



admin.site.register(Category)
admin.site.register(Userprofile)
admin.site.register(createTeam)
admin.site.register(Notification)
admin.site.register(Noti)

admin.site.register(ShownTeamsHistory)
