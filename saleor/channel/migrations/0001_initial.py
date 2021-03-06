# Generated by Django 3.0.6 on 2020-06-16 07:54

from django.conf import settings
from django.core.management.sql import emit_post_migrate_signal
from django.db import migrations, models


def assing_permissions(apps, schema_editor):
    # force post signal as permissions are created in post migrate signals
    # related Django issue https://code.djangoproject.com/ticket/23422
    emit_post_migrate_signal(2, False, "default")
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    manage_channels = Permission.objects.filter(
        codename="manage_channels", content_type__app_label="channel"
    ).first()
    for group in Group.objects.iterator():
        group.permissions.add(manage_channels)


def get_default_currency(Checkout, Order, Product, ShippingMethod, Voucher):
    latest_product = Product.objects.order_by("-pk").first()
    if latest_product:
        return latest_product.currency
    latest_voucher = Voucher.objects.order_by("-pk").first()
    if latest_voucher:
        return latest_voucher.currency
    latest_shipping_method = ShippingMethod.objects.order_by("-pk").first()
    if latest_shipping_method:
        return latest_shipping_method.currency
    latest_order = Order.objects.order_by("-pk").first()
    if latest_order:
        return latest_order.currency
    latest_checkout = Checkout.objects.order_by("-pk").first()
    if latest_checkout:
        return latest_checkout.currency
    return None


def create_default_channel(apps, schema_editor):
    Channel = apps.get_model("channel", "Channel")
    Checkout = apps.get_model("checkout", "Checkout")
    Order = apps.get_model("order", "Order")
    Product = apps.get_model("product", "Product")
    ShippingMethod = apps.get_model("shipping", "ShippingMethod")
    Voucher = apps.get_model("discount", "Voucher")

    default_currency = get_default_currency(
        Checkout, Order, Product, ShippingMethod, Voucher
    )
    if default_currency:
        Channel.objects.create(
            name="Default channel",
            slug=settings.DEFAULT_CHANNEL_SLUG,
            currency_code=default_currency,
            is_active=True,
        )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("checkout", "0025_auto_20200221_0257"),
        ("discount", "0019_auto_20200217_0350"),
        ("order", "0084_auto_20200522_0522"),
        ("product", "0118_populate_product_variant_price"),
        ("shipping", "0018_default_zones_countries"),
    ]

    operations = [
        migrations.CreateModel(
            name="Channel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                ("slug", models.SlugField(max_length=255, unique=True)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "currency_code",
                    models.CharField(max_length=settings.DEFAULT_CURRENCY_CODE_LENGTH),
                ),
            ],
            options={
                "ordering": ("slug",),
                "permissions": (("manage_channels", "Manage channels."),),
            },
        ),
        migrations.RunPython(create_default_channel, migrations.RunPython.noop),
        migrations.RunPython(assing_permissions, migrations.RunPython.noop),
    ]
