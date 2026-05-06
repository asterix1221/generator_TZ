import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { ProjectType, ComplexityLevel, Specification } from '../types';
import { specApi, exportApi, authApi } from '../services/api';

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
  const [generatedSpec, setGeneratedSpec] = useState<Specification | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setGeneratedSpec(null);
    try {
      const spec = await specApi.generate(type, complexity);
      const token = authApi.getToken();
      if (token) {
        navigate(`/specification/${spec.id}`);
      } else {
        setGeneratedSpec(spec);
        toast.success('ТЗ создано! Зарегистрируйтесь, чтобы сохранять свои ТЗ');
      }
    } catch (error: any) {
      toast.error(error.response?.data?.detail || 'Ошибка при создании ТЗ');
    } finally {
      setLoading(false);
    }
  };

  const downloadDocx = async () => {
    if (!generatedSpec) return;
    try {
      const blob = await exportApi.downloadDocx(generatedSpec.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${generatedSpec.title}.docx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error('Ошибка при скачивании DOCX');
    }
  };

  const downloadPdf = async () => {
    if (!generatedSpec) return;
    try {
      const blob = await exportApi.downloadPdf(generatedSpec.id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${generatedSpec.title}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      toast.error('Ошибка при скачивании PDF');
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

      {!authApi.getToken() && !generatedSpec && (
        <div className="mt-8 text-center text-gray-500 text-sm">
          <p>Гостевой режим: ТЗ создаётся без сохранения в истории</p>
          <p className="mt-1">Войдите, чтобы сохранять и редактировать свои ТЗ</p>
        </div>
      )}

      {generatedSpec && (
        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-bold">{generatedSpec.title}</h2>
            <div className="flex gap-2">
              <button
                onClick={downloadDocx}
                className="bg-green-600 text-white px-3 py-1.5 rounded text-sm hover:bg-green-700"
              >
                DOCX
              </button>
              <button
                onClick={downloadPdf}
                className="bg-red-600 text-white px-3 py-1.5 rounded text-sm hover:bg-red-700"
              >
                PDF
              </button>
            </div>
          </div>

          <div className="text-sm text-gray-500 mb-4">
            <span>Тип: {generatedSpec.type}</span>
            <span className="mx-2">|</span>
            <span>Сложность: {generatedSpec.complexity}</span>
          </div>

          {(generatedSpec.content as any).goal && (
            <div className="mb-4">
              <h3 className="font-medium text-gray-800 mb-1">Цель</h3>
              <p className="text-gray-600">{(generatedSpec.content as any).goal}</p>
            </div>
          )}

          {(generatedSpec.content as any).description && (
            <div className="mb-4">
              <h3 className="font-medium text-gray-800 mb-1">Описание</h3>
              <p className="text-gray-600">{(generatedSpec.content as any).description}</p>
            </div>
          )}

          <div className="text-center mt-4">
            <a
              href="/register"
              className="text-blue-600 hover:underline text-sm"
              onClick={(e) => { e.preventDefault(); navigate('/register'); }}
            >
              Зарегистрируйтесь, чтобы редактировать и сохранять ТЗ
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default Home;