from django import template

register = template.Library()


@register.filter
def extraKeyValue(dict, key):
    return dict['ca'+str(key)]

@register.filter
def arrayObject(array, index):
    return array[index]

@register.filter
def makeDict(formSet, objectList):
    dic = {}
    counter = 0
    for form in formSet:
        dicKey = objectList[counter]['id']
        dic[dicKey] = form.as_p()
        counter += 1
    return dic

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

@register.filter
def genImage(imageData):
    data_uri = imageData.replace('\n', '')
    img_tag = '<img src="data:image/png;base64,{0}"/>'.format(data_uri)
    return img_tag

@register.filter
def getName(objectList, objectID):
    for obj in objectList:
        if obj['id'] == objectID:
            return obj['nombre']
    return None

@register.filter
def getTipo(objectList, objectID):
    for obj in objectList:
        if obj['id'] == objectID:
            return obj['tipo']
    return None

@register.filter
def getDireccion(objectList, objectID):
    for obj in objectList:
        if obj['id'] == objectID:
            return obj['direccion']
    return None

@register.filter
def getIntermediario(objectList, objectID):
    for obj in objectList:
        if obj['id'] == objectID:
            return obj['intermediario_id']
    return None

@register.filter
def getTamano(objectList, objectID):
    for obj in objectList:
        if obj['id'] == objectID:
            return obj['tamano']
    return None
    
