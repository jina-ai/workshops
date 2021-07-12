from jina import Flow, DocumentArray, Document


def main():
    docs = DocumentArray()
    docs.append(Document(content='hello world'))                # creating documents
    docs.append(Document(content='hello Berlin'))
    docs.append(Document(content='hello Jina'))

    flow = Flow().add(                                          # provide as class name or jinahub+docker URI
        uses='jinahub+docker://ie1obzm9:980d90f35cf31adf35c805e69c63e68c',
        override_with={                                         # RequestLogger arguments
            'default_log_docs': 1
        },
        volumes='workspace:/abc',                               # mapping local folders to docker instance folders
        override_metas={                                        # Executor (parent class) arguments
            'workspace': '/abc',                                # this should match the above
        },
    )

    with flow as f:                                             # Flow is a context manager
        f.post(
            on='/index',                                        # the endpoint
            inputs=docs,                                        # the documents we send as input
        )

    with flow as f:                                             # Flow is a context manager
        f.post(
            on='/index',                                        # the endpoint
            inputs=docs,                                        # the documents we send as input
            parameters={'log_docs': 2}                          # parameters for this request
        )


if __name__ == '__main__':
    main()
