import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';

const root = 'D:/Sistema Escolta';
const graph = JSON.parse(readFileSync(join(root, '.understand-anything/intermediate/assembled-graph.json'), 'utf8'));
const tour = JSON.parse(readFileSync(join(root, '.understand-anything/intermediate/tour.json'), 'utf8'));

const nodeIds = new Set(graph.nodes.map(n => n.id));

// Fix step 12: migration references
const step12 = tour.find(s => s.step === 12);
if (step12) {
  const validMigrations = ['file:cadastros/migrations/0022_despesaos_trocamotorista_parada_incidente_and_more.py', 'file:cadastros/migrations/0045_funcionariopatrimonial_empresa_freelance.py'];
  step12.nodeIds = validMigrations;
  console.log('Fixed step 12 migration references');
}

// Remove dangling tour edges and re-add
graph.edges = graph.edges.filter(e => {
  if (e.type === 'starts_with' || e.type === 'next_step' || (e.type === 'related' && e.step)) {
    if (!nodeIds.has(e.source) || !nodeIds.has(e.target)) return false;
  }
  return true;
});

// Remove old tour node and tour-specific edges
graph.nodes = graph.nodes.filter(n => n.id !== 'tour:main');
graph.edges = graph.edges.filter(e => {
  if (e.source === 'tour:main') return false;
  if (e.type === 'starts_with') return false;
  if (e.type === 'next_step') return false;
  if (e.type === 'related' && e.step) return false;
  return true;
});

// Re-add clean tour
graph.nodes.push({
  id: 'tour:main',
  type: 'tour',
  label: 'Tour Guiado do Sistema Escolta',
  summary: 'Tour com 14 passos cobrindo a arquitetura completa do Sistema Escolta.',
  tags: ['tour', 'aprendizado'],
  complexity: 'moderate',
  steps: tour
});

for (const step of tour) {
  graph.edges.push({
    source: 'tour:main',
    target: step.nodeIds[0],
    type: 'starts_with',
    step: step.step,
    weight: 0.8
  });
  for (let i = 0; i < step.nodeIds.length - 1; i++) {
    graph.edges.push({
      source: step.nodeIds[i],
      target: step.nodeIds[i + 1],
      type: 'related',
      step: step.step,
      weight: 0.4
    });
  }
  if (step.step < tour.length) {
    const nextStep = tour[step.step];
    graph.edges.push({
      source: step.nodeIds[step.nodeIds.length - 1],
      target: nextStep.nodeIds[0],
      type: 'next_step',
      weight: 0.6
    });
  }
}

// Remove any remaining dangling edges
const finalNodeIds = new Set(graph.nodes.map(n => n.id));
const before = graph.edges.length;
graph.edges = graph.edges.filter(e => finalNodeIds.has(e.source) && finalNodeIds.has(e.target));
const removed = before - graph.edges.length;

writeFileSync(join(root, '.understand-anything/intermediate/assembled-graph.json'), JSON.stringify(graph, null, 2));
writeFileSync(join(root, '.understand-anything/intermediate/tour.json'), JSON.stringify(tour, null, 2));

console.log(`Fixed tour. Removed ${removed} dangling edges.`);
console.log(`Final: ${graph.nodes.length} nodes, ${graph.edges.length} edges`);
