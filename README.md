![NGINX Unit Logo](unitlogo.svg)

# NGINX Unit Documentation

This is the source code for [NGINX Unit](https://github.com/nginx/unit/)'s
official website, written in
[reStructuredText](https://en.wikipedia.org/wiki/ReStructuredText) and built
with the [Sphinx](https://www.sphinx-doc.org/en/master/) generator.

## Development

To run a local version of the website:

```shell
git clone https://github.com/nginx/unit-docs && cd unit-docs
pip install -r requirements.txt
make serve
```

Commits in any branch associated with a Pull Request, if made by a maintainer, will automatically deploy a preview site. A comment with a link to the preview will show up in the PR.

## Deployment

See the [`docs-actions` README](https://github.com/nginxinc/docs-actions/tree/main?tab=readme-ov-file#docs-actions).

## Contributing

Pull requests are welcome. For major changes, please open an issue
first to discuss what you would like to change.

## License

The documentation for NGINX Unit is licensed under [CC BY 4.0](LICENSE).
