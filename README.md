# Jina Jupyter Notebooks

This repo stores material for:

- Workshops
- Jupyter notebooks for posting to blog, elsewhere

## Notebook best practices

### Hosting/Sharing

- Create on your own Colab first
- Share the link early so we can see progress and get a feel for the content (be sure to enable public link - it's not public by default)
- When it's finished and checked, please store it in its own folder in this repo, under [notebooks](./notebooks). If it's specifically for DocArray, Jina core, Finetuner, etc, please store it in its own folder under the relevant project name in the notebooks folder (e.g. `notebooks/docarray/filtering`)

### Links

- Ensure lots of links to our docs/repos. This will help with docs and stars OKRs
- Use inline links where possible. e.g. `[DocArray](http://docarray.jina.ai/) is a library for...` rather than `DocArray is a library for... Learn more [here](http://docarray.jina.ai/)`
- Use a utm-source to help track where our traffic is coming from, e.g. `[DocArray](http://docarray.jina.ai?utm_source=notebook-docarray-filtering) is a library for...`. It should follow the format of `<medium>-<specific piece of content>`
- It's often easier to utm-sources *after* you've saved your notebook to a repo. That way you can run a vim command like `%s/\/)/?utm_source=notebook-foo)` in your notebook (which searches for the end of a markdown link like `/)` and adds the utm info)

### Content

- Introduce the tech stack you'll be using at the beginning
- Introduce the problem you'll be solving, and why this tech stack is a good fit for that problem
- Use consistent heading levels
- Add code comments to explain if the code isn't obvious
- Clear all unnecessary output before saving
- Include a section at the end about "next steps" e.g. visit learning portal, star the repo
- You may also want to check our [blogging best practices](https://medium.com/jina-ai/contribute-to-the-jina-blog-19853d453cf3)

### Code

- Don't hide cells that contain code that teach people how to use our products
- You can hide code cells that contain less relevant stuff
  - e.g. bespoke code for loading a specific dataset that wouldn't be useful in any other example
  - e.g. code to show images in a notebook which is generic and not useful outside notebook
- 

---

NOTE: The content is provided as-is. We don't guarantee compatibility with latest version of Jina or that bugs will be fixed. 

For support with Jina, contact us on Slack: https://slack.jina.ai/
