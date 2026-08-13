# Public Resources for VA.gov Technical Research

> **Maintenance note:** This file contains ~80 hardcoded URLs. Periodically verify that links still resolve, especially the Scroll Help (`scrollhelp.site`) URLs — these are Confluence-exported paths with numeric page IDs (e.g., `...1844215878.html`) that break when pages are moved or renamed.

A curated list of publicly accessible documentation and repositories. Use `fetch_webpage` to pull content from these URLs when answering designer questions.

## VA Design System (VADS) — design.va.gov

The primary source for component documentation, patterns, and design guidance.

| Resource | URL |
|---|---|
| **Home** | `https://design.va.gov/` |
| **Components index** | `https://design.va.gov/components/` |
| **Individual component** | `https://design.va.gov/components/{name}` |
| **Patterns index** | `https://design.va.gov/patterns/` |
| **Templates index** | `https://design.va.gov/templates/` |
| **Form templates** | `https://design.va.gov/templates/forms/` |
| **Form accessibility** | `https://design.va.gov/templates/forms/accessibility-guidelines` |
| **Foundation (color, type, spacing)** | `https://design.va.gov/foundation/` |
| **Layout & grid** | `https://design.va.gov/foundation/layout` |
| **Utilities** | `https://design.va.gov/foundation/utilities` |
| **Content style guide** | `https://design.va.gov/content-style-guide/` |
| **Content principles** | `https://design.va.gov/content-style-guide/content-principles` |
| **Word list** | `https://design.va.gov/content-style-guide/word-list` |
| **SEO guidance** | `https://design.va.gov/content-style-guide/seo` |
| **What's new / changelog** | `https://design.va.gov/about/whats-new` |
| **Contributing** | `https://design.va.gov/about/contributing-to-the-design-system` |
| **For designers** | `https://design.va.gov/about/designers/` |
| **Design libraries (Figma)** | `https://design.va.gov/about/designers/design-libraries` |
| **For developers** | `https://design.va.gov/about/developers/` |
| **Using web components** | `https://design.va.gov/about/developers/using-web-components` |

### Common Component Pages

When a designer asks about a specific component, fetch its page. Common components include:

| Component | URL |
|---|---|
| Accordion | `https://design.va.gov/components/accordion` |
| Action link | `https://design.va.gov/components/action-link` |
| Additional info | `https://design.va.gov/components/additional-info` |
| Alert | `https://design.va.gov/components/alert` |
| Alert - Expandable | `https://design.va.gov/components/alert-expandable` |
| Back to top | `https://design.va.gov/components/back-to-top` |
| Banner | `https://design.va.gov/components/banner` |
| Breadcrumbs | `https://design.va.gov/components/breadcrumbs` |
| Button | `https://design.va.gov/components/button/` |
| Button group | `https://design.va.gov/components/button-group` |
| Card | `https://design.va.gov/components/card` |
| Checkbox | `https://design.va.gov/components/form/checkbox` |
| Crisis Line Modal | `https://design.va.gov/components/crisis-line-modal` |
| Date input | `https://design.va.gov/components/form/date-input` |
| Divider | `https://design.va.gov/components/divider` |
| Featured content | `https://design.va.gov/components/featured-content` |
| File input | `https://design.va.gov/components/form/file-input` |
| Header | `https://design.va.gov/components/header/` |
| Icon | `https://design.va.gov/components/icon` |
| Link | `https://design.va.gov/components/link` |
| Link - Action | `https://design.va.gov/components/link/action` |
| Loading indicator | `https://design.va.gov/components/loading-indicator` |
| Memorable date | `https://design.va.gov/components/form/memorable-date` |
| Modal | `https://design.va.gov/components/modal` |
| Number input | `https://design.va.gov/components/form/number-input` |
| On this page | `https://design.va.gov/components/on-this-page` |
| Pagination | `https://design.va.gov/components/pagination` |
| Privacy agreement | `https://design.va.gov/components/privacy-agreement` |
| Process list | `https://design.va.gov/components/process-list` |
| Progress bar - Activity | `https://design.va.gov/components/progress-bar/activity` |
| Progress bar - Segmented | `https://design.va.gov/components/progress-bar/segmented` |
| Promo banner | `https://design.va.gov/components/promo-banner` |
| Radio button | `https://design.va.gov/components/form/radio-button` |
| Search input | `https://design.va.gov/components/search-input` |
| Select | `https://design.va.gov/components/form/select` |
| Service tag | `https://design.va.gov/components/service-tag` |
| Summary box | `https://design.va.gov/components/summary-box` |
| Table | `https://design.va.gov/components/table` |
| Tag | `https://design.va.gov/components/tag` |
| Telephone | `https://design.va.gov/components/telephone` |
| Text input | `https://design.va.gov/components/form/text-input` |
| Textarea | `https://design.va.gov/components/form/textarea` |

> **Tip**: If a component isn't in this list, try `https://design.va.gov/components/{kebab-case-name}`. The design system is actively growing.

## Storybook — Live Component Demos

Interactive component playground with all variants and props.

| Resource | URL |
|---|---|
| **Storybook home** | `https://design.va.gov/storybook/?path=/docs/about-introduction--docs` |

> Storybook may not render well via `fetch_webpage`. If the designer needs interactive demos, provide the direct Storybook URL for them to visit in a browser.

## Platform Documentation

General platform guidance for teams building on VA.gov.

<!-- ⚠️ Scroll Help URLs are fragile — verify these periodically -->

| Resource | URL |
|---|---|
| **Platform docs home** | `https://depo-platform-documentation.scrollhelp.site/` |
| **Developer docs home** | `https://depo-platform-documentation.scrollhelp.site/developer-docs/` |
| **Getting started (frontend)** | `https://depo-platform-documentation.scrollhelp.site/developer-docs/Setting-up-your-local-frontend-environment.1844215878.html` |
| **Collaboration cycle** | `https://depo-platform-documentation.scrollhelp.site/collaboration-cycle/` |
| **Deployment schedule** | `https://depo-platform-documentation.scrollhelp.site/developer-docs/deployment-process` |
| **Deployment policies (holiday freeze, OOB)** | `https://depo-platform-documentation.scrollhelp.site/developer-docs/deployment-policies` |

## API Documentation

For questions about what data is available or what APIs exist.

| Resource | URL |
|---|---|
| **Developer.va.gov (API docs)** | `https://developer.va.gov/` |
| **Explore APIs** | `https://developer.va.gov/explore` |
| **Benefits APIs** | `https://developer.va.gov/explore/api/benefits-claims` |
| **Health APIs** | `https://developer.va.gov/explore/api/patient-health` |
| **Veteran Verification** | `https://developer.va.gov/explore/api/veteran-verification` |
| **Veteran Service History & Eligibility** | `https://developer.va.gov/explore/api/veteran-service-history-and-eligibility/docs` |
| **Internal vets-api Swagger spec** | `https://dev-api.va.gov/v0/apidocs` |
| **vets-api Swagger UI** | `https://department-of-veterans-affairs.github.io/va-digital-services-platform-docs/api-reference` |

## Public GitHub Repositories

All repos below are public and can be browsed via `fetch_webpage` using GitHub URLs.

| Repository | Purpose | URL |
|---|---|---|
| **vets-website** | VA.gov frontend (React apps) | `https://github.com/department-of-veterans-affairs/vets-website` |
| **component-library** | VADS web components source | `https://github.com/department-of-veterans-affairs/component-library` |
| **vets-api** | VA.gov backend (Ruby/Rails) | `https://github.com/department-of-veterans-affairs/vets-api` |
| **va.gov-team** | Team docs, research, decisions | `https://github.com/department-of-veterans-affairs/va.gov-team` |
| **content-build** | Static content build system | `https://github.com/department-of-veterans-affairs/content-build` |
| **vets-design-system-documentation** | Source for design.va.gov | `https://github.com/department-of-veterans-affairs/vets-design-system-documentation` |
| **va.gov-cms** | Drupal CMS for content | `https://github.com/department-of-veterans-affairs/va.gov-cms` |
| **veteran-facing-services-tools** | Shared tools & platform code | `https://github.com/department-of-veterans-affairs/veteran-facing-services-tools` |
| **next-build** | Next.js CMS content templating | `https://github.com/department-of-veterans-affairs/next-build` |
| **All org repositories** | Full list of 477+ repos | `https://github.com/orgs/department-of-veterans-affairs/repositories` |

### Browsing Repo Files

To look at source code or documentation within a repo:

- **File**: `https://github.com/department-of-veterans-affairs/{repo}/blob/main/{path}`
- **Directory**: `https://github.com/department-of-veterans-affairs/{repo}/tree/main/{path}`

Example paths in **vets-website** that are useful for understanding app structure:

- Applications directory: `.../tree/main/src/applications`
- Platform shared code: `.../tree/main/src/platform`
- Forms system: `.../tree/main/src/platform/forms-system`
- Forms config examples: `.../blob/main/src/applications/{app-name}/config/form.js`

Example paths in **component-library** for component source code:

- Web components source: `.../tree/main/packages/web-components/src/components`
- Specific component: `.../tree/main/packages/web-components/src/components/{va-component-name}`

## Feature Toggles & CSS Library

| Resource | URL |
|---|---|
| **Flipper feature toggle dashboard** | `https://staging-api.va.gov/flipper/features` |
| **VADS CSS Library (npm)** | `https://www.npmjs.com/package/@department-of-veterans-affairs/css-library` |

> The Flipper dashboard requires SOCKS proxy or network access to the VA staging environment.

## Figma

The VADS Figma library is where designers work day-to-day.

| Resource | URL |
|---|---|
| **VADS Component Library (Figma)** | `https://www.figma.com/file/afurtw4iqQe6y4gXfNfkkk/VADS-Component-Library` |
| **How to add the library** | `https://design.va.gov/about/designers/design-libraries` |

> Figma URLs require authentication and won't work with `fetch_webpage`. Provide these as links for the designer to open directly.

## Slack Channels (for when you can't find the answer)

When the documentation doesn't cover a question, suggest these channels:

- `#platform-design-system` — Questions about VADS components and patterns
- `#vfs-platform-support` — General platform support
- `#accessibility-help` — Accessibility-specific questions
- `#design` — General design community discussions
