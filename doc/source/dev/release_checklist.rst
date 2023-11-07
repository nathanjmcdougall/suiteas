Release Checklist
====================================

When releasing a new version of SuiteAs, the following steps should be taken:

1. Create a new branch from the `develop` branch named `doc/release-<version>` for the
   purpose of adding documentation for the release of this version, where `<version>` is
   the new version number in SemVer, e.g. `1.3.2`. Change to this new branch.
2. Run `towncrier build --version=<version> --yes`. This will update the changelog from
   the changelog entry files in `doc/changelog_entries`.
3. Ensure that there are no changelog entry files remaining in the
   `doc/changelog_entries` directory.
4. Manually write a summary of the release in the `doc/source/release/notes.rst`
   file.
5. Open a Pull Request for the `doc/release-<version>` branch and merge it into
   `develop` once it has been approved.
6. Create a new branch from `develop` branch named `release/<version>` for the
   purpose of releasing this version. Change to this new branch.
7. Release the package adding a tag named `v<version>`, e.g. `v1.3.2`.
8. Push the release branch and the tag to the remote repository on GitHub. This will
   trigger a deployment on PyPI.
9. Create a pull request to merge the release branch into `main`.
10. Merge the pull request into `main`, deleting the release branch.
11. Create a pull request to merge the `main` branch into `develop`, and merge it.
12. Publish a GitHub release for the tag `v<version>` with the release notes from
    `doc/source/release/notes.rst` and the changelog from `doc/source/changelog.rst`.
