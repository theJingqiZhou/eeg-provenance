# Forward-test cases

`cases.json` defines black-box expectations for saved Agent responses. It does not invoke an Agent or replace scientific review; it makes generated responses reproducibly scorable.

Save responses as a JSON object keyed by case ID, then run:

```bash
python tools/score_eval_responses.py responses.json
```

Use `--case CASE_ID` repeatedly for a bounded run. The command exits `0` only when every selected response contains all `must_include` terms and none of its `must_not_include` terms. Missing responses fail a full run; malformed inputs or unknown case IDs exit `2`.
