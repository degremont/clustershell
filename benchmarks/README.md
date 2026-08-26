# ClusterShell performance demonstrator

This directory contains a small [airspeed velocity](https://asv.readthedocs.io/)
suite for tracking the performance of the stable `RangeSet` and `NodeSet`
APIs across ClusterShell releases and commits.

The first iteration is deliberately limited to deterministic, in-process
operations. It does not benchmark node group resolution, workers, network I/O,
or command execution.

## Local preview

Create a dedicated environment and install ASV:

```console
python3 -m venv /tmp/clustershell-asv
/tmp/clustershell-asv/bin/pip install -r benchmarks/requirements.txt
```

Check benchmark discovery and run the current checkout quickly:

```console
/tmp/clustershell-asv/bin/asv check
/tmp/clustershell-asv/bin/asv machine --yes
/tmp/clustershell-asv/bin/asv run --quick --no-pull 'HEAD^!'
```

Generate and serve the static dashboard:

```console
/tmp/clustershell-asv/bin/asv publish --no-pull
python3 benchmarks/build_dashboard.py
python3 -m http.server --directory .asv/custom-dashboard
```

The custom ClusterShell interface is generated in `.asv/custom-dashboard`.
The standard ASV interface remains available in `.asv/html` and is published
online below `performance/asv/` as a fallback and detailed expert view.

## Online demonstrator

Pushing the `codex/issue-708-asv-demo` branch runs
`.github/workflows/benchmarks.yml`. The workflow:

1. benchmarks releases `v1.8`, `v1.9`, `v1.10`, `v1.10.1`, and `master`;
2. restores and updates the raw ASV data stored in
   `gh-pages/performance-results/`;
3. transforms the ASV files into the data model used by the ClusterShell
   interface;
4. publishes the custom dashboard to `gh-pages/performance/` and the standard
   ASV view to `gh-pages/performance/asv/`, without modifying the existing site
   at the root of the branch.

Once the workflow completes, the expected URL is:

<https://clustershell.github.io/clustershell/performance/>

GitHub-hosted runners are suitable for demonstrating the workflow and spotting
large changes, but their timing noise makes them unsuitable for enforcing small
performance thresholds. A stable self-hosted runner should be used before the
dashboard is treated as an authoritative regression monitor.
