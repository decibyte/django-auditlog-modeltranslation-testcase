from modeltranslation.translator import register, TranslationOptions

from . import models


@register(models.MyModel)
class MyModelTranslationOptions(TranslationOptions):
    """Translation options for MyModel."""

    fields = (
        'title',
        'text',
    )
