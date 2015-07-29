### Beaker notebook

See [the main website](http://beakernotebook.com/)

To run the beaker notebooks in this directory:
* Copy the contents of the static dir- `static/*`- to the `src/main/web` folder (in the beaker directory); on Mac OS, to `/Applications/Beaker.app/Contents/Resources/dist/src/main/web` ([see FAQ](http://beakernotebook.com/faq))

Some notes on getting beaker to run:
* To run from linux server e.g. raiders2: `./beaker.command --public-server`
* **Currently only works on Firefox ([see issue](https://github.com/twosigma/beaker-notebook/issues/1963))**
* Sometimes data files do not appear to reload properly; to remedy this, save & close the notebook, refresh the page in the browser, re-open the notebook and load data again...
* Note that language options have to be re-set for each notebook (TODO: look up if way to set this up better).  E.g. add to IPython:

        %load_ext autoreload
        %autoreload 2

* Specifying language binaries locations: edit `~/.beaker/v1/config/beaker.pref.json` while beaker not running ([see docs](https://github.com/twosigma/beaker-notebook/wiki/Language-Preferences))
