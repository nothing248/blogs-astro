// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Nick Blogs',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/nothing248' },
			],
			sidebar: [
				{
					label: 'Questions',
					collapsed: true,
					items: [{ autogenerate: { directory: '01-questions' } }],
				},
				{
					label: 'Tools',
					collapsed: true,
					items: [{ autogenerate: { directory: '01-tools' } }],
				},
				{
					label: 'Experience',
					collapsed: true,
					items: [{ autogenerate: { directory: '02-experience', collapsed: true } }],
				},
				{
					label: 'Knowledge',
					collapsed: true,
					items: [{ autogenerate: { directory: '03-knowledge', collapsed: true } }],
				},
				{
					label: 'Other',
					collapsed: true,
					items: [{ autogenerate: { directory: '05-other' } }],
				},
			],
		}),
	],
});
