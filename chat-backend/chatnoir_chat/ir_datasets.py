from django.http import HttpRequest, JsonResponse

IRDS_ALLOW_LIST = set([
    'antique/test', 'cranfield', 'argsme/2020-04-01/touche-2020-task-1', 'argsme/2020-04-01/touche-2021-task-1',
    'clueweb09/en/trec-web-2009', 'clueweb09/en/trec-web-2010', 'clueweb09/en/trec-web-2011',
    'clueweb09/en/trec-web-2012', 'clueweb12/touche-2020-task-2', 'clueweb12/touche-2021-task-2',
    'clueweb12/touche-2022-task-2', 'clueweb12/trec-web-2013', 'clueweb12/trec-web-2014',
    'cord19/trec-covid', 'disks45/nocr/trec-robust-2004', 'disks45/nocr/trec7',
    'disks45/nocr/trec8', 'gov2/trec-tb-2004', 'gov2/trec-tb-2005', 'gov2/trec-tb-2006',
    'msmarco-passage/trec-dl-2019/judged', 'msmarco-passage/trec-dl-2020/judged',
    'msmarco-passage/trec-dl-hard ', 'msmarco-passage-v2/trec-dl-2021/judged',
    'msmarco-passage-v2/trec-dl-2022/judged', 'nfcorpus/test', 'trec-cast/v1/2019/judged',
    'trec-tot/2023/dev', 'trec-cast/v1/2020/judged'])

def docs(request: HttpRequest):
    import ir_datasets
    d = ir_datasets.load(request.GET['ir_dataset_id'])
    ret = d.docs_store().get(str(request.GET['doc_id']))

    return JsonResponse({'text': ret.default_text()})

def topic_description(request: HttpRequest):
    import ir_datasets
    d = ir_datasets.load(request.GET['ir_dataset_id'])
    selected_topic_num = request.GET['topic_num']

    for q in d.queries_iter():
        if selected_topic_num and str(selected_topic_num) == str(q.query_id):
            ret = {'query_id': q.query_id, 'title': q.default_text(), 'description': '', 'narrative': ''}

            try:
                ret['description'] =  q.description
                ret['narrative'] = q.narrative
            except:
                pass

            qrels = []

            for i in d.qrels_iter():
                if str(i.query_id) == str(selected_topic_num) and i.relevance > 0:
                    qrels += [{'Document': i.doc_id, 'Relevance': i.relevance}]

            ret['qrels'] = sorted(qrels, key=lambda i: i['Relevance'], reverse=True)
            
            return JsonResponse(ret)

def ir_datasets(request: HttpRequest):
    import ir_datasets
    datasets_with_topics = []

    for irds_id, irds_obj in ir_datasets.registry._registered.items():
        if irds_id in IRDS_ALLOW_LIST and 'queries_iter' in dir(irds_obj) and 'metadata'in dir(irds_obj):
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