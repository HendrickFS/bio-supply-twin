/**
 * Dashboard - Main Overview Page
 * 
 * Displays key metrics, transport boxes, and samples
 */

import { useEffect, useState } from 'react';
import {
  Card,
  Row,
  Col,
  Statistic,
  Table,
  Tag,
  Space,
  Button,
  message,
  Typography,
  Alert,
  Spin,
} from 'antd';
import {
  InboxOutlined,
  ExperimentOutlined,
  AlertOutlined,
  ReloadOutlined,
  ThunderboltOutlined,
  CloudServerOutlined,
} from '@ant-design/icons';
import { apiService, type Stats, type TransportBox, type Sample } from '../../shared/services/api';
import type { ColumnsType } from 'antd/es/table';

const { Title } = Typography;

export const Dashboard = () => {
  const [stats, setStats] = useState<Stats | null>(null);
  const [boxes, setBoxes] = useState<TransportBox[]>([]);
  const [samples, setSamples] = useState<Sample[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsData, boxesData, samplesData] = await Promise.all([
        apiService.getStats(),
        apiService.getBoxes(),
        apiService.getSamples(),
      ]);
      
      setStats(statsData);
      setBoxes(boxesData);
      setSamples(samplesData);
      message.success('Data loaded successfully');
    } catch (error) {
      message.error('Failed to load data. Make sure backend services are running.');
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  const handleClearCache = async () => {
    try {
      await apiService.clearCache();
      message.success('Cache cleared! Next request will be slower (cache miss)');
      await fetchData();
    } catch (error) {
      message.error('Failed to clear cache');
    }
  };

  useEffect(() => {
    fetchData();
    // Auto-refresh every 5 minutes
    const interval = setInterval(fetchData, 300000);
    return () => clearInterval(interval);
  }, []);

  // Transport Boxes Table Columns
  const boxColumns: ColumnsType<TransportBox> = [
    {
      title: 'Box ID',
      dataIndex: 'box_id',
      key: 'box_id',
      render: (text: string) => <strong>{text}</strong>,
    },
    {
      title: 'Location',
      dataIndex: 'geolocation',
      key: 'geolocation',
    },
    {
      title: 'Temperature',
      dataIndex: 'temperature',
      key: 'temperature',
      render: (temp: number) => (
        <span style={{ color: temp > 8 || temp < 2 ? 'red' : 'green' }}>
          {temp.toFixed(1)}°C
        </span>
      ),
    },
    {
      title: 'Humidity',
      dataIndex: 'humidity',
      key: 'humidity',
      render: (humidity: number) => `${humidity.toFixed(1)}%`,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'active' ? 'green' : 'orange'}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Last Updated',
      dataIndex: 'last_updated',
      key: 'last_updated',
      render: (date: string) => new Date(date).toLocaleString(),
    },
  ];

  // Samples Table Columns
  const sampleColumns: ColumnsType<Sample> = [
    {
      title: 'Sample ID',
      dataIndex: 'sample_id',
      key: 'sample_id',
      render: (text: string) => <strong>{text}</strong>,
    },
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true,
    },
    {
      title: 'Temperature',
      dataIndex: 'temperature',
      key: 'temperature',
      render: (temp: number) => `${temp.toFixed(1)}°C`,
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'collected' ? 'blue' : 'green'}>
          {status.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Collected At',
      dataIndex: 'collected_at',
      key: 'collected_at',
      render: (date: string) => new Date(date).toLocaleString(),
    },
  ];

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '100px' }}>
        <Spin size="large" />
        <p style={{ marginTop: 20 }}>Loading Bio Supply Digital Twin...</p>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px' }}>
      {/* Header */}
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2} style={{ margin: 0 }}>
            🧬 Bio Supply Digital Twin Dashboard
          </Title>
        </Col>
        <Col>
          <Space>
            <Button
              icon={<ThunderboltOutlined />}
              onClick={handleClearCache}
              type="default"
            >
              Clear Cache
            </Button>
            <Button
              icon={<ReloadOutlined />}
              onClick={handleRefresh}
              loading={refreshing}
              type="primary"
            >
              Refresh
            </Button>
          </Space>
        </Col>
      </Row>

      {/* Cache Info Alert */}
      {stats?.from_cache && (
        <Alert
          message="Data loaded from Redis cache"
          description="Faster response time! 🚀"
          type="success"
          showIcon
          icon={<ThunderboltOutlined />}
          style={{ marginBottom: 24 }}
          closable
        />
      )}

      {/* Stats Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={12} lg={8}>
          <Card>
            <Statistic
              title="Transport Boxes"
              value={stats?.num_boxes || 0}
              prefix={<InboxOutlined />}
              valueStyle={{ color: '#3f8600' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={8}>
          <Card>
            <Statistic
              title="Biological Samples"
              value={stats?.num_samples || 0}
              prefix={<ExperimentOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={8}>
          <Card>
            <Statistic
              title="Active Alerts"
              value={stats?.num_active_alerts || 0}
              prefix={<AlertOutlined />}
              valueStyle={{ color: stats?.num_active_alerts ? '#cf1322' : '#3f8600' }}
            />
          </Card>
        </Col>
      </Row>

      {/* Transport Boxes Table */}
      <Card
        title={
          <Space>
            <InboxOutlined />
            <span>Transport Boxes</span>
          </Space>
        }
        style={{ marginBottom: 24 }}
        extra={
          <Tag color="blue" icon={<CloudServerOutlined />}>
            Real-time Monitoring
          </Tag>
        }
      >
        <Table
          columns={boxColumns}
          dataSource={boxes}
          rowKey="box_id"
          pagination={{ pageSize: 5 }}
          scroll={{ x: 800 }}
        />
      </Card>

      {/* Samples Table */}
      <Card
        title={
          <Space>
            <ExperimentOutlined />
            <span>Biological Samples</span>
          </Space>
        }
        extra={
          <Tag color="green" icon={<CloudServerOutlined />}>
            Live Data
          </Tag>
        }
      >
        <Table
          columns={sampleColumns}
          dataSource={samples}
          rowKey="sample_id"
          pagination={{ pageSize: 5 }}
          scroll={{ x: 800 }}
        />
      </Card>

      {/* Footer Info */}
      <Alert
        message="Microservices Architecture"
        description="Data served by FastAPI Digital Twin Service with Redis caching | Django Core API for persistence"
        type="info"
        style={{ marginTop: 24 }}
        showIcon
      />
    </div>
  );
};
