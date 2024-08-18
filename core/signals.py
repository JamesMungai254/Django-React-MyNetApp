from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Student, SchoolFee

@receiver(post_save, sender=Student)
def create_school_fee(sender, instance, created, **kwargs):
    if created:
        SchoolFee.objects.create(
            student=instance,
            total_fee=0.00,
            fee_paid=0.00
        )
