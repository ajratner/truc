### Beaker notebook

See [the main website](http://beakernotebook.com/)

To run the beaker notebooks in this directory:
* Copy the contents of the static dir- `static/*`- to the `src/main/web` folder (in the beaker directory); on Mac OS, to `/Applications/Beaker.app/Contents/Resources/dist/src/main/web` ([see FAQ](http://beakernotebook.com/faq))

Some notes on getting beaker to run:
* To run from linux server e.g. raiders2: `./beaker.command --public-server`
* **Currently only works on Firefox ([see issue](https://github.com/twosigma/beaker-notebook/issues/1963))**
* Specifying language binaries locations: edit `~/.beaker/v1/config/beaker.pref.json` while beaker not running ([see docs](https://github.com/twosigma/beaker-notebook/wiki/Language-Preferences))
