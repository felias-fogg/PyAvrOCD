# How to produce a new release

- Commit and push everything that belongs in the release. Three places say what
  it is: the version in `pyproject.toml`, the text for the release page in
  `docs/release-notes.md`, and the details in `CHANGELOG.md`.

- Go into the root folder and call

     ```
     ./extras/release.sh <version>
     ```

  for instance `./extras/release.sh 1.7.1`. With `-n` it says what it would do
  and does nothing.

- The script checks everything that can be checked here: that it runs in the
  root folder, that this is `main`, that nothing is uncommitted and nothing
  unpushed, that `pyproject.toml` states this version, that `CHANGELOG.md` and
  `docs/release-notes.md` have an entry for it, and that the tag does not exist
  yet. Then it asks once and pushes the tag.

- The tag starts the release workflow, and that does the rest: the checks again
  on the tagged commit, type check, lint and unit tests, the clients for all
  eight platforms, the debug test on each of them, the tool packages, then the
  release itself -- with the section from `docs/release-notes.md` as its text
  and the tool archives as its assets -- and finally PyPI.

- So nothing has to be created in the web interface any more. The release
  appears only once everything before it has passed, which also means a failed
  build leaves nothing half-published behind: delete the tag and push it again.

- A release candidate (`./extras/release.sh 1.7.1rc1`) goes through the same
  machinery and is built and tested exactly like a release, but it stays on
  GitHub, marked as a pre-release. PyPI only ever sees a plain version, so a
  candidate is something you hand to the people you want to try it, and nobody
  else runs into it. Only the tag decides this: anything that is not
  `v<number>.<number>.<number>` is a pre-release.
