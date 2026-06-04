import { readFileSync, writeFileSync } from 'fs';

const root = 'D:/Sistema Escolta/.understand-anything';
const graph = JSON.parse(readFileSync(`${root}/intermediate/merged-graph.json`, 'utf8'));
const layers = JSON.parse(readFileSync(`${root}/layers.json`, 'utf8'));
const tour = JSON.parse(readFileSync(`${root}/tour.json`, 'utf8'));

const knowledgeGraph = {
  version: '1.0',
  kind: 'codebase',
  project: {
    name: 'Sistema Escolta',
    languages: ['python', 'html', 'css', 'javascript', 'json', 'yaml'],
    frameworks: ['Django', 'Gunicorn', 'Whitenoise'],
    description: 'Sistema de gestão operacional para empresa de escolta armada. Gerencia agentes, viaturas, armamento, clientes, ordens de serviço, boletins de medição e módulo patrimonial (JR Segurança, JRS Facilities, Freelance).',
    analyzedAt: new Date().toISOString(),
    gitCommitHash: '0497b1e3bb259c7ee77ab6b5c4c3cb5b27c5ddeb'
  },
  nodes: graph.nodes,
  edges: graph.edges,
  layers: layers,
  tour: tour
};

writeFileSync(`${root}/knowledge-graph.json`, JSON.stringify(knowledgeGraph, null, 2));
console.log('Rebuilt knowledge-graph.json');
console.log('Nodes:', knowledgeGraph.nodes.length);
console.log('Edges:', knowledgeGraph.edges.length);
console.log('Layers:', knowledgeGraph.layers.length);
console.log('Tour steps:', knowledgeGraph.tour.length);
