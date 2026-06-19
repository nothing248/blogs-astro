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
					label: '工具',
					collapsed: true,
					items: [{ autogenerate: { directory: '01-tools' } }],
				},
				{
					label: '经验',
					collapsed: true,
					items: [{ autogenerate: { directory: '02-experience', collapsed: true } }],
				},
				{
					label: '知识',
					collapsed: true,
					items: [{ autogenerate: { directory: '03-knowledge', collapsed: true } }],
				},
				{
					label: '问题',
					collapsed: true,
					items: [{ autogenerate: { directory: '01-questions' } }],
				},
				{
					label: '其他',
					collapsed: true,
					items: [{ autogenerate: { directory: '05-other' } }],
				},
			],
		}),
	],
});
