from django import template 

register = template.Library()


def lookup(somedictionary, somekey):
    #return 77
    return somedictionary.get(somekey, None)

def default_if_zero(x):
    if x==0 or x=='0':
        return ''
    else:
        return x

register.filter('lookup', lookup)
register.filter('default_if_zero', default_if_zero)