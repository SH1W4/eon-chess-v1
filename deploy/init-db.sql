-- AEON Chess Database Initialization Script

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Create schema
CREATE SCHEMA IF NOT EXISTS aeon;

-- Set default schema
SET search_path TO aeon, public;

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    elo_rating INTEGER DEFAULT 1200,
    games_played INTEGER DEFAULT 0,
    games_won INTEGER DEFAULT 0,
    games_drawn INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS games (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    white_player_id UUID REFERENCES users(id),
    black_player_id UUID REFERENCES users(id),
    pgn TEXT,
    result VARCHAR(10), -- '1-0', '0-1', '1/2-1/2', '*'
    opening_name VARCHAR(100),
    eco_code VARCHAR(10),
    time_control VARCHAR(20),
    rated BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMP WITH TIME ZONE
);

CREATE TABLE IF NOT EXISTS moves (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    game_id UUID REFERENCES games(id) ON DELETE CASCADE,
    move_number INTEGER NOT NULL,
    is_white_move BOOLEAN NOT NULL,
    from_square VARCHAR(2) NOT NULL,
    to_square VARCHAR(2) NOT NULL,
    piece_type VARCHAR(10) NOT NULL,
    captured_piece VARCHAR(10),
    promotion_piece VARCHAR(10),
    is_check BOOLEAN DEFAULT false,
    is_checkmate BOOLEAN DEFAULT false,
    is_castling BOOLEAN DEFAULT false,
    is_en_passant BOOLEAN DEFAULT false,
    fen_after TEXT NOT NULL,
    time_spent INTEGER, -- milliseconds
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS cultural_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    aggression_weight FLOAT DEFAULT 0.5,
    defense_weight FLOAT DEFAULT 0.5,
    creativity_weight FLOAT DEFAULT 0.5,
    patience_weight FLOAT DEFAULT 0.5,
    complexity_weight FLOAT DEFAULT 0.5,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    elo_rating INTEGER DEFAULT 1500,
    play_style VARCHAR(50),
    opening_book_depth INTEGER DEFAULT 10,
    endgame_knowledge_level INTEGER DEFAULT 5,
    time_management_style VARCHAR(50),
    risk_tolerance FLOAT DEFAULT 0.5,
    learning_rate FLOAT DEFAULT 0.1,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_games_players ON games(white_player_id, black_player_id);
CREATE INDEX idx_games_created ON games(created_at DESC);
CREATE INDEX idx_moves_game ON moves(game_id, move_number);
CREATE INDEX idx_users_rating ON users(elo_rating DESC);

-- Create functions for updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- Insert default data
INSERT INTO cultural_profiles (name, description, aggression_weight, defense_weight, creativity_weight, patience_weight, complexity_weight) VALUES
('Aggressive', 'Estilo agressivo focado em ataques diretos', 0.8, 0.2, 0.5, 0.3, 0.6),
('Defensive', 'Estilo defensivo focado em solidez posicional', 0.2, 0.8, 0.3, 0.7, 0.4),
('Balanced', 'Estilo equilibrado e adaptativo', 0.5, 0.5, 0.5, 0.5, 0.5),
('Creative', 'Estilo criativo com jogadas não convencionais', 0.6, 0.4, 0.9, 0.4, 0.8),
('Positional', 'Estilo posicional focado em pequenas vantagens', 0.3, 0.6, 0.4, 0.8, 0.7);

INSERT INTO ai_profiles (name, description, elo_rating, play_style, risk_tolerance, learning_rate) VALUES
('Novice', 'IA iniciante para novos jogadores', 800, 'random', 0.7, 0.2),
('Intermediate', 'IA intermediária com conhecimento básico', 1200, 'balanced', 0.5, 0.15),
('Advanced', 'IA avançada com bom conhecimento tático', 1600, 'positional', 0.4, 0.1),
('Expert', 'IA expert com profundo conhecimento', 2000, 'strategic', 0.3, 0.05),
('Master', 'IA mestre com jogo quase perfeito', 2400, 'optimal', 0.2, 0.01);

-- Grant permissions
GRANT ALL PRIVILEGES ON SCHEMA aeon TO aeon_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA aeon TO aeon_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA aeon TO aeon_user;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA aeon TO aeon_user;
