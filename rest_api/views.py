import json
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.apps import apps


DefaultLimit = 20

def get_models():
    out = {}
    for model in apps.get_models():
        if not model._meta.app_label in out:
            out[model._meta.app_label] = {}
        out[model._meta.app_label][model.__name__] = model
    return out

def index(request):
    out = "<H1>Протокол запросов:</H1>\n"
    out += " - <b>Получить запись по индексу</b></br>\n"
    out += "   GET /rest_api/%Project_name%/%Model_name%/%id%/ </br>\n"
    out += "</br>\n"
    out += " - <b>Найти записи по полям. Сортировка по ключу order-by. Кол-во записей на странице по плючу limit</b></br>\n"
    out += "   GET /rest_api/%Project_name%/%Model_name%/?order-by=field1,-field2&limit=23&page=0&field1=72 </br>\n"
    out += "</br>\n"
    out += " - <b>Добавление записи, данные в формате JSON</b></br>\n"
    out += "   POST /rest_api/%Project_name%/%Model_name%/ </br>\n"
    out += "</br>\n"
    out += " - <b>Изменение запись по индексу, данные в формате JSON</b></br>\n"
    out += "   PUT /rest_api/%Project_name%/%Model_name%/%id%/ </br>\n"
    out += "</br>\n"
    out += " - <b>Удаление записи по индексу</b></br>\n"
    out += "   DELETE /rest_api/%Project_name%/%Model_name%/%id%/ </br>\n"
    out += "</br>\n"
    out += "| <b>Project_name</b> / <b>Model_name</b> |</br>\n"
    for model in apps.get_models():
        out += "| {} / {} |</br>\n".format(model._meta.app_label, model.__name__)
    return HttpResponse(out)

def req_args(req, model):
    args = {}
    obj = model.objects.first()
    if not obj:
        return {}
    for k in obj._meta.fields:
        v = req.get(k.name, None)
        if v is not None:
            args[k.name] = v
    return args

def api(request, app_name, model_name, oid=None, *args, **kwargs):
    oid = int(oid) if oid else None
    try:
        model = apps.get_model(app_name, model_name)
    except LookupError:
        return HttpResponseBadRequest("No such app or model")
    data = None
    if request.body:
        try:
            data = json.loads(request.body)
        except JSONDecodeError:
            return HttpResponseBadRequest("Body JSON format error")
    resp = []

    if request.method == 'GET':
        if oid is not None:
            resp = model.objects.filter(pk=oid).values()[0]
            return JsonResponse(resp)
        else:
            order_by = [x.strip() for x in request.GET.get("order-by", '').split(',') if x.strip()]
            limit = int(request.GET.get("limit", DefaultLimit))
            shift = int(request.GET.get("page", 0)) * limit
            filters = req_args(request.GET, model)
            try:
                vals = model.objects.filter(**filters).order_by(*order_by).values()[shift:shift+limit]
                resp = dict(zip(range(shift, shift+len(vals)), vals))
            except Exception as e:
                return HttpResponseBadRequest(str(e))
            return JsonResponse(resp)
    elif request.method == 'POST' and oid is None:
        if not data:
            return HttpResponseBadRequest("No JSON body")
        if isinstance(data, dict):
            data = [data]
        elif not isinstance(data, list):
            return HttpResponseBadRequest("Body must be JSON-dict or JSON-list-of-dicts")
        for d in data:
            try:
                obj, ok = model.objects.get_or_create(**d)
                if ok:
                    resp += [obj]
            except Exception as e:
                return HttpResponseBadRequest("Can`t add {} {}: {}\n".format(model_name, d, e))
        return JsonResponse({"records_added": len(resp)})
    elif request.method == 'PUT' and oid is not None:
        if not isinstance(data, dict):
            return HttpResponseBadRequest("Body must be JSON-dict")
        obj = model.objects.filter(pk=oid)
        obj.update(**data)
        return JsonResponse({"records_updated": len(obj)})
    elif request.method == 'DELETE' and oid is not None:
        obj = model.objects.filter(pk=oid)
        resp = {"records_deleted": len(obj)}
        obj.delete()
        return JsonResponse(resp)

    return HttpResponseBadRequest("")

