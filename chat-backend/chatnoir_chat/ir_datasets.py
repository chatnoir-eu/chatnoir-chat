from django.http import HttpRequest, JsonResponse

def ir_datasets(request: HttpRequest):
    import ir_datasets
    datasets_with_topics = []

    for irds_id, irds_obj in ir_datasets.registry._registered.items():
        if 'queries_iter' in dir(irds_obj) and 'metadata'in dir(irds_obj):
            metadata = irds_obj.metadata()
            if 'queries' in metadata and 'count' in metadata['queries'] and metadata['queries']['count'] < 500:
                datasets_with_topics += [irds_id]

    ret = {'ir_datasets': datasets_with_topics}
    selected_topic_num = request.GET.get('topic_id', None)
    selected_topic = {}
    available_topics = []

    try:
        d = ir_datasets.load(request.GET['id'])
        for q in d.queries_iter():
            available_topics += [{'id': q.query_id, 'title': q.default_text() + ' ( Topic ' + str(q.query_id) + ')'}]
            if selected_topic_num and str(selected_topic_num) == str(q.query_id):
                try:
                    selected_topic = {'query_id': q.query_id, 'title': q.title, 'description': q.description, 'narrative': q.narrative}
                except: pass

    except:
        pass

    ret['available_topics'] = available_topics
    ret['topic_details'] = selected_topic
    return JsonResponse(ret)