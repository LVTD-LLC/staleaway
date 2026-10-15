// Pure, bounded arithmetic. No network, persistence, URL or browser dependencies.
const FIELDS = [
  { key: "pages", label: "Pages to review", max: 100000, example: "60" },
  { key: "minutesPerPage", label: "Minutes per page", max: 480, example: "8" },
  { key: "sessionMinutes", label: "Minutes per session", max: 480, example: "30" },
  { key: "sessionsPerWeek", label: "Sessions per week", max: 7, example: "2" },
  { key: "targetWeeks", label: "Target weeks", max: 104, example: "8" },
];

function validate(raw) {
  const values = {};
  const errors = {};
  FIELDS.forEach(({ key, label, max }) => {
    const text = typeof raw[key] === "string" ? raw[key].trim() : "";
    if (!/^[0-9]{1,6}$/.test(text) || Number(text) < 1 || Number(text) > max) {
      errors[key] = `${label}: enter a whole number from 1 to ${max.toLocaleString("en-US")} using digits 0–9.`;
    } else {
      values[key] = Number(text);
    }
  });
  return { values, errors };
}

function calculate(raw) {
  const { values, errors } = validate(raw);
  if (Object.keys(errors).length) return { status: "invalid", errors };
  const { pages, minutesPerPage, sessionMinutes, sessionsPerWeek, targetWeeks } = values;
  const batch = Math.min(pages, Math.floor(sessionMinutes / minutesPerPage));
  if (!batch) return { status: "cannot-fit", values };
  const sessionsNeeded = Math.ceil(pages / batch);
  const weeksNeeded = Math.ceil(sessionsNeeded / sessionsPerWeek);
  const targetCapacity = batch * sessionsPerWeek * targetWeeks;
  return {
    status: "ready", values, batch, sessionsNeeded, weeksNeeded, targetCapacity,
    reviewMinutes: pages * minutesPerPage,
    reservedMinutes: sessionsNeeded * sessionMinutes,
    remainingAtTarget: Math.max(0, pages - targetCapacity),
    minimumSessionsPerWeek: Math.ceil(sessionsNeeded / targetWeeks),
  };
}

function report(result) {
  if (result.status !== "ready") return "";
  const v = result.values;
  return [
    "Content review workload estimate — Staleaway",
    `Assumptions: ${v.pages} pages; ${v.minutesPerPage} minutes per page; ${v.sessionMinutes} minutes per session; ${v.sessionsPerWeek} sessions per week; ${v.targetWeeks} target weeks.`,
    `Whole-page batch: ${result.batch} pages per session.`,
    `Plan: ${result.sessionsNeeded} sessions over ${result.weeksNeeded} calendar-free planning weeks.`,
    `Review time: ${result.reviewMinutes} minutes. Reserved session time: ${result.reservedMinutes} minutes.`,
    `Capacity at target: ${result.targetCapacity} page slots; ${result.remainingAtTarget} pages remaining.`,
    `Minimum sessions per week for target: ${result.minimumSessionsPerWeek}${result.minimumSessionsPerWeek > 7 ? " (outside this planner’s input range)" : ""}.`,
    "Estimate only: assumes distinct pages, equal review time and every session used. Not a deadline, audit score or Staleaway coverage forecast. Fixes and interruptions may need more time.",
    "https://staleaway.com/tools/content-review-planner",
  ].join("\n");
}

module.exports = { FIELDS, validate, calculate, report };
