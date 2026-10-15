const assert = require("assert").strict;
const { FIELDS, validate, calculate, report } = require("../src/tools/review_planner");
const example = Object.fromEntries(FIELDS.map(field => [field.key, field.example]));
let checks = 0;
const r = calculate(example);
assert.equal(r.status, "ready");
assert.deepEqual([r.batch, r.sessionsNeeded, r.weeksNeeded, r.reviewMinutes, r.reservedMinutes, r.targetCapacity, r.remainingAtTarget, r.minimumSessionsPerWeek], [3, 20, 10, 480, 600, 48, 12, 3]);
checks++;
for (const field of FIELDS) {
  for (const invalid of ["", " ", "0", "-1", "1.5", "1e2", "Infinity", "NaN", "１２", "١٢", "+1", "1 2", "1,000", "9".repeat(10000), "<script>", String(field.max + 1), null, undefined, 2]) {
    const raw = { ...example, [field.key]: invalid };
    assert.equal(calculate(raw).status, "invalid", `${field.key}: ${String(invalid).slice(0, 20)}`);
    assert.ok(validate(raw).errors[field.key]);
    assert.equal(report(calculate(raw)), "");
    checks++;
  }
  for (const valid of ["1", String(field.max), " 2 ", "\t2\n", "\u00a02\u00a0", "000002"]) {
    assert.equal(validate({ ...example, [field.key]: valid }).errors[field.key], undefined);
    checks++;
  }
}
assert.equal(calculate({ ...example, minutesPerPage: "31" }).status, "cannot-fit");
assert.equal(report(calculate({ ...example, minutesPerPage: "31" })), "");
checks++;
const single = calculate({ pages: "1", minutesPerPage: "1", sessionMinutes: "480", sessionsPerWeek: "7", targetWeeks: "1" });
assert.deepEqual([single.batch, single.sessionsNeeded, single.weeksNeeded, single.reservedMinutes, single.remainingAtTarget], [1, 1, 1, 480, 0]);
checks++;
const partial = calculate({ ...example, pages: "7", minutesPerPage: "10", sessionMinutes: "30", targetWeeks: "1" });
assert.deepEqual([partial.batch, partial.sessionsNeeded, partial.weeksNeeded, partial.reviewMinutes, partial.reservedMinutes, partial.remainingAtTarget], [3, 3, 2, 70, 90, 1]);
checks++;
const max = calculate({ pages: "100000", minutesPerPage: "480", sessionMinutes: "480", sessionsPerWeek: "1", targetWeeks: "1" });
assert.deepEqual([max.batch, max.sessionsNeeded, max.weeksNeeded, max.reviewMinutes, max.minimumSessionsPerWeek], [1, 100000, 100000, 48000000, 100000]);
assert.ok(report(max).includes("outside this planner’s input range"));
checks++;
// Independently simulate completing distinct pages in short schedules. This catches
// fractional-page carryover, final-batch rounding and target-capacity errors.
for (let pages = 1; pages <= 23; pages++) {
  for (let minutes = 1; minutes <= 7; minutes++) {
    for (let session = minutes; session <= 15; session++) {
      let sessions = 0;
      let left = pages;
      while (left > 0) {
        let time = session;
        while (left > 0 && time >= minutes) { left--; time -= minutes; }
        sessions++;
      }
      const simulated = calculate({ pages: String(pages), minutesPerPage: String(minutes), sessionMinutes: String(session), sessionsPerWeek: "3", targetWeeks: "2" });
      assert.equal(simulated.sessionsNeeded, sessions);
      assert.equal(simulated.weeksNeeded, Math.ceil(sessions / 3));
      assert.equal(simulated.reservedMinutes, sessions * session);
      assert.ok(simulated.reservedMinutes >= simulated.reviewMinutes);
      assert.equal(simulated.remainingAtTarget > 0, sessions > 6);
      checks++;
    }
  }
}
assert.ok(report(r).includes("60 pages; 8 minutes per page; 30 minutes per session; 2 sessions per week; 8 target weeks."));
assert.ok(report(r).includes("Not a deadline, audit score or Staleaway coverage forecast."));
console.log(`${checks} review planner calculation and boundary cases passed (no network).`);
