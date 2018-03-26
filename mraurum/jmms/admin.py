# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserType
from .models import User
from .models import Raw_Material_Type
from .models import Material_Purchase
from .models import Jewellery_type
from .models import Design_Catalog
from .models import Jewel
from .models import Jewellery
from .models import Cutting_phase
from .models import Embedding_phase
from .models import Polishing_phase

# Register your models here.
admin.site.register(UserType)
admin.site.register(User)
admin.site.register(Raw_Material_Type)
admin.site.register(Material_Purchase)
admin.site.register(Jewellery_type)
admin.site.register(Design_Catalog)
admin.site.register(Jewel)
admin.site.register(Jewellery)
admin.site.register(Cutting_phase)
admin.site.register(Embedding_phase)
admin.site.register(Polishing_phase)