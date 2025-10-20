/**
 * Main App Component
 * Bio Supply Digital Twin - Frontend
 */

import { ConfigProvider, Layout, theme } from 'antd';
import { Dashboard } from '../features/dashboard/Dashboard';
import './App.css';

const { Header, Content, Footer } = Layout;

function App() {
  return (
    <ConfigProvider
      theme={{
        algorithm: theme.defaultAlgorithm,
        token: {
          colorPrimary: '#1890ff',
          borderRadius: 6,
        },
      }}
    >
      <Layout style={{ minHeight: '100vh' }}>
        <Header style={{ 
          display: 'flex', 
          alignItems: 'center',
          background: '#001529',
          padding: '0 50px'
        }}>
          <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold' }}>
            🧬 Bio Supply Digital Twin
          </div>
        </Header>
        
        <Content style={{ padding: '0 50px', marginTop: 24 }}>
          <Dashboard />
        </Content>
        
        <Footer style={{ textAlign: 'center', background: '#f0f2f5' }}>
          Bio Supply Digital Twin ©2025 | 
          <span style={{ margin: '0 8px' }}>Built with React + TypeScript + Ant Design</span> |
          <span style={{ marginLeft: 8 }}>
            Microservices: Django + FastAPI + Redis + MQTT
          </span>
        </Footer>
      </Layout>
    </ConfigProvider>
  );
}

export default App;
