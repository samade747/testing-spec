import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
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
