import glob
import os
from jina import Document
from jina.optimizers.flow_runner import SingleFlowRunner, MultiFlowRunner


def get_id(filename):
    return filename.split('/')[-1].split('.')[0]


def print_callback(request):
    correct = 0
    total = 0
    for doc in request.search.docs:
        total += 1
        print(get_id(doc.uri), get_id(str(doc.matches[0].tags.fields['filename'])))
        if get_id(doc.uri) == get_id(str(doc.matches[0].tags.fields['filename'])):
            correct += 1
    print(f'correct: {correct}, total: {total}')


def get_input_iterator(edition, full_document):
    image_src = f'data/pokemon/main-sprites/{edition}/*.png'
    for filename in glob.iglob(image_src, recursive=True):
        if full_document:
            with open(filename, 'rb') as fp:
                yield Document(buffer=fp.read(), tags={'filename': filename})
        else:
            yield filename


def get_flows():
    index_flow = SingleFlowRunner(
        flow_yaml='flows/index.yml',
        documents=get_input_iterator('red-blue', True),
        request_size=64,
        execution_method='index',
        overwrite_workspace=True
    )

    search_flow = SingleFlowRunner(
        flow_yaml='flows/query.yml',
        documents=get_input_iterator('red-green', False),
        request_size=64,
        execution_method='search'
    )

    multi_flow = MultiFlowRunner([index_flow, search_flow])
    multi_flow.run({}, callback=print_callback)


def config():
    os.environ['JINA_SHARDS'] = str(1)
    os.environ['JINA_SHARDS_INDEXERS'] = str(1)
    os.environ['JINA_WORKSPACE'] = './workspace'
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))


def main():
    config()
    get_flows()


if __name__ == '__main__':
    main()
