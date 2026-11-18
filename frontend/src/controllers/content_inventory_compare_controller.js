import { Controller } from "@hotwired/stimulus";
import { FIELDS, GROUPS, LIMITS, compare, csv } from "../tools/content_inventory_compare";
import { extractPageUrls } from "../tools/sitemap_page_urls";

export default class extends Controller {
  static targets = ["fields", "input", "error", "summary", "unavailable", "result", "status", "counts", "rows", "listStats", "displayed", "download", "xml", "xmlStatus", "xmlOutput", "xmlUse"];

  connect() {
    this.fieldsTarget.disabled = false;
    this.unavailableTarget.hidden = true;
    this.calculate();
  }

  invalidate() {
    this.result = null;
    this.resultTarget.hidden = true;
    this.downloadTarget.disabled = true;
    this.rowsTarget.replaceChildren();
    this.countsTarget.replaceChildren();
    this.listStatsTarget.replaceChildren();
    this.displayedTarget.textContent = "";
    this.summaryTarget.hidden = true;
    this.summaryTarget.replaceChildren();
    this.inputTargets.forEach(input => input.removeAttribute("aria-invalid"));
    this.errorTargets.forEach(error => { error.textContent = ""; });
    this.statusTarget.textContent = "Inputs changed. Compare again; no current result is available.";
  }

  calculate(event) {
    if (event) event.preventDefault();
    this.invalidate();
    const raw = {};
    this.inputTargets.forEach(input => { raw[input.dataset.field] = input.value; });
    const result = compare(raw);
    if (result.status !== "ready") {
      const heading = document.createElement("p");
      heading.textContent = "Comparison not run. Correct these lists:";
      this.summaryTarget.append(heading);
      const list = document.createElement("ul");
      Object.entries(result.errors).forEach(([key, message]) => {
        const input = this.inputTargets.find(input => input.dataset.field === key);
        input.setAttribute("aria-invalid", "true");
        this.errorTargets.find(error => error.dataset.field === key).textContent = message;
        const item = document.createElement("li");
        const link = document.createElement("a");
        link.href = `#${input.id}`;
        link.textContent = `${FIELDS.find(field => field.key === key).label}: ${message}`;
        item.append(link);
        list.append(item);
      });
      this.summaryTarget.append(list);
      this.summaryTarget.hidden = false;
      this.statusTarget.textContent = "No comparison available. Invalid or missing input is not a clean result.";
      if (event) this.summaryTarget.focus();
      return;
    }
    this.result = result;
    FIELDS.forEach(({key, label}) => {
      const item = document.createElement("li");
      const stats = result.lists[key];
      item.textContent = `${label}: ${stats.urls.size} unique URLs; ${stats.duplicates} duplicate lines ignored; ${stats.blanks} blank lines ignored.`;
      this.listStatsTarget.append(item);
    });
    GROUPS.forEach(group => {
      const item = document.createElement("div");
      const term = document.createElement("dt");
      const detail = document.createElement("dd");
      term.textContent = group.label;
      detail.textContent = result.counts[group.key];
      item.append(term, detail);
      this.countsTarget.append(item);
    });
    result.rows.slice(0, LIMITS.displayed).forEach(row => {
      const item = document.createElement("li");
      const url = document.createElement("strong");
      const detail = document.createElement("p");
      url.textContent = row.url;
      detail.textContent = `${row.label}. Manual next step: ${row.action}.`;
      item.append(url, detail);
      this.rowsTarget.append(item);
    });
    this.displayedTarget.textContent = `Displaying ${Math.min(result.rows.length, LIMITS.displayed)} of ${result.rows.length} unique URLs in first-seen list order. Download includes every result row and all three presence flags.`;
    this.downloadTarget.disabled = false;
    this.resultTarget.hidden = false;
    this.statusTarget.textContent = `Comparison ready: ${result.rows.length} unique URLs across the three pasted lists. Membership only, not a pass/fail audit.`;
  }

  example() {
    this.inputTargets.forEach(input => { input.value = FIELDS.find(field => field.key === input.dataset.field).example; });
    this.invalidate();
    this.statusTarget.textContent = "Fictional example loaded. Compare lists to see its result.";
  }

  clear() {
    this.inputTargets.forEach(input => { input.value = ""; });
    this.xmlTarget.value = "";
    this.invalidateXml();
    this.invalidate();
    this.statusTarget.textContent = "Lists cleared. No comparison or download is available.";
    this.inputTargets[0].focus();
  }

  invalidateXml() {
    this.extraction = null;
    this.xmlOutputTarget.value = "";
    this.xmlUseTarget.disabled = true;
    this.xmlTarget.removeAttribute("aria-invalid");
    this.xmlStatusTarget.textContent = "No current extracted list. The three comparison lists are unchanged.";
  }

  extractXml() {
    this.invalidateXml();
    const result = extractPageUrls(this.xmlTarget.value);
    if (result.status !== "ready") {
      this.xmlTarget.setAttribute("aria-invalid", "true");
      this.xmlStatusTarget.textContent = result.error + " The three comparison lists are unchanged.";
      return;
    }
    this.extraction = result;
    this.xmlOutputTarget.value = result.text;
    this.xmlUseTarget.disabled = false;
    this.xmlStatusTarget.textContent = `${result.entries} page entries; ${result.unique} unique URLs; ${result.duplicates} duplicates removed. This is only the pasted file, not a complete website inventory. Review the list before replacing the selected sitemap input.`;
  }

  useXml() {
    if (!this.extraction) return;
    const input = this.inputTargets.find(input => input.dataset.field === "sitemap");
    input.value = this.extraction.text;
    this.invalidate();
    this.statusTarget.textContent = "Selected sitemap list replaced. Intended inventory and imported records are unchanged. Compare again; no current comparison is available.";
    input.focus();
  }

  download() {
    if (!this.result) return;
    const url = URL.createObjectURL(new Blob([csv(this.result)], { type: "text/csv;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = "content-inventory-comparison.csv";
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
    this.statusTarget.textContent = "Complete CSV download requested. The comparison is unchanged.";
  }
}
