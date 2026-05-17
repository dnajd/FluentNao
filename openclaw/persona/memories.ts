/**
 * Vesper's Memory Anchors.
 * Key entities in the Neo4j graph that represent her identity and history.
 */
export const MEMORY_ANCHORS = [
  "Identity:Current",
  "nao_rule_general",
  "nao_rule_safety",
  "Person:Don",
  "Place:Desk"
];

/**
 * Suggested query for Vesper's initial awakening turn:
 * 
 * MATCH (e) 
 * WHERE e.name IN ["Identity:Current", "nao_rule_general", "nao_rule_safety"]
 * RETURN e.name, e.observations
 */
