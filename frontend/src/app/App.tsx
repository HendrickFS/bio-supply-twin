/**
 * Main App Component
 * Bio Supply Digital Twin - Frontend
 */

import { ConfigProvider, Layout, Menu, theme } from 'antd';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { DashboardOutlined, EnvironmentOutlined, ExperimentOutlined } from '@ant-design/icons';
import { Dashboard } from '../features/dashboard/Dashboard';
import { BoxTracking } from '../features/transport-boxes/BoxTracking';
import { BoxSamples } from '../features/transport-boxes/BoxSamples';
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
      <Router>
        <Layout style={{ minHeight: '100vh' }}>
          <Header style={{ 
            display: 'flex', 
            alignItems: 'center',
            background: '#001529',
            padding: '0 50px'
          }}>
            <div style={{ color: 'white', fontSize: '20px', fontWeight: 'bold', marginRight: '50px' }}>
              🧬 Bio Supply Digital Twin
            </div>
            
            <Menu
              theme="dark"
              mode="horizontal"
              defaultSelectedKeys={['dashboard']}
              style={{ flex: 1, minWidth: 0 }}
              items={[
                {
                  key: 'dashboard',
                  icon: <DashboardOutlined />,
                  label: <Link to="/">Dashboard</Link>,
                },
                {
                  key: 'tracking',
                  icon: <EnvironmentOutlined />,
                  label: <Link to="/tracking">Box Tracking</Link>,
                },
                {
                  key: 'samples',
                  icon: <ExperimentOutlined />,
                  label: <Link to="/samples">Box Samples</Link>,
                },
              ]}
            />
          </Header>
          
          <Content style={{ padding: '0 50px', marginTop: 24 }}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/tracking" element={<BoxTracking />} />
              <Route path="/samples" element={<BoxSamples />} />
            </Routes>
          </Content>
          
          <Footer style={{ textAlign: 'center', background: '#f0f2f5' }}>
            Bio Supply Digital Twin ©2025 | 
            <span style={{ margin: '0 8px' }}>Built with React + TypeScript + Ant Design</span> |
            <span style={{ marginLeft: 8 }}>
              Microservices: Django + FastAPI + Redis + MQTT
            </span>
          </Footer>
        </Layout>
      </Router>
    </ConfigProvider>
  );
}

export default App;
