// PostgreSQL removed - using file-based storage instead
// See python/mesh_toolkit/src/mesh_toolkit/persistence/repository.py for persistence layer

// User types for compatibility with server/storage.ts
export type User = {
  id: number;
  username: string;
  password: string;
};

export type InsertUser = Omit<User, 'id'>;

// Placeholder for users table (not actually used since we're using MemStorage)
export const users = {};
