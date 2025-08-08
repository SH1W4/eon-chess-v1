/**
 * Gera um ID único usando crypto.randomUUID() se disponível,
 * ou fallback para Math.random() se não estiver.
 */
export function generateId(): string {
  if (typeof crypto !== 'undefined' && crypto.randomUUID) {
    return crypto.randomUUID();
  }
  return Math.random().toString(36).substring(2, 15) + 
         Math.random().toString(36).substring(2, 15);
}
