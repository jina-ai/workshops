# Jina Workshop @ TUM-AI: Image Search with Pokemons

[comment]: <> (TODO)
[TOC]

## Download and Extract Data

For this example we're using Pokemon sprites from [veekun.com](https://veekun.com/dex/downloads). To download them run:

```sh
sh ./get_data.sh
```

## Download and Extract Pretrained Model

In this example we use [BiT (Big Transfer) model](https://github.com/google-research/big_transfer), To download it:

```sh
sh ./download.sh
```

## Index Data

```sh
python app.py index
```

After this you should see a new `workspace` folder, which contains all the encoded data generated during indexing. 

## Parallelization

Notice how the `shards` parameter affects training. It creates parallel instances of the encoder to speed up the process.

For Indexers, it splits the data cross shards.

## Query Data

```sh
python app.py search
```

And then following:

 - You can use [Jinabox.js](https://jina.ai/jinabox.js/) to find the Pokemon which matches most clearly. Just set the endpoint to `http://127.0.0.1:45678/api/search` and drag from the thumbnails on the left or from your file manager.
 - Or you can `curl`/query/js it via HTTP POST request. [Details here](#query-via-rest-api). 

### Diving Deeper

Jina's REST API uses the [data URI scheme](https://en.wikipedia.org/wiki/Data_URI_scheme) to represent multimedia data. To query your indexed data, simply organize your picture(s) into this scheme and send a POST request to `http://0.0.0.0:45678/api/search`, e.g.:

```bash
curl --verbose --request POST -d '{"top_k": 10, "mode": "search",  "data": ["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAA2ElEQVR4nADIADf/AxWcWRUeCEeBO68T3u1qLWarHqMaxDnxhAEaLh0Ssu6ZGfnKcjP4CeDLoJok3o4aOPYAJocsjktZfo4Z7Q/WR1UTgppAAdguAhR+AUm9AnqRH2jgdBZ0R+kKxAFoAME32BL7fwQbcLzhw+dXMmY9BS9K8EarXyWLH8VYK1MACkxlLTY4Eh69XfjpROqjE7P0AeBx6DGmA8/lRRlTCmPkL196pC0aWBkVs2wyjqb/LABVYL8Xgeomjl3VtEMxAeaUrGvnIawVh/oBAAD///GwU6v3yCoVAAAAAElFTkSuQmCC", "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSncAAAA2ElEQVR4nADIADf/AvdGjTZeOlQq07xSYPgJjlWRwfWEBx2+CgAVrPrP+O5ghhOa+a0cocoWnaMJFAsBuCQCgiJOKDBcIQTiLieOrPD/cp/6iZ/Iu4HqAh5dGzggIQVJI3WqTxwVTDjs5XJOy38AlgHoaKgY+xJEXeFTyR7FOfF7JNWjs3b8evQE6B2dTDvQZx3n3Rz6rgOtVlaZRLvR9geCAxuY3G+0mepEAhrTISES3bwPWYYi48OUrQOc//IaJeij9xZGGmDIG9kc73fNI7eA8VMBAAD//0SxXMMT90UdAAAAAElFTkSuQmCC"]}' -H 'Content-Type: application/json' 'http://0.0.0.0:34567/api/search'
```

[JSON payload syntax and spec can be found in the docs](https://docs.jina.ai/chapters/restapi/#).

The above explains how to use a REST gateway, but by default Jina uses a gRPC gateway, which has much higher performance and richer features. Read our [documentation on Jina IO](https://docs.jina.ai/chapters/io/#) for more information.

## Changing Encoders

We can switch the `Encoder` easily.

`pods/encode.yml`:

```yaml
!ImageKerasEncoder
with:
  model_name: ResNet50V2 # any model could go here
  pool_strategy: avg
  channel_axis: -1
```

## Changing Crafters

In `pods/craft.yml`:

- remove `target_size: 96` from `ImageNormalizer`

```yaml
- !CenterImageCropper
with:
  target_size: 96
  channel_axis: -1
metas:
  name: img_cropper
```

We also need to specify the request paths, both for `IndexRequest` and for `SearchRequest`:

```yaml
      - !CraftDriver
        with:
          traversal_paths: ['r']
          executor: img_cropper
```

We can save an intermediary file to examine the cropped image to see if everything looks as expected. Add this to the `IndexRequest`:

```yaml
      - !PngToDiskDriver
        with:
          prefix: 'crop'
```

## License

Copyright (c) 2021 Jina AI Limited. All rights reserved.

Jina is licensed under the Apache License, Version 2.0. See [LICENSE](https://github.com/jina-ai/jina/blob/master/LICENSE) for the full license text.
