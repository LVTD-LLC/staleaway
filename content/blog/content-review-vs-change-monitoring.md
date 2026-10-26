Content review asks whether a page is still accurate and useful; website change monitoring checks for changes or configured conditions on watched pages. Choose review reminders when you need a human to revisit your own content. Choose monitoring when you need change alerts. Use both when changes and quiet, outdated pages matter.

A contact page can stay exactly the same while your opening hours change. A redesigned page can look different while every fact remains correct. Neither a quiet monitor nor an opened reminder establishes that the content is right.

This guide helps you choose the workflow, not a winning vendor. The decision framework below is Staleaway’s practical recommendation, followed by fictional examples and a record you can copy into your own document. It is not a benchmark or a report of customer results.

<nav aria-label="On this page">
<p><strong>On this page</strong></p>
<ul>
<li><a href="#compare-the-job">Content review vs change monitoring: compare the job</a></li>
<li><a href="#monitoring-wins">Where website change monitoring wins</a></li>
<li><a href="#human-review-wins">Where human content review wins</a></li>
<li><a href="#two-questions">Use two questions before deciding what to do</a></li>
<li><a href="#combine-workflows">Combine alerts and reminders without duplicating work</a></li>
<li><a href="#review-date-vs-expiry">Review dates, expiry and your CMS workflow</a></li>
<li><a href="#staleaway-fit">When Staleaway is the right fit</a></li>
<li><a href="#common-decisions">Common decisions</a></li>
</ul>
</nav>

<h2 id="compare-the-job">Content review vs change monitoring: compare the job</h2>

| Decision | Human content review | Website change monitoring |
|---|---|---|
| Main question | Does this page still help its reader and match current facts? | Did the watched source change, or does a configured check need attention? |
| Starting signal | A scheduled review, known business change, question or complaint | A detected change or a configured condition |
| Evidence to inspect | The page, current source material and the responsible owner’s knowledge | The alert, affected page or region, relevant history and rule configuration |
| Next step | Keep accurate content, fix a problem or ask its owner to resolve uncertainty | Investigate the signal, confirm intent and decide whether action is needed |
| What silence means | No reminder is not evidence that everything is current | No alert is not evidence that every business fact is current |

These are different questions, not competing definitions of quality. [GOV.UK’s content-maintenance guidance](https://guidance.publishing.service.gov.uk/writing-to-gov-uk-standards/plan-manage-content/manage-existing-govuk-content/) recommends regular checks of existing content’s usefulness and changes to correct factual errors or update information. That is editorial work, even when software helps decide where to look.

<h2 id="monitoring-wins">Where website change monitoring wins</h2>

Start with monitoring if the job is to notice a change to a particular source without waiting for your next reading session. Examples include an unexpected edit to your own page, a changed upstream document, or a technical condition you have explicitly configured a tool to check.

Modern monitors are not limited to comparing raw HTML. [Distill’s documentation](https://distill.io/docs/web-monitor/using-conditions-to-get-alert-on-important-changes/) describes conditions using text, added or removed content, numbers and combined rules. [Visualping describes AI summaries and importance criteria](https://visualping.io/blog/visualping-ai) for interpreting changes. Check what a specific tool actually watches and how it decides to alert.

Automated monitoring has three clear advantages over Staleaway’s reminder workflow:

- **Unexpected changes:** use a monitor when you need an alert about a watched edit rather than a prompt to read a few pages.
- **Specific technical faults:** [Little Warden lists checks](https://littlewarden.com/features) for matters such as response codes, redirects, certificates, indexability and content rules. Staleaway does not provide that technical monitoring suite.
- **Change history and alert triage:** [Conductor Monitoring describes a change history and configurable alerting](https://www.conductor.com/platform/monitoring/). Choose a suitable monitoring product when investigating technical changes across a site is the primary job, rather than treating a reminder email as an incident record.

Those are vendor-documented capabilities, not tools we tested for this article. Alert timing, coverage and accuracy depend on the product and configuration. There is no price or performance ranking here.

<h2 id="human-review-wins">Where human content review wins</h2>

A reviewer can ask the person responsible for a service whether its description still matches what the business offers. That question can matter even if the published page has not changed. An internal change to availability, staffing or procedure may never appear in a public source that your monitor watches.

Monitoring authoritative upstream sources can help. If a supplier publishes revised instructions and you monitor that document, the resulting alert can prompt a review of your own guide. The useful distinction is not “software cannot understand content.” It is whether the evidence needed for your decision is included in the checks you have configured.

Human review also needs boundaries. A person can miss an error, overlook a page or leave a task unfinished. A scheduled reminder creates a reason to look; it does not certify correctness. For each important claim, decide who can confirm it and what source they should check. Give known changes and reported errors their own follow-up instead of waiting for the next scheduled session.

When you are ready to inspect a page, use the [website content review checklist](/blog/website-content-review-checklist). It covers the review itself; this comparison is for choosing what should trigger that work.

<h2 id="two-questions">Use two questions before deciding what to do</h2>

Ask whether the watched page changed, then separately check whether its current claim is correct. The second answer needs evidence, not an assumption based on the first.

<figure class="my-8">
<svg viewBox="0 0 400 410" width="100%" role="img" aria-labelledby="content-review-vs-change-monitoring-title content-review-vs-change-monitoring-desc" style="color:var(--sa-night)">
<title id="content-review-vs-change-monitoring-title">Change and accuracy require separate decisions</title>
<desc id="content-review-vs-change-monitoring-desc">Staleaway decision framework. A changed page may be correct or need a fix. An unchanged page may also be correct or need a fix. Check the facts before deciding.</desc>
<text x="200" y="25" text-anchor="middle" font-size="18" font-weight="bold" fill="currentColor">Check change. Then check the facts.</text>
<text x="101" y="64" text-anchor="middle" font-size="18" fill="currentColor">Facts correct</text>
<text x="299" y="64" text-anchor="middle" font-size="18" fill="currentColor">Facts wrong</text>
<rect x="8" y="78" width="186" height="132" rx="16" fill="var(--sa-lavender)"/>
<rect x="206" y="78" width="186" height="132" rx="16" fill="var(--sa-lavender)"/>
<rect x="8" y="224" width="186" height="132" rx="16" fill="var(--sa-lavender)"/>
<rect x="206" y="224" width="186" height="132" rx="16" fill="var(--sa-lavender)"/>
<text x="101" y="110" text-anchor="middle" font-size="18" fill="currentColor">Changed page</text>
<text x="101" y="150" text-anchor="middle" font-size="18" font-weight="bold" fill="currentColor">Confirm intent</text>
<text x="101" y="180" text-anchor="middle" font-size="17" fill="currentColor">No needless rewrite</text>
<text x="299" y="110" text-anchor="middle" font-size="18" fill="currentColor">Changed page</text>
<text x="299" y="150" text-anchor="middle" font-size="18" font-weight="bold" fill="currentColor">Investigate + fix</text>
<text x="299" y="180" text-anchor="middle" font-size="17" fill="currentColor">Verify the correction</text>
<text x="101" y="256" text-anchor="middle" font-size="18" fill="currentColor">Unchanged page</text>
<text x="101" y="296" text-anchor="middle" font-size="18" font-weight="bold" fill="currentColor">Keep useful content</text>
<text x="101" y="326" text-anchor="middle" font-size="17" fill="currentColor">Record the check</text>
<text x="299" y="256" text-anchor="middle" font-size="18" fill="currentColor">Unchanged page</text>
<text x="299" y="296" text-anchor="middle" font-size="18" font-weight="bold" fill="currentColor">Find the changed fact</text>
<text x="299" y="326" text-anchor="middle" font-size="17" fill="currentColor">Correct the quiet page</text>
<text x="200" y="389" text-anchor="middle" font-size="15" fill="currentColor">Staleaway decision framework · October 2026</text>
</svg>
<figcaption>A change is a reason to investigate, not a verdict on accuracy. An unchanged page can still need a correction.</figcaption>
</figure>

**Fictional examples — not customer results or monitoring tests:**

1. **Unchanged page, wrong fact.** A consultancy stops taking Friday calls. Its contact page still promises Friday phone support. Compare the page with the current operating schedule, assign the correction and verify the published result. A monitor watching only that unchanged page has no on-page edit to detect.
2. **Changed page, correct facts.** The consultancy replaces a photograph and rearranges its contact section. Check that the change was intended and that the contact route still works. If the information remains correct, do not rewrite it just to make it look newly reviewed.
3. **Changed page, wrong fact.** An editor accidentally publishes old opening hours during a redesign. Investigate the change, confirm the current hours with their owner and check the correction after publication. A known error should not wait for a routine reminder.
4. **Unchanged page, correct facts.** The contact details and hours still match the business. Keep the useful content. Record what you checked so that the next reviewer does not have to guess.

If you cannot establish the facts, leave the decision unresolved and name the person who can. Do not turn missing evidence into a “passed” result.

<h2 id="combine-workflows">Combine alerts and reminders without duplicating work</h2>

Give each signal a job. A monitor on an upstream release-notes page can flag a possible reason to revisit your integration guide. A regular human review can check whether the guide remains useful between those alerts. Neither signal should automatically mean “rewrite the whole page.”

Use one external document or task record for the resulting decision. Copy this record for each page that needs a check:

- **Page and claim:** which statement or reader task are you checking?
- **Trigger:** reminder, detected change, known business change or feedback?
- **Evidence checked:** current source, responsible person and date checked.
- **Decision:** keep, fix or unresolved; explain the reason.
- **Follow-up:** who owns the action, when is it needed, and who will verify it?
- **Return condition:** next planned review or a named change that should bring it forward.

This record is a suggested method for your own document, not a feature that Staleaway fills in. Use the [free workload planner](/tools/content-review-planner) to choose a manual review batch that fits your available time. Its estimate is not a promise of reminder coverage or completion.

<h2 id="review-date-vs-expiry">Review date vs expiry date: choose the action first</h2>

A content review date asks for an editorial check. An expiry date can change what is published, depending on the CMS and its configuration. Before setting either, decide whether you want someone to inspect the content or whether you have already agreed what must happen to it. Read your CMS’s field description; the label alone is not enough.

| What you need | Appropriate next step | What to verify |
|---|---|---|
| Check whether a service description is still accurate | A human review reminder, or your existing CMS review workflow | Who will check the facts and where unfinished work stays visible |
| Stop displaying a time-limited announcement | An agreed expiry, replacement or unpublish action in your publishing system | The intended public result, responsible editor and actual execution time |
| Notice an unexpected edit or a change to a watched source | A configured change monitor | What it watches and which conditions cause an alert |

For a concrete example, [Terminalfour’s content documentation](https://docs.terminalfour.com/documentation/managing-content/create-content/) describes a Review date that emails the last editor or content owner. Its Expiry date affects content on the next publish; whether content stops publishing in place or moves to an archive depends on the Archive Section setting. These are documented behaviors, not a test of your installation. Confirm them with your CMS administrator before relying on a deadline.

Timing deserves its own check. [Drupal Scheduler’s documentation](https://www.drupal.org/docs/contributed-modules/scheduler/configuring-scheduled-publication) explains that scheduled publishing and unpublishing run through cron, so execution follows that schedule. A date entered in a field is not by itself proof that the public change happened at that moment.

**Fictional handoff example — not a completed review:** an event announcement must stop accepting registrations at 17:00 Europe/London on 30 October 2026.

- **Review:** Sam, the fictional web editor, checks the closing message and registration platform’s separate cutoff at 10:00 Europe/London on 29 October.
- **Chosen publishing action:** Jo, the fictional publishing owner, will replace the announcement’s registration invitation with an approved closed-registration notice at 16:45 Europe/London on 30 October. The earlier notice is agreed with the event owner. In this example, the CMS’s next automatic publish is too late, so Jo uses a supervised update instead of relying on expiry.
- **Verification:** Taylor, the fictional checker, will inspect the public notice after Jo’s update and the registration route after the 17:00 cutoff. The task stays pending until those checks are recorded; if either result is wrong, Taylor escalates it to the responsible owner. Changing the announcement does not close the registration platform.

A routine reminder is not the fallback for a missed cutoff.

Use this short handoff in your existing task or CMS record:

> **Public page / time-limited claim:**<br>
> **Review before / responsible person:**<br>
> **Agreed publishing action / owner:**<br>
> **Deadline and timezone / scheduler checked:**<br>
> **Public result checked on / evidence or unresolved follow-up:**

This is a manual planning aid, not a Staleaway feature. Set page-specific deadlines in a system that supports them; Staleaway’s random reminder selection does not guarantee a particular page will arrive before its cutoff, and Staleaway does not unpublish content.

Check your existing CMS workflow before adding another tool. If it already gives your team the review reminders, ownership, approvals and decision record you need, keep that as the source of truth. Staleaway can suit a simpler sitemap-based reminder habit; it should not replace a working editorial approval record. Use the [content review checklist](/blog/website-content-review-checklist#owner-handoff) for the check itself and any unfinished correction.

<h2 id="staleaway-fit">When Staleaway is the right fit</h2>

Staleaway is for a small human-review habit: add a sitemap, choose reminder settings and receive a few pages by email. All features are currently free. If you need help finding your starting list, follow the [sitemap-finding guide](/blog/find-your-website-sitemap).

The current reminder selection picks randomly from eligible unreviewed pages. Choosing daily, weekly or monthly settings does not guarantee that every page will be reviewed, or reviewed again, at that interval. Keep deliberate full-site coverage in your own plan.

The [current review-link implementation](https://github.com/LVTD-LLC/staleaway/blob/437c52d43adbfcbf88ab830de8ea2b0b57d44baf/core/views.py) marks the page reviewed and redirects you to it when you open the link. That action does not establish that you read the page carefully, confirmed its facts or finished a correction. Keep unfinished work in your own record.

Choose another product when your immediate need is automated change detection, uptime or technical fault monitoring. Staleaway does not audit or rewrite your content. If its reminder workflow fits, [create a free account](/accounts/signup/) and start with a manageable review list.

<h2 id="common-decisions">Common decisions</h2>

### Can unchanged website content be out of date?

Yes. A page can remain unchanged while the business facts behind it change. Check its claims against current sources and the responsible owner. Monitoring relevant upstream sources can help, but a quiet monitor alone does not prove the page is current.

### Do I need both content review and change monitoring?

Use both when you need alerts about watched changes and a regular check of your own content’s usefulness and accuracy. Define the evidence and follow-up owner for each signal so that an alert or reminder leads to a decision, not automatic rewriting.

### Does opening a Staleaway reminder prove the review is complete?

No. Opening the review link marks the page reviewed and redirects you to it. It does not prove that the content was checked or a fix was completed. Keep unresolved work and verification in your own record.
