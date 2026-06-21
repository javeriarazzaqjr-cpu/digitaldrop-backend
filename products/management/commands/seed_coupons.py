from django.core.management.base import BaseCommand
from orders.models import Coupon


class Command(BaseCommand):
    help = "Seed discount coupons"

    def handle(self, *args, **options):
        coupons = [
            {"code": "SUMMER10", "discount_pct": 10},
            {"code": "WELCOME20", "discount_pct": 20},
        ]
        created = 0
        for c in coupons:
            obj, was_created = Coupon.objects.get_or_create(
                code=c["code"],
                defaults={"discount_pct": c["discount_pct"], "is_active": True}
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Done! {created} coupons created."))