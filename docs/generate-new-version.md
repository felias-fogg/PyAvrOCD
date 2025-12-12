# How to Generate a New Version

1. Inside `PyAvrOCD`:
   1. Bump version number in `pyproject.toml`
   2. git commit -a -m "\<version number\>"
   3. git push
   4. Goto web page and make new release (use correct version number for tag and version!). This will trigger a workflow that will do the following:
      - check for correct version number
      - run unit-tests
      - build the binaries
      - upload assets to new release
      - deploy the new binaries to the download site
      - install everything on PyPI
5. Change into xCore
   1. Change version number for `AVROCDTOOLS_VERSION` in Add_avrocd-tools-release.sh
   2. Change `AVROCDTOOLSVERSION` number in `Boads_manager_release.sh`
   3. create PR
