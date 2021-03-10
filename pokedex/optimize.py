import glob
import os
from jina import Document
from jina.optimizers.flow_runner import SingleFlowRunner, MultiFlowRunner
from jina.optimizers import FlowOptimizer, MeanEvaluationCallback


def get_id(filename):
    return filename.split('/')[-1].split('.')[0]


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
        flow_yaml='flows/index_opt.yml',
        documents=get_input_iterator('red-blue', True),
        request_size=64,
        execution_method='index',
        overwrite_workspace=True
    )

    search_flow = SingleFlowRunner(
        flow_yaml='flows/query_opt.yml',
        documents=get_input_iterator('red-green', False),
        request_size=64,
        execution_method='search'
    )

    multi_flow = MultiFlowRunner([index_flow, search_flow])
    return multi_flow


def config():
    os.environ['JINA_SHARDS'] = str(1)
    os.environ['JINA_SHARDS_INDEXERS'] = str(1)
    os.environ['JINA_PORT'] = os.environ.get('JINA_PORT', str(45678))


class PokemonCallback(MeanEvaluationCallback):
    """TODO: document why is this here and no Evaluator in place."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._eval_name = "pokedex_eval"

    def get_empty_copy(self):
        return PokemonCallback(self._eval_name)

    def __call__(self, response):
        self._n_docs += len(response.search.docs)
        for doc in response.search.docs:
            if doc.matches:
                if get_id(doc.uri) == get_id(str(doc.matches[0].tags.fields['filename'])):
                    self._evaluation_values[self._eval_name] += 1


def optimize(flows):
    optimizer = FlowOptimizer(
        flow_runner=flows,
        parameter_yaml='optimize/parameters.yml',
        evaluation_callback=PokemonCallback(eval_name='correct'),
        workspace_base_dir='workspace',
        n_trials=20,
        sampler='RandomSampler'
    )
    result = optimizer.optimize_flow()
    result.save_parameters('optimize/best_config.yml')


def main():
    config()
    flows = get_flows()
    optimize(flows)


if __name__ == '__main__':
    main()
