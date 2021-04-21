# Instructions

To run the server locally, (optionally) create a new Python virtualenv of your preferred flavor and install the dependencies.

```shell
pip install -r requirements
```

You can then run the server with:

```shell
uvicorn --reload --port=8000 main:app
```

## Example queries:

-   To get an HTML response:

    ```shell
    curl http://localhost:8000/2021/04/marda-dd/test\#helloWorld
    ```

    or alternatively just visit http://localhost:8000/2021/04/marda-dd/test\#helloWorld in your browser with the server running.

-   To get responses in an RDF format:

    ```shell
    curl -H "Accept: text/turtle" http://localhost:8000/2021/04/marda-dd/test\#helloWorld
    ```

    where `text/turtle` can be replaced with any [rdflib-compatible format or mime-type](https://rdflib.readthedocs.io/en/stable/plugin_serializers.html), e.g., `application/rdf+xml`, `nquads`.
