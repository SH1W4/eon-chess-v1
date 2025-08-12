// Padrões de fundo culturais
export const patterns = {
  castle: `
    radial-gradient(circle at center, rgba(0,0,0,0.1) 0%, transparent 70%),
    repeating-linear-gradient(45deg, rgba(0,0,0,0.05) 0px, rgba(0,0,0,0.05) 2px, transparent 2px, transparent 10px)
  `,
  floral: `
    radial-gradient(circle at center, rgba(0,0,0,0.1) 0%, transparent 70%),
    repeating-radial-gradient(circle at 50% 50%, rgba(0,0,0,0.05) 0, rgba(0,0,0,0.05) 10px, transparent 10px, transparent 20px)
  `,
  geometric: `
    linear-gradient(45deg, rgba(0,0,0,0.05) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.05) 75%, rgba(0,0,0,0.05)),
    linear-gradient(45deg, rgba(0,0,0,0.05) 25%, transparent 25%, transparent 75%, rgba(0,0,0,0.05) 75%, rgba(0,0,0,0.05))
  `,
  papyrus: `
    linear-gradient(90deg, rgba(0,0,0,0.05) 0px, transparent 1px),
    linear-gradient(0deg, rgba(0,0,0,0.05) 0px, transparent 1px)
  `,
} as const;
