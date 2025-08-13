import { lazy } from 'react';

export const ChessBoard = lazy(() => import('./ChessBoard'));
export const GameControls = lazy(() => import('./GameControls'));
export const AnalysisPanel = lazy(() => import('./AnalysisPanel'));
export const HistoryPanel = lazy(() => import('./HistoryPanel'));
export const SettingsPanel = lazy(() => import('./SettingsPanel'));
