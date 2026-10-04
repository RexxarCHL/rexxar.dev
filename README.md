# rexxar.dev

Personal site of Chia-Hung (Rexxar) Lin, built with [Astro](https://astro.build) as a static site.

## Editing content

| What | Where |
|---|---|
| Intro, headline, links | `src/data/about.md` |
| Experience, education, patents, skills | `src/data/resume.yaml` |
| Projects (one file each) | `src/content/projects/*.md` |
| Photo | `src/assets/profile.jpg` |
| Resume PDF (no phone number) | `public/resume.pdf` |

To add a project, copy an existing file in `src/content/projects/` and edit it. The `order` field controls sorting, and the first three projects appear on the home page.

## Running locally

```sh
npm install
npm run dev      # http://localhost:4321
npm run build    # outputs to dist/
npm run check    # type-check
```

## Deploying

Cloudflare Workers Builds deploys every push to `main` to the `rexxar-dev` Worker, which serves rexxar.dev. `wrangler.jsonc` tells it to serve the static files in `dist/`.

- Build command: `npm run build`
- Deploy command: `npx wrangler deploy`

## Credits

The visual design is adapted from [Minimalist Light & Dark Theme Portfolio](https://astro.build/themes/details/minimalist-litght-dark-theme-portfolio/) by Javier Castillo, which is listed as MIT. The original is built with React and Tailwind. This version is plain Astro and CSS.
