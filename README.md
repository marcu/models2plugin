# Models to plugin - QGIS Plugin

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)




## Generated options

### Plugin

> Here is a list of the options you picked when creating the plugin with the cookiecutter template.

| Cookiecutter option | Picked value |
| :------------------ | :----------: |
| Plugin name | Models to plugin |
| Plugin name slugified | models2plugin |
| Plugin name class (used in code) | Models2Plugin |
| Plugin category | None |
| Plugin description short | This plugin helps you for generating a plugin embedding your models |
| Plugin description long | This plugin helps you for generating a plugin embedding your models |
| Plugin tags | plugin,model |
| Plugin icon | default_icon.png |
| Plugin with processing provider | False |
| Author name | Marc Ducobu |
| Author organization | WAPY |
| Author email | marc.ducobu@posteo.be |
| Minimum QGIS version | 3.40 |
| Maximum QGIS version | 3.99 |
| Support Qt6 | True |
| Git repository URL | https://gitlab.com/WAPY/models2plugin/ |
| Git default branch | main |
| License | MIT |
| Python linter | None |
| CI/CD platform | GitHub |
| Publish to <https://plugins.qgis.org> using CI/CD | True |
| IDE | VSCode |

### Tooling

This project is configured with the following tools:

- [Black](https://black.readthedocs.io/en/stable/) to format the code without any existential question
- [iSort](https://pycqa.github.io/isort/) to sort the Python imports

Code rules are enforced with [pre-commit](https://pre-commit.com/) hooks.

See also: [contribution guidelines](CONTRIBUTING.md).

## CI/CD

Plugin is linted, tested, packaged and published with GitHub.

If you mean to deploy it to the [official QGIS plugins repository](https://plugins.qgis.org/), remember to set your OSGeo credentials (`OSGEO_USER_NAME` and `OSGEO_USER_PASSWORD`) as environment variables in your CI/CD tool.


### Documentation

The documentation is located in `docs` subfolder, written in Markdown using [myst-parser](https://myst-parser.readthedocs.io/), structured in two main parts, Usage and Contribution, generated using Sphinx (have a look to [the configuration file](./docs/conf.py)) and is automatically generated through the CI and published on Pages: <https://gitlab.com/WAPY/models2plugin/> (see [post generation steps](#2-build-the-documentation-locally) below).

----

## Next steps post generation

### 1. Set up development environment

> Typical commands on Linux (Ubuntu).

1. If you didn't pick the `git init` option, initialize your local repository:

    ```sh
    git init
    ```

1. Follow the [embedded documentation to set up your development environment](./docs/development/environment.md) to create  virtual environment and install development dependencies.
1. Add all files to git index to prepare initial commit:

    ```sh
    git add -A
    ```

1. Run the git hooks to ensure that everything runs OK and to start developing on quality standards:

    ```sh
    # run all pre-commit hooks on all files
    pre-commit run -a
    # don't be shy, run it again until it's all grren
    ```

### 2. Adjust URL and build the documentation locally

> [!NOTE]
> Since it's very hard to determine which the final documentation URL will be, the templater does not set it up. You have to do it manually.
> The final URL should be something like this: <https://{user_org}.github.io/{project_slug}>. You can find it in Pages settings of your repository: <https://gitlab.com/WAPY/models2plugin//settings/pages>.

1. Have a look to the [plugin's metadata.txt file](models2plugin/metadata.txt): review it, complete it or fix it if needed (URLs, etc.)., especially the `homepage` URL which should be to your GitLab or GitHub Pages.
1. Update the base URL of custom repository in [installation doc page](./docs/usage/installation.md).
1. Change the plugin's icon stored in `models2plugin/resources/images`
1. Follow the [embedded documentation to build plugin documentation locally](./docs/development/documentation.md)

### 3. Prepare your remote repository

1. If you did not yet, create a remote repository on your Git hosting platform (GitHub, GitLab, etc.)
1. Create labels listed in [labeler.yml file](.github/labeler.yml) to make PR auto-labelling work.
1. Switch the source of GitHub Pages to `GitHub Actions` in your repository settings <https://gitlab.com/WAPY/models2plugin//settings/pages>
1. Add the remote repository to your local repository:

    ```sh
    git remote add origin https://gitlab.com/WAPY/models2plugin/
    ```

1. Commit changes:

    ```sh
    git commit -m "init(plugin): adding first files of Models to plugin" -m "generated with QGIS Plugin Templater (https://oslandia.gitlab.io/qgis/template-qgis-plugin)"
    ```

1. Push the initial commit to the remote repository:

    ```sh
    git push -u origin main
    ```

1. Create a new release following the [packaging/release guide](./docs//development/packaging.md) with the tag `0.1.0-beta1` to trigger the CI/CD pipeline and publish the plugin on the [official QGIS plugins repository](https://plugins.qgis.org/) (if you picked up the option).

----

## License

Distributed under the terms of the [`MIT` license](LICENSE).
