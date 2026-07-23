# How to produce a new release

- Commit and push any changes.

- Go into the root folder and call

     ```
     ./extras/prepare_release.sh <release-id>
     ```

- This will check whether we are really ready to make a new release by checking the release-id and checking whether there are uncommitted/unpushed changes.

- Then it will connect to Trixie (a Raspi 3) and produce the arm-linux-gnueabihf version of PyAvrOCD, which will be copied to the corresponding binary folder.

- After it, these changes are uploaded to GitHub.

- Then you need to create a release on the Web UI.