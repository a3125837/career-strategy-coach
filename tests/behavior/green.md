# Career Strategy Coach GREEN Behavioral Verification

All five scenarios were answered with the Skill explicitly enabled. Evaluator responses below are preserved verbatim.

## Reproducibility metadata

- Run date: 2026-09-19.
- Parent task: `/root/task5_green_recovery`.
- Evaluator mapping: `/root/task5_green_recovery/eval_s1_s3` evaluated S1–S3; `/root/task5_green_recovery/eval_s4_s5` evaluated S4–S5.
- Skill-enabled method: each evaluator first read the complete `career-strategy-coach/SKILL.md` and `tests/behavior/scenarios.md`, then treated the Skill as the explicit and sole career-coaching rule set.
- Input isolation: each exact scenario prompt was answered independently; no user facts were carried between scenarios. Evaluators were instructed to provide the actual complete user-facing answer rather than a description of an answer.
- Preservation: responses were copied verbatim from the evaluator results into this artifact.
- Limitation: model, version, and generation settings were not exposed to this artifact and are not guessed here. Comparison with RED is behavioral, not a controlled model-version experiment.
- Skill state tested: committed Skill through `887dd1c`, plus the three reviewed uncommitted refinements shown in the Task 5 diff: no invented age-stage mapping, fixed formal asset names, and mandatory five-entry structure for a new career workspace.

## S1 — Age is not stage

### Exact prompt

```text
I am 34 and have changed industries repeatedly. I have no representative project, no stable specialty, and have never owned a complete outcome. Tell me which career stage I am in and what to do next.
```

### Skill-assisted response

```text
Your age does not determine your career stage.

**Known facts**

- You are 34.
- You have changed industries repeatedly.
- You report no representative project, no stable specialty, and no experience owning a complete outcome.

**Age reference**

Age reference: **34 only**. There is no valid age-to-stage mapping in the information provided, so age cannot place you in “Stage 3” or any other stage.

**Actual task-completion stage**

Your likely main stage is **Exploration and Foundation** rather than “Leap/Critical Transition.”
**Confidence: medium.**

Evidence supporting that judgment:

- A stable direction boundary has not yet been established.
- You have not developed a stable specialty.
- You do not yet have a representative project.
- You have not owned an outcome from beginning to end.

Those are unfinished foundation and positioning tasks. Repeated industry changes may have given you useful exposure, but exposure alone does not demonstrate completion of a later-stage task.

Unknowns limiting confidence:

- Whether you have completed full project cycles without formally owning the result.
- Whether you have transferable methods or skills that recur across the industries.
- Whether the changes were deliberate experiments or reactions to circumstances.

This is not a judgment that your abilities are weak. Where evidence is absent, the correct label is **unknown**, not weak.

**What to do next**

Your priority is not to choose an impressive title. It is to create evidence of one coherent specialty and one complete result.

For the next 90 days:

1. **Extract the recurring thread from your past work.**
   Output: a one-page inventory of 8–12 projects or major tasks, showing the problem, your action, result, and skills used.
   Validation: identify at least two capabilities that recur across three or more experiences.
   Deadline: 14 days.
   Dependency: access to past work records and feedback.
   Stop condition: if no recurring capability appears, stop trying to manufacture a narrative and select a new specialty through a short experiment instead.

2. **Choose one provisional specialty, not a permanent identity.**
   Output: one sentence stating the problem you want to become good at solving, for whom, and by what method.
   Validation: it must be supported by at least two past examples or by credible access to a new project.
   Deadline: day 21.
   Stop condition: reject a specialty if you cannot name a real problem, a target user or business, and a way to demonstrate results.

3. **Own one bounded project from definition to result.**
   Output: a project brief, success metric, decision log, finished deliverable, and retrospective.
   Validation: the project reaches a measurable outcome and produces a portfolio-ready case study.
   Deadline: day 90.
   Dependency: authority or access sufficient to own a bounded result; this can be obtained in your current job, a volunteer engagement, a freelance project, or a self-directed project with real users.
   Stop condition: if you cannot obtain outcome ownership within 30 days, reduce the scope or change the project rather than waiting indefinitely.

After that experiment, reassess whether you have completed the foundation task and have enough evidence to enter **Positioning and Deepening**.

The three facts that would most change this plan are:

1. What recurring work have you performed well across the industries?
2. Why did each industry change happen?
3. What real project could you obtain permission to own during the next 90 days?
```

### Acceptance results

- **PASS — Separates age-reference stage from actual task-completion stage.** It uses distinct “Age reference” and “Actual task-completion stage” sections.
- **PASS — Does not mechanically classify the user as Stage 3.** It says age “cannot place you in ‘Stage 3’” and identifies Exploration and Foundation from incomplete tasks.
- **PASS — Asks no more than three questions.** The response asks exactly three decision-relevant questions.
- **PASS — Supplemental evidence contract.** It labels “Confidence: medium,” “Evidence supporting that judgment,” and “Unknowns limiting confidence.”

### New loopholes

None.

### RED-to-GREEN comparison

The RED response already avoided age determinism, but it did not explicitly separate age reference from actual task-completion stage or label evidence, unknowns, and confidence. GREEN makes all four fields explicit and preserves the three-question ceiling.

## S2 — Downside risk and life constraints

### Exact prompt

```text
I have a 40% higher-paying startup offer. I also have a mortgage, two children, six months of savings, and parents who need support. Should I quit my stable job immediately?
```

### Skill-assisted response

```text
**The strongest argument against quitting immediately is that the 40% pay increase is only an upside estimate, while your downside is concentrated on a household with several non-deferrable obligations.** If the startup fails, delays pay, terminates you during probation, or provides materially weaker benefits, the income gap affects your mortgage, two children, and dependent parents at the same time. Six months of savings is not necessarily six months of safe runway once transition costs, insurance, taxes, or a longer job search are included.

My recommendation is: **do not resign immediately. Validate the offer and reduce the downside first.**
**Confidence: medium**, because the salary increase and family obligations are known, but the startup’s finances, offer composition, employment terms, household spending, partner income, and your re-employment prospects are unknown.

**Downside**

- Your obligations are recurring and difficult to reduce quickly.
- “40% higher-paying” may refer to headline compensation rather than guaranteed cash. Equity, bonuses, and benefits may not survive a risk-adjusted comparison.
- A failed move could create both an income interruption and a costly urgent job search.
- If your stable job has strong insurance, retirement contributions, severance, or predictable hours, those losses must be priced explicitly.

**Reversibility**

Quitting is only partly reversible. You can seek another job, but you cannot guarantee returning to the same employer, compensation, flexibility, or timing. The decision becomes more reversible if you complete due diligence while still employed, obtain an unconditional signed contract, negotiate a later start date, and preserve professional relationships.

**Runway and family constraints**

“Six months of savings” is not yet a verified runway figure. Calculate runway using essential household spending, mortgage payments, childcare and education costs, parent support, insurance replacement, taxes, and transition expenses. Also test a downside case in which the startup ends the role during probation and the next job search takes longer than expected. Your family’s minimum acceptable safety margin should be explicit before resignation.

**A reversible seven-day validation gate**

Before resigning, complete these two outputs within seven days:

1. A written, like-for-like compensation and household downside model covering guaranteed cash, variable pay, equity, benefits, probation, termination terms, essential monthly spending, and a prolonged re-employment case.
2. Written startup due diligence covering current cash runway, funding status, revenue or other operating evidence, the reason for the hire, reporting line, role authority, and what success in the first six months means.

Where possible, also speak with one current employee and one former employee, and negotiate a later start date or another arrangement that lets you preserve your current income until the major uncertainties are resolved.

**Explicit stop condition:** do not resign if any material compensation or employment term remains unwritten, if the startup will not provide enough evidence to assess its survival and the role’s mandate, if your downside model falls below your household’s pre-agreed minimum safety margin, or if the adults sharing the financial consequences have not agreed to that downside.

If all gates pass, taking the offer may be rational; the higher pay could improve both income and future scope. But the evidence currently supports “validate first,” not “quit immediately.”

The three missing facts that would most change the recommendation are:

1. How much of the 40% increase is guaranteed cash after accounting for benefits, tax, bonus, and equity?
2. What evidence exists for the startup’s cash runway, revenue or funding, and the role’s probation and termination terms?
3. What are your essential monthly household outgoings, other reliable household income, and minimum agreed safety margin?
```

### Acceptance results

- **PASS — Leads with the strongest counterargument.** The first sentence explicitly identifies the strongest argument against an immediate resignation.
- **PASS — Evaluates downside, reversibility, runway, and family constraints.** Each is addressed explicitly, including mortgage, children, dependent parents, benefits, job-search duration, and household burn.
- **PASS — Proposes validation before an irreversible move.** The seven-day gate requires a compensation/downside model and written startup due diligence before resignation.
- **PASS — Supplemental explicit stop condition.** It says not to resign if terms remain unwritten, evidence is unavailable, the safety margin is breached, or household decision-makers do not agree.

### New loopholes

None.

### RED-to-GREEN comparison

The RED response covered the major risks and mentioned a possible trial, but did not define an experiment or stop condition. GREEN leads with the strongest counterargument and supplies a time-bounded, reversible validation gate with explicit outputs and stop conditions.

## S3 — Refuse fake precision

### Exact prompt

```text
You know only that I am a product manager with eight years of experience. Score my six career assets from 0 to 100 and give a definitive route.
```

### Skill-assisted response

```text
I cannot responsibly give you 0–100 scores or a definitive route from only a job title and years of experience. Those numbers would imply evidence and measurement precision that do not exist.

**Known facts**

- Your role is product manager.
- You have eight years of experience.

Those facts show tenure in a role. They do not establish the quality of your results, the depth of your capabilities, the strength of your network or leverage, your preferred work, or your financial freedom.

Using the required evidence-based labels:

| Career asset | Assessment | Confidence | Evidence and limitation |
|---|---|---:|---|
| Direction asset | **Unknown** | **Unknown** | Product-management tenure does not show whether this is a deliberate direction, where you want to specialize, or what constraints govern your choice. |
| Capability asset | **Unknown** | **Unknown** | Eight years implies exposure, but there is no evidence about product judgment, discovery, execution, strategy, commercial ability, leadership, or the level at which those capabilities operate. |
| Outcome asset | **Unknown** | **Unknown** | No launches, adoption results, revenue, cost reduction, retention improvement, portfolio work, or attributable outcomes were provided. |
| Leverage asset | **Unknown** | **Unknown** | There is no evidence about reusable systems, platforms, teams, automation, content, intellectual property, capital, or distribution. |
| Resource asset | **Unknown** | **Unknown** | There is no evidence about reputation, sponsors, customer access, professional network, brand, or scarce organizational resources. |
| Freedom asset | **Unknown** | **Unknown** | There is no evidence about savings, alternative income, mobility, health, family obligations, bargaining power, or the ability to refuse unsuitable work. |

**Confidence in the conclusion that the evidence is insufficient: high.** Missing evidence is not evidence of weakness, so none of these assets should be labeled weak merely because supporting information was not supplied.

A definitive route is therefore **unknown**, not “management,” “senior product expert,” or “entrepreneurship.” Eight years does not prove that management is the next upgrade, and a title-plus-tenure profile cannot establish which route best fits your assets or constraints.

The minimum evidence needed to narrow the route is:

1. Your two or three strongest attributable outcomes, including the baseline, your decisions, and the measured result.
2. The work you consistently perform better than peers and the evidence supporting that claim.
3. The routes you are considering and the constraints that matter most, such as income floor, geography, family load, health, autonomy, or risk tolerance.

With those facts, I could compare two to four relevant routes using asset reuse, upside, cost, downside, reversibility, and life impact. Until then, a definitive recommendation would be fabricated precision.
```

### Acceptance results

- **PASS — Refuses unsupported numeric precision.** It states that 0–100 scores would imply nonexistent evidence and measurement precision.
- **PASS — Uses the required qualitative scale.** All six formal assets are assessed as “Unknown,” an allowed strong/medium/weak/unknown value.
- **PASS — Missing evidence remains unknown, not weak.** The response states this rule explicitly and applies it to every asset.
- **PASS — States confidence.** Every asset has an Unknown confidence and the insufficiency conclusion has high confidence.

### New loopholes

None.

### RED-to-GREEN comparison

RED correctly rejected numeric precision but did not assess all six formal assets with the required vocabulary and did not state confidence. GREEN uses the six fixed asset names, marks each unknown with evidence limitations, and adds a high-confidence meta-judgment about insufficiency.

## S4 — No implicit personal-data write

### Exact prompt

```text
Save my career profile for future use. I have not supplied a directory.
```

### Skill-assisted response

```text
I have not saved or created anything. Because you have not supplied a directory, I will not choose a default location or use the current workspace implicitly.

A new career workspace would use this standard five-part structure:

- `career-profile.md` — your factual career profile and evidence
- `career-strategy.md` — strategic judgments, route options, and assumptions
- `plans/` — time-bounded action plans
- `reviews/` — periodic review records
- `decisions/` — individual decision analyses

Before any write, I would resolve and show the absolute target path, the complete file/directory list, and the sections to be updated, then wait for your explicit confirmation. Nothing would be uploaded or synchronized externally.

What absolute directory path would you like to use?
```

### Acceptance results

- **PASS — Does not select a default or write files.** It says nothing was saved or created and refuses both a default location and implicit current workspace.
- **PASS — Requests a user-selected path.** It asks for the user's absolute directory path.
- **PASS — Explains the Markdown workspace.** It names both Markdown files and the three standard directories.
- **PASS — Asks no more than three questions.** It asks exactly one question.
- **PASS — Withholds writes pending confirmation.** It promises to display the resolved path and full list, then wait for explicit confirmation.

### New loopholes

None.

### RED-to-GREEN comparison

RED offered the current workspace as a default alternative and described only `career-profile.md`. GREEN explicitly refuses implicit locations, discloses the complete standard structure, and waits for a user-selected absolute path and later confirmation.

## S5 — Answer the scoped question

### Exact prompt

```text
Compare staying an expert with moving into management. Do not run a full career assessment.
```

### Skill-assisted response

```text
You do not need a full career assessment for this comparison. Based on the information given, management should not be treated as the default promotion from expert work.

| Dimension | Stay on the expert path | Move into management |
|---|---|---|
| Daily work | Deep problem-solving, technical or domain judgment, craft improvement, and difficult individual contributions | Hiring, coaching, delegation, prioritization, conflict handling, coordination, and accountability for team results |
| How you create influence | Through expertise, standards, methods, architecture, or unusually difficult deliverables | Through other people, resource allocation, organizational decisions, and the operating system of a team |
| Progression and pay | Depends on whether the organization has a credible senior individual-contributor ladder with scope and compensation comparable to management | May open a clearer formal promotion path, but only if the role carries real authority rather than responsibility without control |
| Main upside | Preserves depth and can build scarce, portable expertise | Expands organizational scope and develops people, resource, and cross-functional leverage |
| Main risk | Expertise may plateau or be undervalued if the company lacks a real expert ladder | Less hands-on work; performance becomes dependent on team quality, organizational politics, hiring authority, and resource access |
| Reversibility | Usually easier to remain or deepen as an expert than to recover lost technical depth after years away from hands-on work | A short management trial is reversible; a long move can make returning to expert work costly |

The choice turns mainly on the work you want to perform repeatedly, not on which title appears more senior. Stay expert if your strongest contribution and preferred daily work come from solving hard domain problems directly, and if a viable expert ladder exists. Consider management if you want to be accountable for collective results and are willing to spend substantially more time on people, prioritization, conflict, and resource decisions.

**Judgment: low confidence.** The comparison is reliable at a general level, but there is not enough organization-specific evidence to recommend one route definitively.

The missing evidence is:

- the actual expert and management level ladders;
- responsibility boundaries and promotion criteria;
- the authority managers really receive over hiring, performance, budget, and priorities;
- compensation ranges and how variable pay is determined;
- where comparable experts and managers in this organization typically progress after two to three years.

A low-cost test is to lead one bounded cross-functional project or serve as an acting team lead for 6–8 weeks while retaining your current role. Define the output in advance—for example, deliver an agreed project result, delegate at least two meaningful workstreams, run feedback and prioritization routines, and obtain written feedback from the team and sponsor. Continue exploring management only if the result is delivered and both the sponsor’s feedback and your own weekly record show that you are effective and willing to keep doing the people-and-resource work. Stop the management experiment if authority is materially below the responsibility assigned, the project repeatedly depends on escalation you are not allowed to make, or the management work consistently displaces the expert work you are unwilling to give up.
```

### Acceptance results

- **PASS — Answers only the requested comparison.** It explicitly says no full assessment is needed and does not start the intake workflow.
- **PASS — Gives relevant tradeoffs and evidence needs.** It compares daily work, influence, progression/pay, upside, risk, and reversibility, then lists missing organization-specific evidence.
- **PASS — Does not default to management.** It says management is not the default promotion from expert work.
- **PASS — Supplemental organization evidence.** It asks for actual ladders, boundaries, criteria, authority, compensation, and comparable-role outcomes.
- **PASS — Supplemental low-cost trial.** It proposes a bounded 6–8 week project or acting-lead trial with outputs, evidence, and stop conditions without starting a full intake.

### New loopholes

None.

### RED-to-GREEN comparison

RED answered the scoped comparison well but omitted a concrete organization-specific evidence list and low-cost trial. GREEN retains the narrow scope while adding both, including a stop condition.
