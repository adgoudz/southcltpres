from django.utils.safestring import mark_safe


def static_label(label):
    return mark_safe('<label style="width: 14%">{label}:</label> '
                     '<p style="font-size: 1.1em; padding-top: 1.2em; padding-bottom: 0.8em;">'
                     'This section cannot be configured.</p>'.format(label=label))
