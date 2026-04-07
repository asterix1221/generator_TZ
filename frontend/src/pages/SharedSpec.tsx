import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Specification } from '../types';
import { specApi } from '../services/api';

function SharedSpec() {
  const { token } = useParams<{ token: string }>();
  const [spec, setSpec] = useState<Specification | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSharedSpec();
  }, [token]);

  const loadSharedSpec = async () => {
    if (!token) return;
    try {
      const data = await specApi.getShared(token);
      setSpec(data);
    } catch (error: any) {
      toast.error('ТЗ не найдено или ссылка недействительна');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  if (!spec) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600 mb-4">ТЗ не найдено</p>
        <Link to="/" className="text-blue-600 hover:underline">На главную</Link>
      </div>
    );
  }

  const content = spec.content as any;

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">{spec.title}</h1>
      
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-medium mb-2">Цель</h2>
        <p className="text-gray-700">{content.goal}</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-medium mb-2">Описание</h2>
        <p className="text-gray-700">{content.description}</p>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-medium mb-2">Функциональные требования</h2>
        <ul className="list-disc list-inside">
          {(content.functional_requirements || []).map((item: string, i: number) => (
            <li key={i} className="text-gray-700">{item}</li>
          ))}
        </ul>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-medium mb-2">Требования к БД</h2>
        <ul className="list-disc list-inside">
          {(content.db_requirements || []).map((item: string, i: number) => (
            <li key={i} className="text-gray-700">{item}</li>
          ))}
        </ul>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-medium mb-2">Стек технологий</h2>
        <ul className="list-disc list-inside">
          {(content.tech_stack || []).map((item: string, i: number) => (
            <li key={i} className="text-gray-700">{item}</li>
          ))}
        </ul>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-lg font-medium mb-2">Список фич</h2>
        <ul className="list-disc list-inside">
          {(content.features || []).map((item: string, i: number) => (
            <li key={i} className="text-gray-700">{item}</li>
          ))}
        </ul>
      </div>

      <div className="text-center mt-8">
        <Link to="/" className="text-blue-600 hover:underline">Создать своё ТЗ</Link>
      </div>
    </div>
  );
}

export default SharedSpec;