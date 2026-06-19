import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { docsSchema } from '@astrojs/starlight/schema';

export const collections = {
	docs: defineCollection({
		loader: glob({
			pattern: [
				'**/*.{md,mdx}',
				'!00-inbox/**',
				'!00-resources/**',
				'!00-archive/**',
			],
			base: './src/content/docs',
		}),
		schema: docsSchema(),
	}),
};
