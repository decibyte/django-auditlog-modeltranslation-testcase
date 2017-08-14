from modeltranslation.translator import register, TranslationOptions

from . import models


@register(models.MyModel)
@register(models.MyModel.audit_log.model)
class MyModelTranslationOptions(TranslationOptions):
    """Translation options for MyModel."""

    fields = (
        'title',
        'text',
    )
