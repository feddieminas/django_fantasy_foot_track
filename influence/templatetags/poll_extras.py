from django import template
register = template.Library()

# register filters to be able to access inner dicts (created from the views) to the frontend 

@register.filter()
def hash(h, key): 
    return h, key
    
@register.filter()
def hash2(hash, key2):
    h, key = hash
    return h[key][key2]    