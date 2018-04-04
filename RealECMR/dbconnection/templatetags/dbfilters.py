from django import template

register = template.Library()


@register.filter
def extraKeyValue(dict, key):
    return dict['ca'+str(key)]

@register.filter
def arrayObject(array, index):
    return array[index]

@register.filter
def makeArray(formSet):
    arr = []
    for form in formSet:
        arr.append(form.as_p())
    return arr

@register.filter
def extraValues(objectList, camposAdicionales):
    arr = []
    for prop in objectList:
        propDict = {}
        for camp in camposAdicionales:
            cId = 'ca'+str(camp['id'])
            if prop[cId] != None:
                propDict[cId] = prop[cId]
            else:
                propDict[cId] = ''
        arr.append(propDict)
    return(arr)
