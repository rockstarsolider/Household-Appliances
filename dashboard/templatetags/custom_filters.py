from django import template  

register = template.Library()  

@register.filter  
def with_commas(value):  
    """Converts a number to string with commas as thousands separator."""  
    if value is None:  
        return ''  
    try:  
        return f"{int(value):,}"  
    except (ValueError, TypeError):  
        return value  # Return the original value if conversion fails