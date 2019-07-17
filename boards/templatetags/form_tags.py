from django import template

register = template.Library()

@register.filter
def field_type(bound_field):
    return bound_field.field.widget.__class__.__name__

@register.filter
def input_class(bound_field):
    css_class = ''
    if bound_field.form.is_bound:
        if bound_field.errors:
            css_class = 'invalid'
        elif field_type(bound_field) != 'PasswordInput':
            css_class = 'valid'

    return f'form-control {css_class}'