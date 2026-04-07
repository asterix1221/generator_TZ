import { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Specification, ProjectType, ComplexityLevel } from '../types';
import { specApi } from '../services/api';

const PROJECT_TYPES: { value: ProjectType; label: string }[] = [
  { value: 'Web', label: 'Веб' },
  { value: 'Mobile', label: 'Мобильное' },
  { value: 'Game', label: 'Игра' },
  { value: 'Corp IS', label: 'Корпоративная система' },
  { value: 'Other', label: 'Другое' },
];

function Dashboard() {
  const navigate = useNavigate();
  const [specs, setSpecs] = useState<Specification[]>([]);
  const [loading, setLoading] = useState(true);
  const [type, setType] = useState<ProjectType>('Web');
  const [complexity, setComplexity] = useState<ComplexityLevel>(1);
  const [generating, setGenerating] = useState(false);

  useEffect(() => {
    loadSpecs();
  }, []);

  const loadSpecs = async () => {
    try {
      const data = await specApi.list();
      setSpecs(data);
    } catch (error: any) {
      if (error.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const spec = await specApi.generate(type, complexity);
      navigate(`/specification/${spec.id}`);
    } catch (error: any) {
      toast.error('Ошибка при создании ТЗ');
    } finally {
      setGenerating(false);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Удалить это ТЗ?')) return;
    try {
      await specApi.delete(id);
      setSpecs(specs.filter(s => s.id !== id));
      toast.success('ТЗ удалено');
    } catch (error: any) {
      toast.error('Ошибка удаления');
    }
  };

  if (loading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">Мои технические задания</h1>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-medium mb-4">Создать новое ТЗ</h2>
        <div className="flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-sm text-gray-600 mb-1">Тип проекта</label>
            <select
              value={type}
              onChange={(e) => setType(e.target.value as ProjectType)}
              className="border border-gray-300 rounded-lg px-3 py-2"
            >
              {PROJECT_TYPES.map(pt => (
                <option key={pt.value} value={pt.value}>{pt.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm text-gray-600 mb-1">Сложность</label>
            <select
              value={complexity}
              onChange={(e) => setComplexity(Number(e.target.value) as ComplexityLevel)}
              className="border border-gray-300 rounded-lg px-3 py-2"
            >
              <option value={1}>Базовый</option>
              <option value={2}>Средний</option>
              <option value={3}>Продвинутый</option>
              <option value={4}>Профессиональный</option>
            </select>
          </div>
          <button
            onClick={handleGenerate}
            disabled={generating}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 disabled:opacity-50"
          >
            {generating ? 'Создание...' : 'Создать'}
          </button>
        </div>
      </div>

      {specs.length === 0 ? (
        <div className="text-center text-gray-500 py-8">
          У вас пока нет технических заданий. Создайте первое!
        </div>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {specs.map(spec => (
            <div key={spec.id} className="bg-white rounded-lg shadow-md p-4">
              <h3 className="font-medium text-lg mb-2">{spec.title}</h3>
              <div className="text-sm text-gray-500 mb-4">
                <span>Тип: {spec.type}</span> | <span>Сложность: {spec.complexity}</span>
              </div>
              <div className="flex gap-2">
                <Link
                  to={`/specification/${spec.id}`}
                  className="text-blue-600 hover:underline text-sm"
                >
                  Открыть
                </Link>
                <button
                  onClick={() => handleDelete(spec.id)}
                  className="text-red-600 hover:underline text-sm"
                >
                  Удалить
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Dashboard;