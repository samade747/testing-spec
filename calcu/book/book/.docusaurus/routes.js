import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/book/__docusaurus/debug',
    component: ComponentCreator('/book/__docusaurus/debug', 'f31'),
    exact: true
  },
  {
    path: '/book/__docusaurus/debug/config',
    component: ComponentCreator('/book/__docusaurus/debug/config', '140'),
    exact: true
  },
  {
    path: '/book/__docusaurus/debug/content',
    component: ComponentCreator('/book/__docusaurus/debug/content', 'da6'),
    exact: true
  },
  {
    path: '/book/__docusaurus/debug/globalData',
    component: ComponentCreator('/book/__docusaurus/debug/globalData', '58b'),
    exact: true
  },
  {
    path: '/book/__docusaurus/debug/metadata',
    component: ComponentCreator('/book/__docusaurus/debug/metadata', 'ae0'),
    exact: true
  },
  {
    path: '/book/__docusaurus/debug/registry',
    component: ComponentCreator('/book/__docusaurus/debug/registry', 'a8a'),
    exact: true
  },
  {
    path: '/book/__docusaurus/debug/routes',
    component: ComponentCreator('/book/__docusaurus/debug/routes', 'a5a'),
    exact: true
  },
  {
    path: '/book/docs',
    component: ComponentCreator('/book/docs', 'a9f'),
    routes: [
      {
        path: '/book/docs',
        component: ComponentCreator('/book/docs', 'ad1'),
        routes: [
          {
            path: '/book/docs',
            component: ComponentCreator('/book/docs', 'a28'),
            routes: [
              {
                path: '/book/docs/chapter-1-getting-started',
                component: ComponentCreator('/book/docs/chapter-1-getting-started', '518'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book/docs/chapter-2-architecture',
                component: ComponentCreator('/book/docs/chapter-2-architecture', '758'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book/docs/chapter-3-frontend',
                component: ComponentCreator('/book/docs/chapter-3-frontend', '9ff'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book/docs/chapter-4-backend',
                component: ComponentCreator('/book/docs/chapter-4-backend', '597'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book/docs/chapter-5-rag-pipeline',
                component: ComponentCreator('/book/docs/chapter-5-rag-pipeline', 'd5c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book/docs/chapter-6-deployment',
                component: ComponentCreator('/book/docs/chapter-6-deployment', '4fe'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book/docs/intro',
                component: ComponentCreator('/book/docs/intro', '317'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/book/docs/rag-chatbot/',
                component: ComponentCreator('/book/docs/rag-chatbot/', '706'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
