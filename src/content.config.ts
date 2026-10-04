import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const projects = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/projects' }),
  schema: z.object({
    title: z.string(),
    org: z.string(),
    date: z.coerce.string(),
    order: z.number(),
    tags: z.array(z.string()),
    summary: z.string(),
    links: z.array(z.object({ label: z.string(), url: z.url() })).default([]),
  }),
});

export const collections = { projects };
