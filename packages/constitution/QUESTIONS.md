# jp.constitution — open questions and technical gaps

Each entry: what is missing, a minimal reproduction, the workaround in the package, the qualification. None of these is
a declarative provision; each is unfinished work unless stated otherwise. The full audit is
`docs/foundations/jp-constitution/AUDIT.md`; the rows are in `COVERAGE.md` (classification TECH_GAP).

1. **Terms that exclude the recess of the Diet (Art. 59(4), 60(2), 67(2)).** `.law` cannot subtract periods from a term
   (the oracle has `suspensions` for `business_day`/`calendar_day`, unreachable from `.law`/`.lawtest`; months and years
   reject it). Workaround: representation B (recess days are case facts; counted days = calendar days − recess days;
   lapse when the count exceeds the limit); representation A (a pinned calendar whose recess days are non-working) was
   verified but needs a calendar resource and a lock row per session. Qualification: no capability, both evaluators alike.
2. **`legal_time` is not readable by a rule.** `context::legal_time` in a rule body passes `check` and fails at evaluation
   (`TYPE_ERROR … not an A3 parameter value`). Workaround: the fact `assessment_date(x)` that the case must equal to the
   `legal_time` axis (Art. 54(3), 59(4), 60(2), 67(2)). The three scenarios of AUDIT (`12-legal-time-in-body`) reproduce it.
3. **A `valid_when` cannot read the effect of another `power`** (Art. 35 relies on the condition of the arrest power, not on
   its effect). Reproduction in `coverage/J4.json` (T-J4-1). A defeasible `unless` over a power effect is silently not
   applied (LDC-E4103 stops only strict rules); Chapter IV derives `house_dissolved` from the validity facts instead.
4. **Art. 79(2), «and thereafter every ten years».** A recursive rule is refused (LDC-E4102). The model is a ladder of five
   reviews (more than 40 years); a justice retires at the statutory age (Art. 79(5)).
5. **Cabinet competence under Art. 71.** `house_dissolved` and `pm_appointed_on` read the plain fact of advice and approval:
   the competence check would create a cycle through `not_known` that cannot be stratified. The model also cannot tell the
   act of a new Cabinet from that of the resigned one (`resigned_by` works by date only).
6. **Judgment answers.** Both evaluators accept a `case_input` fact of a judgment relation as the answer of the authority
   (SPEC §47.3/§73 names `origin adjudicated`). The package always uses `origin adjudicated`; the lint does not catch a mistake.
   A `positions()` query with an unanswered judgment returns ACTIVE for the prohibition of Art. 76(2) (no violation is derived
   from silence), not REQUIRES_JUDGMENT; an unanswered judgment behind a power effect gives NEITHER (ART73-18).
7. **Proof graphs of NEITHER queries.** With several `count distinct` aggregates in one rule one evaluator may keep
   unreferenced `assertion` nodes and the other not (bytes differ). Qualification: SPEC gap (errata to §180.1) plus a latent
   defect of both implementations (order of the search); `audit/13-proof-graph-orphan-assertions/QUALIFICATION.md`. Not fixed
   (a full circle); the package avoids the trigger.
8. **Position statuses EXERCISED / VALIDLY_EXERCISED / INVALIDLY_EXERCISED / AVAILABLE** are never emitted by either evaluator;
   a `power` is observed through its effect and the issue `POWER_INVALID_EXERCISE`.
9. **Partial nullity (Art. 98(1)).** The text does not say which part of a partly void act stands; a law without force in any
   extent is not a basis for the tax (Art. 84). Two competing readings could be added if a primary source appears.
10. **Choices without a source** that a reviewer may want to revisit: the window of Art. 86 (the financial year) and of Art. 90;
    the denominator of Art. 95 (votes cast); the authority of the judgment in Art. 73(3) («afterwards, depending on circumstances»,
    the Diet) and in Art. 96(2) («immediately», the Supreme Court); the three municipal capacities of Art. 94 as `liberty`, not `power`;
    the rule `DeemedRejectionIsDissent` (Art. 59(4)) reads facts, not the power effect, and so its window from 1947-05-03 does not apply.
11. **Unconfirmed against primary sources** (marked unverified in the comments): the Naganuma decisions (1973, 1976, 1982); the
    entry into force on 29 March 2016 of the 2015 legislation; the purpose-and-effect test of Art. 20(3) (Tsu, 1977; Ehime, 1997); the
    Tomabechi decision on Art. 7 dissolution (1960).
