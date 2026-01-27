import { useEffect, useState } from 'react';
import { Card, Table, Select, Space, Alert, Spin, Tag, Button } from 'antd';
import { ExperimentOutlined, ReloadOutlined } from '@ant-design/icons';
import { apiService } from '../../shared/services/api';
import type { TransportBox, Sample } from '../../shared/services/api';

const getStatusColor = (status: string) => {
  const colors: { [key: string]: string } = {
    'collected': 'blue',
    'in_transit': 'processing',
    'stored': 'success',
    'analyzed': 'purple',
    'disposed': 'default',
  };
  return colors[status.toLowerCase()] || 'default';
};

export const BoxSamples = () => {
  const [boxes, setBoxes] = useState<TransportBox[]>([]);
  const [samples, setSamples] = useState<Sample[]>([]);
  const [selectedBoxId, setSelectedBoxId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchBoxes = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.getBoxes();
      setBoxes(data);
      if (data.length > 0 && !selectedBoxId) {
        setSelectedBoxId(data[0].id);
      }
    } catch (err) {
      setError('Failed to fetch transport boxes');
      console.error('Error fetching boxes:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSamples = async () => {
    setLoading(true);
    try {
      const data = await apiService.getSamples();
      setSamples(data);
    } catch (err) {
      console.error('Error fetching samples:', err);
      setSamples([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBoxes();
    fetchSamples();
  }, []);

  const filteredSamples = selectedBoxId 
    ? samples.filter(s => s.box === selectedBoxId)
    : samples;

  const columns = [
    {
      title: 'Sample ID',
      dataIndex: 'sample_id',
      key: 'sample_id',
      width: 150,
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
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (status: string) => (
        <Tag color={getStatusColor(status)}>{status}</Tag>
      ),
    },
    {
      title: 'Temperature',
      dataIndex: 'temperature',
      key: 'temperature',
      width: 120,
      render: (temp: number) => `${temp}°C`,
    },
    {
      title: 'Humidity',
      dataIndex: 'humidity',
      key: 'humidity',
      width: 100,
      render: (humidity: number) => `${humidity}%`,
    },
    {
      title: 'Collected',
      dataIndex: 'collected_at',
      key: 'collected_at',
      width: 180,
      render: (date: string) => new Date(date).toLocaleString(),
    },
  ];

  const selectedBox = boxes.find(b => b.id === selectedBoxId);

  return (
    <div style={{ padding: '24px' }}>
      <Card 
        title={
          <Space>
            <ExperimentOutlined />
            <span>Box Samples</span>
          </Space>
        }
        extra={
          <Button 
            icon={<ReloadOutlined />} 
            onClick={() => {
              fetchBoxes();
              fetchSamples();
            }}
            loading={loading}
          >
            Refresh
          </Button>
        }
      >
        {error && (
          <Alert
            message="Error"
            description={error}
            type="error"
            closable
            style={{ marginBottom: 16 }}
          />
        )}

        <Space direction="vertical" size="large" style={{ width: '100%' }}>
          <div>
            <label style={{ marginRight: 8, fontWeight: 500 }}>Select Transport Box:</label>
            <Select
              style={{ width: 300 }}
              placeholder="Select a box"
              value={selectedBoxId}
              onChange={setSelectedBoxId}
              loading={loading}
              options={boxes.map(box => ({
                label: `${box.box_id} - ${box.status}`,
                value: box.id,
              }))}
            />
            {selectedBox && (
              <span style={{ marginLeft: 16, color: '#666' }}>
                {filteredSamples.length} sample(s) in this box
              </span>
            )}
          </div>

          {loading ? (
            <div style={{ textAlign: 'center', padding: '50px 0' }}>
              <Spin size="large" tip="Loading samples..." />
            </div>
          ) : (
            <Table
              dataSource={filteredSamples}
              columns={columns}
              rowKey="sample_id"
              pagination={{ pageSize: 10 }}
              locale={{ emptyText: 'No samples found in this box' }}
            />
          )}
        </Space>
      </Card>
    </div>
  );
};
