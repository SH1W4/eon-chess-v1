import React from 'react';
import Head from 'next/head';
import ARKITECTDashboard from '../components/ARKITECTDashboard';

const ARKITECTPage: React.FC = () => {
  return (
    <>
      <Head>
        <title>ARKITECT Dashboard - AEON Chess</title>
        <meta name="description" content="Sistema de Controle de Complexidade Arquitetural ARKITECT" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      
      <ARKITECTDashboard />
    </>
  );
};

export default ARKITECTPage;
