# Generated by Django 3.2.23 on 2024-03-13 14:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0045_alter_item_item_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemcategory',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_family', to='inventory.itemfamily'),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='type_category', to='inventory.itemcategory'),
        ),
    ]
