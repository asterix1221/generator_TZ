import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ProjectType, ComplexityLevel } from '../types';
import { specApi, authApi } from '../services/api';

const PROJECT_TYPES: { value: ProjectType; label: string }[] = [
  { value: 'Web', label: 'Веб-приложение' },
  { value: 'Mobile', label: 'Мобильное приложение' },
  { value: 'Game', label: 'Игра' },
  { value: 'Corp IS', label: 'Корпоративная система' },
  { value: 'Other', label: 'Другое' },
];

const COMPLEXITY_LEVELS: { value: ComplexityLevel; label: string; description: string }[] = [
  { value: 1, label: 'Базовый', description: 'Простой проект для начинающих' },
  { value: 2, label: 'Средний', description: 'Стандартный учебный проект' },
  { value: 3, label: 'Продвинутый', description: 'Сложный проект с интеграциями' },
  { value: 4, label: 'Профессиональный', description: 'Production-ready проект' },
];

function Home() {
  const navigate = useNavigate();
  const [type, setType] = useState<ProjectType>('Web');
  const [complexity, setComplexity] = useState<ComplexityLevel>(1);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const spec = await specApi.generate(type, complexity);
      const token = authApi.getToken();
      if (token) {
        navigate(`/specification/${spec.id}`);
      } else {
        toast.success('ТЗ создано! Войдите, чтобы сохранить его');
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Ошибка при создании ТЗ');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold text-center mb-8">
        Генератор технических заданий
      </h1>
      <p className="text-center text-gray-600 mb-8">
        Создайте структурированное ТЗ для вашего учебного проекта за несколько секунд
      </p>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Тип проекта
          </label>
          <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
            {PROJECT_TYPES.map((pt) => (
              <button
                key={pt.value}
                onClick={() => setType(pt.value)}
                className={`p-3 rounded-lg border-2 transition-colors ${
                  type === pt.value
                    ? 'border-blue-600 bg-blue-50 text-blue-700'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                {pt.label}
              </button>
            ))}
          </div>
        </div>

        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Уровень сложности
          </label>
          <div className="space-y-2">
            {COMPLEXITY_LEVELS.map((cl) => (
              <button
                key={cl.value}
                onClick={() => setComplexity(cl.value)}
                className={`w-full p-4 rounded-lg border-2 text-left transition-colors ${
                  complexity === cl.value
                    ? 'border-blue-600 bg-blue-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="font-medium">{cl.label}</div>
                <div className="text-sm text-gray-500">{cl.description}</div>
              </button>
            ))}
          </div>
        </div>

        <button
          onClick={handleGenerate}
          disabled={loading}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50 transition-colors"
        >
          {loading ? 'Создание ТЗ...' : 'Создать техническое задание'}
        </button>
      </div>

      <div className="mt-8 text-center text-gray-500 text-sm">
        <p>Гостевой режим: ТЗ создаётся без сохранения</p>
        <p className="mt-1">Войдите, чтобы сохранять и редактировать свои ТЗ</p>
      </div>
    </div>
  );
}

export default Home;