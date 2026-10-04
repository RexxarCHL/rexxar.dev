# rexxar.dev

Personal site of Chia-Hung (Rexxar) Lin, built with [Astro](https://astro.build) as a static site.

## Editing content

| What | Where |
|---|---|
| Intro, headline, links | `src/data/about.md` |
| Experience, education, patents, skills | `src/data/resume.yaml` |
| Projects (one file each) | `src/content/projects/*.md` |
| Photo | `src/assets/profile.jpg` |

To add a project, copy an existing file in `src/content/projects/` and edit it. The `order` field controls sorting, and the first three projects appear on the home page.

## Running locally

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs to dist/
npm run check    # type-check
```

## Deploying

Cloudflare builds and deploys every push to `main`.

- Build command: `npm run build`
- Output directory: `dist`
