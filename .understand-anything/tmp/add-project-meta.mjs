import { readFileSync, writeFileSync } from 'fs';

const kgPath = 'D:/Sistema Escolta/.understand-anything/knowledge-graph.json';
const layersPath = 'D:/Sistema Escolta/.understand-anything/layers.json';
const tourPath = 'D:/Sistema Escolta/.understand-anything/tour.json';

const kg = JSON.parse(readFileSync(kgPath, 'utf8'));
const layers = JSON.parse(readFileSync(layersPath, 'utf8'));
const tour = JSON.parse(readFileSync(tourPath, 'utf8'));

const fullKg = {
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
  nodes: kg.nodes,
  edges: kg.edges,
  layers: layers,
  tour: tour
};

writeFileSync(kgPath, JSON.stringify(fullKg, null, 2));
console.log('Updated knowledge-graph.json');
console.log('Nodes:', fullKg.nodes.length);
console.log('Edges:', fullKg.edges.length);
console.log('Layers:', fullKg.layers.length);
console.log('Tour steps:', fullKg.tour.length);
console.log('Has project:', !!fullKg.project);
console.log('Has version:', !!fullKg.version);
