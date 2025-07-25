import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../constants/theme';

// Screens
import HomeScreen from '../screens/HomeScreen';
import GameScreen from '../screens/GameScreen';
import AICoachScreen from '../screens/AICoachScreen';
import CulturalScreen from '../screens/CulturalScreen';
import ProfileScreen from '../screens/ProfileScreen';
import AnalysisScreen from '../screens/AnalysisScreen';
import SettingsScreen from '../screens/SettingsScreen';

export type RootStackParamList = {
  MainTabs: undefined;
  Game: { gameMode?: string };
  Analysis: { gameId?: string };
  Settings: undefined;
};

export type MainTabParamList = {
  Home: undefined;
  AICoach: undefined;
  Cultural: undefined;
  Profile: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();

const MainTabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName: keyof typeof Ionicons.glyphMap;

          switch (route.name) {
            case 'Home':
              iconName = focused ? 'home' : 'home-outline';
              break;
            case 'AICoach':
              iconName = focused ? 'brain' : 'brain-outline';
              break;
            case 'Cultural':
              iconName = focused ? 'library' : 'library-outline';
              break;
            case 'Profile':
              iconName = focused ? 'person' : 'person-outline';
              break;
            default:
              iconName = 'help-outline';
          }

          return <Ionicons name={iconName} size={size} color={color} />;
        },
        tabBarActiveTintColor: Colors.secondary,
        tabBarInactiveTintColor: Colors.textMuted,
        tabBarStyle: {
          backgroundColor: Colors.surface,
          borderTopColor: Colors.primary,
          borderTopWidth: 1,
          paddingBottom: 5,
          paddingTop: 5,
          height: 60,
        },
        tabBarLabelStyle: {
          fontSize: 12,
          fontWeight: '500',
        },
        headerStyle: {
          backgroundColor: Colors.primary,
        },
        headerTintColor: Colors.text,
        headerTitleStyle: {
          fontWeight: 'bold',
          fontSize: 18,
        },
      })}
    >
      <Tab.Screen 
        name="Home" 
        component={HomeScreen}
        options={{
          title: 'XadrezMaster',
          tabBarLabel: 'Início',
        }}
      />
      <Tab.Screen 
        name="AICoach" 
        component={AICoachScreen}
        options={{
          title: 'EstrategiX',
          tabBarLabel: 'IA Coach',
        }}
      />
      <Tab.Screen 
        name="Cultural" 
        component={CulturalScreen}
        options={{
          title: 'Narrativas Culturais',
          tabBarLabel: 'Cultura',
        }}
      />
      <Tab.Screen 
        name="Profile" 
        component={ProfileScreen}
        options={{
          title: 'Perfil',
          tabBarLabel: 'Perfil',
        }}
      />
    </Tab.Navigator>
  );
};

export const AppNavigator = () => {
  return (
    <NavigationContainer
      theme={{
        dark: true,
        colors: {
          primary: Colors.primary,
          background: Colors.background,
          card: Colors.surface,
          text: Colors.text,
          border: Colors.primary,
          notification: Colors.secondary,
        },
      }}
    >
      <Stack.Navigator
        screenOptions={{
          headerStyle: {
            backgroundColor: Colors.primary,
          },
          headerTintColor: Colors.text,
          headerTitleStyle: {
            fontWeight: 'bold',
          },
        }}
      >
        <Stack.Screen 
          name="MainTabs" 
          component={MainTabNavigator}
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="Game" 
          component={GameScreen}
          options={{
            title: 'Partida',
            headerBackTitle: 'Voltar',
          }}
        />
        <Stack.Screen 
          name="Analysis" 
          component={AnalysisScreen}
          options={{
            title: 'Análise',
            headerBackTitle: 'Voltar',
          }}
        />
        <Stack.Screen 
          name="Settings" 
          component={SettingsScreen}
          options={{
            title: 'Configurações',
            headerBackTitle: 'Voltar',
          }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

