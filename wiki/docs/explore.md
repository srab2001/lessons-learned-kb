---
title: "Explore Recommendations"
lifecycle: active
sensitivity: public
---

# Explore Recommendations

Search and filter all recommendations by keyword, capability, project, lesson type, or confidence level.

This page ships with the filtering UI wired up but no seeded data — the source repo this KB was bootstrapped from (`proposal-intelligence-kb`) had this page populated with its own business-specific proof points, which were not ported. Populate the `DATA` array below (or replace this page's generation step) once the first recommendation pages exist.

<div id="rec-explorer">
  <div class="explorer-controls">
    <input type="text" id="rec-search" placeholder="Search by keyword, metric, headline…" autocomplete="off" />
    <div class="explorer-filters">
      <select id="f-capability"><option value="">All capabilities</option></select>
      <select id="f-project"><option value="">All projects</option></select>
      <select id="f-lessontype"><option value="">All lesson types</option></select>
      <select id="f-confidence"><option value="">All confidence levels</option></select>
    </div>
    <div class="explorer-meta">
      <span id="rec-count"></span>
      <button id="rec-reset">Clear filters</button>
    </div>
  </div>
  <div id="rec-results"></div>
</div>

<style>
#rec-explorer {
  margin-top: 1.5rem;
}
.explorer-controls {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
}
#rec-search {
  width: 100%;
  padding: 0.6rem 0.9rem;
  font-size: 1rem;
  border: 1.5px solid var(--md-default-fg-color--lighter, #ccc);
  border-radius: 6px;
  background: var(--md-default-bg-color, #fff);
  color: var(--md-default-fg-color, #000);
  box-sizing: border-box;
}
#rec-search:focus {
  outline: none;
  border-color: var(--md-accent-fg-color, #4051b5);
}
.explorer-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}
.explorer-filters select {
  flex: 1;
  min-width: 140px;
  padding: 0.4rem 0.7rem;
  font-size: 0.875rem;
  border: 1.5px solid var(--md-default-fg-color--lighter, #ccc);
  border-radius: 6px;
  background: var(--md-default-bg-color, #fff);
  color: var(--md-default-fg-color, #000);
  cursor: pointer;
}
.explorer-meta {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.85rem;
  color: var(--md-default-fg-color--light, #666);
}
#rec-reset {
  font-size: 0.8rem;
  padding: 0.25rem 0.6rem;
  border: 1px solid currentColor;
  border-radius: 4px;
  background: none;
  cursor: pointer;
  color: var(--md-default-fg-color--light, #666);
}
#rec-reset:hover {
  background: var(--md-default-fg-color--lightest, #eee);
}
.rec-card {
  border: 1px solid var(--md-default-fg-color--lighter, #ddd);
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin-bottom: 0.75rem;
  background: var(--md-default-bg-color, #fff);
}
.rec-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
}
.rec-card h3 {
  margin: 0;
  font-size: 0.95rem;
  font-weight: 600;
  line-height: 1.3;
}
.rec-card h3 a {
  color: var(--md-primary-fg-color, #4051b5);
  text-decoration: none;
}
.rec-card h3 a:hover { text-decoration: underline; }
.rec-badge {
  display: inline-block;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  white-space: nowrap;
  flex-shrink: 0;
}
.badge-high { background: #d4edda; color: #155724; }
.badge-medium { background: #fff3cd; color: #856404; }
.badge-low { background: #f8d7da; color: #721c24; }
.rec-metric {
  font-size: 0.875rem;
  color: var(--md-default-fg-color--light, #555);
  margin-bottom: 0.6rem;
  line-height: 1.5;
}
.rec-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}
.rec-tag {
  font-size: 0.72rem;
  padding: 0.15rem 0.5rem;
  border-radius: 3px;
  background: var(--md-default-fg-color--lightest, #f0f0f0);
  color: var(--md-default-fg-color--light, #555);
}
.rec-tag.t-cap { background: #e8eaf6; color: #3949ab; }
.rec-tag.t-proj { background: #e3f2fd; color: #1565c0; }
.rec-tag.t-lt  { background: #f3e5f5; color: #6a1b9a; }
#rec-empty {
  text-align: center;
  padding: 2.5rem;
  color: var(--md-default-fg-color--light, #888);
  font-style: italic;
}
.highlight { background: #fff176; border-radius: 2px; }
</style>

<script>
(function() {
  // Seed data is intentionally empty — see the note above this widget.
  const DATA = [];

  function unique(arr, key) {
    return [...new Set(arr.map(d => d[key]).filter(Boolean))].sort();
  }

  function populate(selectId, values) {
    const sel = document.getElementById(selectId);
    const first = sel.options[0];
    sel.innerHTML = '';
    sel.appendChild(first);
    values.forEach(v => {
      const opt = document.createElement('option');
      opt.value = v;
      opt.textContent = v;
      sel.appendChild(opt);
    });
  }

  function hl(text, q) {
    if (!q) return text;
    const escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return text.replace(new RegExp(`(${escaped})`, 'gi'), '<mark class="highlight">$1</mark>');
  }

  function render(items, q) {
    const container = document.getElementById('rec-results');
    const count = document.getElementById('rec-count');
    count.textContent = `${items.length} of ${DATA.length} recommendations`;
    if (items.length === 0) {
      container.innerHTML = '<div id="rec-empty">No recommendations yet. Run a synthesis session to populate this KB.</div>';
      return;
    }
    container.innerHTML = items.map(rec => {
      const badgeClass = rec.confidence === 'high' ? 'badge-high' : rec.confidence === 'medium' ? 'badge-medium' : 'badge-low';
      const tags = [
        rec.capability ? `<span class="rec-tag t-cap">${hl(rec.capability, q)}</span>` : '',
        rec.project    ? `<span class="rec-tag t-proj">${hl(rec.project, q)}</span>` : '',
        rec.lesson_type? `<span class="rec-tag t-lt">${hl(rec.lesson_type, q)}</span>` : '',
      ].filter(Boolean).join('');
      return `
        <div class="rec-card">
          <div class="rec-card-header">
            <h3><a href="${rec.page}">${hl(rec.headline, q)}</a></h3>
            <span class="rec-badge ${badgeClass}">${rec.confidence}</span>
          </div>
          <div class="rec-metric">${hl(rec.metric, q)}…</div>
          <div class="rec-tags">${tags}</div>
        </div>`;
    }).join('');
  }

  function filter() {
    const q = document.getElementById('rec-search').value.trim().toLowerCase();
    const cap = document.getElementById('f-capability').value;
    const proj = document.getElementById('f-project').value;
    const lt  = document.getElementById('f-lessontype').value;
    const conf= document.getElementById('f-confidence').value;

    const results = DATA.filter(rec => {
      if (cap  && rec.capability !== cap) return false;
      if (proj && rec.project    !== proj) return false;
      if (lt   && rec.lesson_type!== lt)  return false;
      if (conf && rec.confidence !== conf) return false;
      if (q) {
        const haystack = [rec.headline, rec.metric, rec.capability, rec.project, rec.lesson_type].join(' ').toLowerCase();
        if (!haystack.includes(q)) return false;
      }
      return true;
    });
    render(results, q);
  }

  document.addEventListener('DOMContentLoaded', function() {
    populate('f-capability',  unique(DATA, 'capability'));
    populate('f-project',     unique(DATA, 'project'));
    populate('f-lessontype',  unique(DATA, 'lesson_type'));
    populate('f-confidence',  unique(DATA, 'confidence'));

    ['rec-search','f-capability','f-project','f-lessontype','f-confidence'].forEach(id => {
      document.getElementById(id).addEventListener('input', filter);
    });
    document.getElementById('rec-reset').addEventListener('click', function() {
      document.getElementById('rec-search').value = '';
      ['f-capability','f-project','f-lessontype','f-confidence'].forEach(id => {
        document.getElementById(id).value = '';
      });
      filter();
    });

    render(DATA, '');
  });
})();
</script>
