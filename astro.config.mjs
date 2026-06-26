// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightGitHubAlerts from 'starlight-github-alerts';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'Nick Blogs',
			plugins: [
				starlightGitHubAlerts(),
			],
			head: [
				{
					tag: 'script',
					attrs: {
						async: true,
						src: 'https://www.googletagmanager.com/gtag/js?id=G-T2R62ZENL5',
					},
				},
				{
					tag: 'script',
					content: `
						window.dataLayer = window.dataLayer || [];
						function gtag(){dataLayer.push(arguments);}
						gtag('js', new Date());
						gtag('config', 'G-T2R62ZENL5');
					`,
				},
			],
			locales: {
				root: {
					label: "简体中文",
					lang: "zh-CN",
				}
			},
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
					label: '方案',
					collapsed: true,
					items: [{ autogenerate: { directory: '04-solution', collapsed: true } }],
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

