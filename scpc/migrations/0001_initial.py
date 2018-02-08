# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.blocks
import wagtail.wagtailimages.blocks
import scpc.models
import django.db.models.deletion
import modelcluster.fields
import wagtail.wagtailcore.fields
import django.core.validators
import wagtail.wagtailsnippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('wagtailimages', '0018_remove_rendition_filter'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUsLeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=32)),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
                ('twitter_url', models.URLField(null=True, blank=True)),
                ('facebook_url', models.URLField(null=True, blank=True)),
                ('instagram_url', models.URLField(null=True, blank=True)),
                ('bio', wagtail.wagtailcore.fields.RichTextField(null=True, blank=True)),
                ('image', models.ForeignKey(to='wagtailimages.Image', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, related_name='+')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AboutUsPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
                ('menu_title', models.CharField(help_text='An alternate page title to be used in automatically generated menus', null=True, max_length=12, blank=True)),
                ('hero_align', models.CharField(help_text='Aligns the image vertically', verbose_name='Alignment', default='middle', max_length=6, choices=[('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom')])),
                ('hero_y', models.PositiveSmallIntegerField(help_text='The vertical position to align to the middle of the container (middle alignment only)', verbose_name='Y', default=50)),
                ('introduction', models.TextField()),
                ('vision_header', models.CharField(max_length=32)),
                ('vision_intro', wagtail.wagtailcore.fields.RichTextField()),
                ('profiles_header', models.CharField(verbose_name='Divider', max_length=25)),
                ('staff_header', models.CharField(max_length=25)),
                ('hero_image', models.ForeignKey(to='wagtailimages.Image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='AboutUsStaff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('name', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=32)),
                ('email', models.EmailField(null=True, max_length=254, blank=True)),
                ('image', models.ForeignKey(to='wagtailimages.Image', null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, related_name='+')),
                ('page', modelcluster.fields.ParentalKey(to='scpc.AboutUsPage', related_name='staff')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AboutUsVision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('image_src', models.CharField(help_text='For icon images we use the SVG format and SVGs cannot be uploaded here. This path must refer to an SVG which already exists. Modifying the icon requires changing the raw file externally from Wagtail.', verbose_name='Icon Path', max_length=50)),
                ('header', models.CharField(max_length=25)),
                ('content', models.TextField(max_length=200)),
                ('page', modelcluster.fields.ParentalKey(to='scpc.AboutUsPage', related_name='vision_statement')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AddressBookSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('facebook_url', models.URLField(verbose_name='Facebook')),
                ('twitter_url', models.URLField(verbose_name='Twitter')),
                ('instagram_url', models.URLField(verbose_name='Instagram')),
                ('location_name', models.CharField(verbose_name='Name', max_length=50)),
                ('location_street', models.CharField(verbose_name='Street', max_length=22)),
                ('location_city', models.CharField(verbose_name='City, State, Zip', max_length=22)),
                ('directions_url', models.URLField(verbose_name='Google Maps')),
                ('mailing_name', models.CharField(verbose_name='Name', null=True, max_length=50, blank=True)),
                ('mailing_street', models.CharField(verbose_name='Street', null=True, max_length=22, blank=True)),
                ('mailing_city', models.CharField(verbose_name='City, State, Zip', null=True, max_length=22, blank=True)),
                ('email', models.EmailField(null=True, max_length=254)),
                ('phone_number', models.CharField(verbose_name='Phone', null=True, max_length=23, validators=[django.core.validators.RegexValidator(message='Phone numbers should contain only digits and optional delimiters.', regex='^(\\+1 )?[()0-9-. ]{9,20}$')], blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='BeliefsDoctrine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('sort_order', models.IntegerField(null=True, blank=True, editable=False)),
                ('header', models.CharField(max_length=25)),
                ('content', models.TextField(max_length=200)),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BeliefsPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
                ('menu_title', models.CharField(help_text='An alternate page title to be used in automatically generated menus', null=True, max_length=12, blank=True)),
                ('hero_align', models.CharField(help_text='Aligns the image vertically', verbose_name='Alignment', default='middle', max_length=6, choices=[('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom')])),
                ('hero_y', models.PositiveSmallIntegerField(help_text='The vertical position to align to the middle of the container (middle alignment only)', verbose_name='Y', default=50)),
                ('introduction', models.TextField()),
                ('gospel_header', models.CharField(max_length=25)),
                ('gospel_content', wagtail.wagtailcore.fields.RichTextField()),
                ('doctrines_header', models.CharField(max_length=32)),
                ('doctrines_intro', wagtail.wagtailcore.fields.RichTextField()),
                ('hero_image', models.ForeignKey(to='wagtailimages.Image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='FooterSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('contact_info', models.ForeignKey(to='scpc.AddressBookSnippet', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
        ),
        migrations.CreateModel(
            name='GivingPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
                ('menu_title', models.CharField(help_text='An alternate page title to be used in automatically generated menus', null=True, max_length=12, blank=True)),
                ('hero_align', models.CharField(help_text='Aligns the image vertically', verbose_name='Alignment', default='middle', max_length=6, choices=[('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom')])),
                ('hero_y', models.PositiveSmallIntegerField(help_text='The vertical position to align to the middle of the container (middle alignment only)', verbose_name='Y', default=50)),
                ('introduction', wagtail.wagtailcore.fields.RichTextField()),
                ('giving_content', wagtail.wagtailcore.fields.RichTextField()),
                ('online_link_name', models.CharField(max_length=15)),
                ('online_link_url', models.URLField()),
                ('mail_header', models.CharField(max_length=32)),
                ('contact_info', models.ForeignKey(to='scpc.AddressBookSnippet', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
                ('hero_image', models.ForeignKey(to='wagtailimages.Image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='HomePage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
                ('content', wagtail.wagtailcore.fields.StreamField((('location', wagtail.wagtailcore.blocks.StructBlock((('contact_info', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(target_model='scpc.AddressBookSnippet')), ('time', wagtail.wagtailcore.blocks.CharBlock(max_length=25)), ('content', wagtail.wagtailcore.blocks.RichTextBlock())))), ('text', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('header', wagtail.wagtailcore.blocks.CharBlock(help_text="The site-wide style for headers is to use sentence case (not title case). Try not to capitalize words unless you'd normally do so in a sentence.", required=False, max_length=32)), ('subheader', wagtail.wagtailcore.blocks.CharBlock(required=False, max_length=32)), ('content', wagtail.wagtailcore.blocks.RichTextBlock())))), ('verse', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(template='scpc/blocks/verse.html', target_model='scpc.VerseSnippet'))), blank=True)),
                ('subtitle', models.CharField(max_length=35)),
                ('introduction', wagtail.wagtailcore.fields.RichTextField()),
            ],
            options={
                'verbose_name': 'homepage',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='MinistriesPage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
                ('menu_title', models.CharField(help_text='An alternate page title to be used in automatically generated menus', null=True, max_length=12, blank=True)),
                ('hero_align', models.CharField(help_text='Aligns the image vertically', verbose_name='Alignment', default='middle', max_length=6, choices=[('top', 'Top'), ('middle', 'Middle'), ('bottom', 'Bottom')])),
                ('hero_y', models.PositiveSmallIntegerField(help_text='The vertical position to align to the middle of the container (middle alignment only)', verbose_name='Y', default=50)),
                ('content', wagtail.wagtailcore.fields.StreamField((('children', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('header', wagtail.wagtailcore.blocks.CharBlock(help_text="The site-wide style for headers is to use sentence case (not title case). Try not to capitalize words unless you'd normally do so in a sentence.", required=False, max_length=32)), ('subheader', wagtail.wagtailcore.blocks.CharBlock(required=False, max_length=32)), ('content', wagtail.wagtailcore.blocks.RichTextBlock())))), ('youth', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('header', wagtail.wagtailcore.blocks.CharBlock(help_text="The site-wide style for headers is to use sentence case (not title case). Try not to capitalize words unless you'd normally do so in a sentence.", required=False, max_length=32)), ('subheader', wagtail.wagtailcore.blocks.CharBlock(required=False, max_length=32)), ('content', wagtail.wagtailcore.blocks.RichTextBlock())))), ('life_groups', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('header', wagtail.wagtailcore.blocks.CharBlock(help_text="The site-wide style for headers is to use sentence case (not title case). Try not to capitalize words unless you'd normally do so in a sentence.", required=False, max_length=32)), ('subheader', wagtail.wagtailcore.blocks.CharBlock(required=False, max_length=32)), ('content', wagtail.wagtailcore.blocks.RichTextBlock()), ('groups', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('day', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('Sundays', 'Sundays'), ('Mondays', 'Mondays'), ('Tuesdays', 'Tuesdays'), ('Wednesdays', 'Wednesdays'), ('Thursdays', 'Thursdays'), ('Fridays', 'Fridays'), ('Saturdays', 'Saturdays')])), ('time', wagtail.wagtailcore.blocks.CharBlock(help_text='Try to stick to the format "HH-HHpm".', max_length=12)), ('region', wagtail.wagtailcore.blocks.CharBlock(help_text='This should be a commonly-recognized area of Charlotte.', max_length=25)), ('location', wagtail.wagtailcore.blocks.CharBlock(help_text='This should be a nearby intersection or well-known neighborhood.', max_length=32)), ('childcare_policy', wagtail.wagtailcore.blocks.TextBlock()), ('map', wagtail.wagtailcore.blocks.StructBlock((('query', wagtail.wagtailcore.blocks.CharBlock(help_text='This is used both for creating a static map image and for auto-filling the search box when this static map is clicked. If Google Maps is unable to reverse-geocode this query to a single location, latitude and longitude coordinates can be provided below to center the static map.')), ('zoom', wagtail.wagtailcore.blocks.IntegerBlock(help_text='See https://developers.google.com/maps/documentation/static-maps/intro #Zoomlevels. The default zoom is 12.', max_value=20, required=False, min_value=1)), ('latitude', wagtail.wagtailcore.blocks.CharBlock(label='Lat.', required=False)), ('longitude', wagtail.wagtailcore.blocks.CharBlock(label='Long.', required=False))), template='scpc/blocks/lifegroups/map.html')))))))))))),
                ('hero_image', models.ForeignKey(to='wagtailimages.Image', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='StyleGuidePage',
            fields=[
                ('page_ptr', models.OneToOneField(to='wagtailcore.Page', primary_key=True, auto_created=True, serialize=False, parent_link=True)),
                ('sections', wagtail.wagtailcore.fields.StreamField((('text', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('header', wagtail.wagtailcore.blocks.CharBlock(help_text="The site-wide style for headers is to use sentence case (not title case). Try not to capitalize words unless you'd normally do so in a sentence.", required=False, max_length=32)), ('subheader', wagtail.wagtailcore.blocks.CharBlock(required=False, max_length=32)), ('content', wagtail.wagtailcore.blocks.RichTextBlock())))),), blank=True)),
                ('custom', wagtail.wagtailcore.fields.StreamField((('location', wagtail.wagtailcore.blocks.StructBlock((('contact_info', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(target_model='scpc.AddressBookSnippet')), ('time', wagtail.wagtailcore.blocks.CharBlock(max_length=25)), ('content', wagtail.wagtailcore.blocks.RichTextBlock())))), ('life_groups', wagtail.wagtailcore.blocks.StructBlock((('image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=False)), ('header', wagtail.wagtailcore.blocks.CharBlock(help_text="The site-wide style for headers is to use sentence case (not title case). Try not to capitalize words unless you'd normally do so in a sentence.", required=False, max_length=32)), ('subheader', wagtail.wagtailcore.blocks.CharBlock(required=False, max_length=32)), ('content', wagtail.wagtailcore.blocks.RichTextBlock()), ('groups', wagtail.wagtailcore.blocks.ListBlock(wagtail.wagtailcore.blocks.StructBlock((('day', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('Sundays', 'Sundays'), ('Mondays', 'Mondays'), ('Tuesdays', 'Tuesdays'), ('Wednesdays', 'Wednesdays'), ('Thursdays', 'Thursdays'), ('Fridays', 'Fridays'), ('Saturdays', 'Saturdays')])), ('time', wagtail.wagtailcore.blocks.CharBlock(help_text='Try to stick to the format "HH-HHpm".', max_length=12)), ('region', wagtail.wagtailcore.blocks.CharBlock(help_text='This should be a commonly-recognized area of Charlotte.', max_length=25)), ('location', wagtail.wagtailcore.blocks.CharBlock(help_text='This should be a nearby intersection or well-known neighborhood.', max_length=32)), ('childcare_policy', wagtail.wagtailcore.blocks.TextBlock()), ('map', wagtail.wagtailcore.blocks.StructBlock((('query', wagtail.wagtailcore.blocks.CharBlock(help_text='This is used both for creating a static map image and for auto-filling the search box when this static map is clicked. If Google Maps is unable to reverse-geocode this query to a single location, latitude and longitude coordinates can be provided below to center the static map.')), ('zoom', wagtail.wagtailcore.blocks.IntegerBlock(help_text='See https://developers.google.com/maps/documentation/static-maps/intro #Zoomlevels. The default zoom is 12.', max_value=20, required=False, min_value=1)), ('latitude', wagtail.wagtailcore.blocks.CharBlock(label='Lat.', required=False)), ('longitude', wagtail.wagtailcore.blocks.CharBlock(label='Long.', required=False))), template='scpc/blocks/lifegroups/map.html'))))))))), ('divider', scpc.models.DividerBlock()), ('verse', wagtail.wagtailsnippets.blocks.SnippetChooserBlock(template='scpc/blocks/verse.html', target_model='scpc.VerseSnippet'))), blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='VerseSnippet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('passage', models.TextField(max_length=750)),
                ('verse', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='beliefsdoctrine',
            name='page',
            field=modelcluster.fields.ParentalKey(to='scpc.BeliefsPage', related_name='doctrines'),
        ),
        migrations.AddField(
            model_name='aboutusleader',
            name='page',
            field=modelcluster.fields.ParentalKey(to='scpc.AboutUsPage', related_name='leadership'),
        ),
    ]
