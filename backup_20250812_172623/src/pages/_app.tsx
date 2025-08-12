import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { MemoizedLayout } from '../web/components/layout/Layout';

export default function App({ Component, pageProps }: AppProps) {
  return (
    <MemoizedLayout>
      <Component {...pageProps} />
    </MemoizedLayout>
  );
}
