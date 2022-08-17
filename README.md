# Jina Notebooks

At Jina we create a lot of different types of content. One of these is [notebooks](https://www.nature.com/articles/d41586-018-07196-1) which let users read, write and run code in their browser, accompanied by instructional text. This lets them get hands-on with the Jina codebase and see the results without having to download stuff to their own machines.

## Jupyter or Colab or Kaggle?

There are many different providers of notebooks, but they're all based (as far as the writer knows) on Jupyter. We recommend using [Google Colab](https://research.google.com/colaboratory/) because:

- It has free GPU allowance - this is good if you need to generate embeddings or run deep learning algorithms
- It is flexible about opening ports (unlike, say, [Kaggle](https://kaggle.com/))
- It doesn't require you to run anything on your own machine (unlike [Jupyter](https://jupyter.org/), which you download, run, then open in your browser)
- It's well-known, so more folks are familiar with it
- [This](https://www.kaggle.com/general/130391)

### Why not just author it in Jupyter on your own machine and save directly in a repo branch?

- In Colab you can share progress and give others access easily. Especially when you're getting started with Jina or notebooks, check early with dev rel, and check often.
- Jupyter runs on your machine, which may have it's own interesting quirks. Since most people will use the notebook in Colab *anyway* we recommend authoring there.

### Colab Caveats

- There is no way (that we know of) to track who opens or runs a notebook, or any way to know that package downloads came from a notebook or elsewhere (though in Colab, they all fall under `without_mirrors`)
- Colab can be a bit of a pain sometimes, needing runtime restarts or even outright runtime deletions (don't worry - this doesn't affect your notebook itself)
- Google is legendary for sun-setting their offerings, so we also export them to our own repo once ready.

## Working with notebooks

1. Create a [new notebook](https://colab.research.google.com/#create=true)
2. Refer to our best practices below when authoring your notebook
3. Once done, run it past Jina's dev rel team so we can give it a spin!
4. When all is good, download it from Colab and push to our [workshops repo](https://github.com/jina-ai/workshops)
5. Re-import it into Colab from the workshops repo. This ensures we're all working with a single source of truth and other folks can easily fork it as they would any other OSS project.

![](./.github/images/colab_import.png)

## Hosting/Sharing

- Create on your own Colab first
- Share the link with Jina dev rel early so we can see progress and get a feel for the content (be sure to enable public link - it's not public by default)
- When it's finished and checked, please store it in its own folder in this repo, under [notebooks](./notebooks). If it's specifically for DocArray, Jina core, Finetuner, etc, please store it in its own folder under the relevant project name in the notebooks folder (e.g. `notebooks/docarray/filtering`)

## Content

- Introduce the tech stack you'll be using at the beginning
- Introduce the problem you'll be solving, and why this tech stack is a good fit for that problem
- Use consistent heading levels
- Add code comments to explain if the code isn't obvious
- Clear all unnecessary output before saving
- Include a section at the end about "next steps" e.g. visit learning portal, star the repo
- If you're mentioning Colab, remember it's "Google Colab" with one `l`. Not Collab, Colllllab or Colllllllllab.
- You may also want to check our [blogging best practices](https://medium.com/jina-ai/contribute-to-the-jina-blog-19853d453cf3)

## Links

- Ensure lots of links to our docs/repos. This will help drive more users to Jina :smile:
- Use inline links where possible. e.g. `[DocArray](http://docarray.jina.ai/) is a library for...` rather than `DocArray is a library for... Learn more [here](http://docarray.jina.ai/)`
- Use a [utm-source](https://buffer.com/library/utm-guide/) to help track where our traffic is coming from, e.g. `[DocArray](http://docarray.jina.ai?utm_source=notebook-docarray-filtering) is a library for...`. It should follow the format of `<medium>-<specific piece of content>`
- It's often easier to utm-sources *after* you've saved your notebook to a repo. That way you can run a vim command like `%s/\/)/?utm_source=notebook-foo)` in your notebook (which searches for the end of a markdown link like `/)` and adds the utm info)

## Code

- For a nicer notebook experience (more native progress bars, etc), `!pip install ipywidgets` (no need to import)
- Don't hide cells that contain code that teach people how to use Jina's ecosystem
- You can hide code cells that contain less relevant stuff
  - e.g. bespoke code for loading a specific dataset that wouldn't be useful in any other example
  - e.g. code to show images in a notebook which is generic and not useful outside notebook
- Remember, Colab doesn't save state or get other files from the repo except your notebook. So you'll either need to `!wget <somewhere>/requirements.txt` or `!pip install <dependencies>` in the notebook itself.
- If you have a lot of helper functions, create a `helper.py` and `!wget` it
- To not overflow your notebook with terminal output (when using CLI) commands, tell them to [stfu](https://gist.github.com/alexcg1/6e6718c43761d68b7404ec4aa8a0ca59)
