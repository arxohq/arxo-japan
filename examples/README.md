# Reader examples

Each named directory contains `request.json`, `case.json`, `query.json` and `result.json`.
The [index](index.json) records the originating package scenario and its authored expectations.

Run from the repository root with the pinned `law` on `PATH`:

```sh
law eval examples/amendment-eight-of-twelve
```

To explore a different hypothetical, copy a case and query into your own directory. Keep the case's context (`legalTime`, `decisionTime`, `knowledgeTime`, timezone, deadline policy and reading where supplied). Build a `law.core.evaluation-request/0.2` request using the exact bundled world, then evaluate it with the pinned CLI. Never add an adjudicated fact solely to obtain a preferred answer. A negative assertion retains its negative polarity and its evidence origin.

The bundled examples are synthetic scenarios. They do not assert historical facts about an actual parliamentary vote, armed force, court judgment or Gazette issue.

The two Article 96 House cases ask one House-level prerequisite, not the entire amendment procedure. The referendum case asks a different prerequisite. Article 9 examples make the reading and court-assessment boundary explicit. Kanpo examples distinguish an official publication measure from an ordinary database copy.

`result.json` contains the full proof graph and canonical hashes. Truth status, evaluation status and deontic position status are separate fields. The verification command compares the complete canonical document and repeats the same input; a matching authored truth-status expectation alone is not a claim of full legal correctness.
