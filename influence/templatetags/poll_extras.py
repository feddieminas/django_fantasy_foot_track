from django import template
register = template.Library()

@register.filter()
def hash(h, key): 
    return h, key
    
@register.filter()
def hash2(hash, key2):
    h, key = hash
    return h[key][key2]    