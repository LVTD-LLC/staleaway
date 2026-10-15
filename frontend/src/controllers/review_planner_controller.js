import { Controller } from "@hotwired/stimulus";
import { FIELDS, calculate, report } from "../tools/review_planner";

export default class extends Controller {
  static targets = ["fields", "input", "error", "summary", "unavailable", "result", "status", "breakdown", "bottleneck", "export", "copyStatus", "copy", "download"];

  connect() {
    this.fieldsTarget.disabled = false;
    this.unavailableTarget.hidden = true;
    this.calculate();
  }

  invalidate() {
    this.resultTarget.hidden = true;
    this.exportTarget.value = "";
    this.copyTarget.disabled = true;
    this.downloadTarget.disabled = true;
    this.copyStatusTarget.textContent = "";
    this.statusTarget.textContent = "Inputs changed. Calculate again to update your estimate.";
    this.clearErrors();
  }

  clearErrors() {
    this.summaryTarget.hidden = true;
    this.summaryTarget.replaceChildren();
    this.inputTargets.forEach(input => input.removeAttribute("aria-invalid"));
    this.errorTargets.forEach(error => { error.textContent = ""; });
  }

  calculate(event) {
    if (event) event.preventDefault();
    this.invalidate();
    const raw = {};
    this.inputTargets.forEach(input => { raw[input.dataset.field] = input.value; });
    const result = calculate(raw);
    if (result.status === "invalid") {
      const heading = document.createElement("p");
      heading.textContent = "Check these values before calculating:";
      this.summaryTarget.append(heading);
      const list = document.createElement("ul");
      Object.entries(result.errors).forEach(([key, message]) => {
        const input = this.inputTargets.find(input => input.dataset.field === key);
        input.setAttribute("aria-invalid", "true");
        this.errorTargets.find(error => error.dataset.field === key).textContent = message;
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = `#${input.id}`;
        link.textContent = message;
        item.append(link);
        list.append(item);
      });
      this.summaryTarget.append(list);
      this.summaryTarget.hidden = false;
      this.statusTarget.textContent = "No estimate available until the values are corrected.";
      if (event) this.summaryTarget.focus();
      return;
    }
    if (result.status === "cannot-fit") {
      this.statusTarget.textContent = "One estimated page review does not fit in a session. Allow a longer session or reconsider the scope of each page review. Do not shorten a careful review just to fit the plan.";
      return;
    }
    this.statusTarget.textContent = "Estimate updated. These are planning weeks, not scheduled dates.";
    this.breakdownTarget.replaceChildren();
    const rows = [
      ["Whole pages per session", result.batch],
      ["Sessions needed", result.sessionsNeeded],
      ["Planning weeks needed", result.weeksNeeded],
      ["Estimated review minutes", result.reviewMinutes],
      ["Reserved session minutes", result.reservedMinutes],
      ["Page slots by target week", result.targetCapacity],
      ["Pages remaining at target", result.remainingAtTarget],
      ["Minimum weekly sessions for target", result.minimumSessionsPerWeek],
    ];
    rows.forEach(([label, value]) => {
      const group = document.createElement("div");
      const term = document.createElement("dt");
      const detail = document.createElement("dd");
      term.textContent = label;
      detail.textContent = value.toLocaleString("en-US");
      group.append(term, detail);
      this.breakdownTarget.append(group);
    });
    const unused = result.reservedMinutes - result.reviewMinutes;
    const range = result.minimumSessionsPerWeek > 7
      ? " The target needs more than seven sessions per week, outside this planner’s input range."
      : ` The target needs at least ${result.minimumSessionsPerWeek} session(s) per week at this batch size.`;
    this.bottleneckTarget.textContent = result.remainingAtTarget
      ? `The target has ${result.remainingAtTarget.toLocaleString("en-US")} more pages than available whole-page slots.${range} Try a smaller first-pass scope, longer sessions, more available weekly sessions or a longer planning window. Keep the time needed for a careful review.`
      : `The selected workload fits within the target under these assumptions.${range} Full sessions reserve ${unused.toLocaleString("en-US")} extra minutes beyond review time because pages are not split and the final batch may be smaller. Leave room for fixes and interruptions.`;
    this.exportTarget.value = report(result);
    this.copyTarget.disabled = false;
    this.downloadTarget.disabled = false;
    this.resultTarget.hidden = false;
  }

  reset() {
    this.inputTargets.forEach(input => { input.value = FIELDS.find(field => field.key === input.dataset.field).example; });
    this.calculate();
  }

  async copy() {
    const text = this.exportTarget.value;
    if (!text) return;
    try {
      await navigator.clipboard.writeText(text);
      this.copyStatusTarget.textContent = this.exportTarget.value === text ? "Estimate copied." : "Inputs changed; the previously calculated estimate was copied.";
    } catch {
      this.exportTarget.focus();
      this.exportTarget.select();
      this.copyStatusTarget.textContent = "Clipboard unavailable. Select and copy the plain-text estimate below, or download it.";
    }
  }

  download() {
    if (!this.exportTarget.value) return;
    const url = URL.createObjectURL(new Blob([this.exportTarget.value], { type: "text/plain;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "content-review-estimate.txt";
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    this.copyStatusTarget.textContent = "Plain-text estimate download requested.";
  }
}
