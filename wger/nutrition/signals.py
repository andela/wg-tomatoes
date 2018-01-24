from django.core.cache import cache
from wger.utils.cache import cache_mapper
from django.db.models.signals import (post_save, post_delete)
from django.dispatch import receiver
from wger.nutrition.models import (
    NutritionPlan,
    Meal,
    MealItem
)


@receiver([post_save, post_delete], sender=NutritionPlan)
def nplan_trigger_cache_reset(sender, instance, **kwargs):
    cache.delete(cache_mapper.get_nutritional_info(instance.pk))


@receiver([post_save, post_delete], sender=Meal)
def meal_trigger_cache_reset(sender, instance, **kwargs):
    cache.delete(cache_mapper.get_nutritional_info(instance.pk))


@receiver([post_save, post_delete], sender=MealItem)
def mitem_trigger_cache_reset(sender, instance, **kwargs):
    cache.delete(cache_mapper.get_nutritional_info(instance.pk))
