from apps.designers import models as designers_models
from apps.aboutus import models as aboutus_models
from apps.services import models as services_models
from apps.companies import models as companies_models


class DesignerService:
    __designer_model = designers_models.Designer

    @classmethod
    def get_list(cls, *args, **kwargs):
        return (
            cls.__designer_model.objects.filter(*args, **kwargs)
        )

