import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Specification, SpecificationContent } from '../types';
import { specApi, exportApi } from '../services/api';

function SpecificationView() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [spec, setSpec] = useState<Specification | null>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [editingTitle, setEditingTitle] = useState(false);
  const [title, setTitle] = useState('');
  const [content, setContent] = useState<SpecificationContent | null>(null);
  const [shareLink, setShareLink] = useState<string | null>(null);

  useEffect(() => {
    loadSpec();
  }, [id]);

  const loadSpec = async () => {
    if (!id) return;
    try {
      const data = await specApi.get(id);
      setSpec(data);
      setTitle(data.title);
      setContent(data.content);
    } catch (error: any) {
      toast.error('ТЗ не найдено');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const saveChanges = useCallback(async () => {
    if (!id || !content) return;
    setSaving(true);
    try {
      await specApi.update(id, title, content);
      toast.success('Сохранено');
    } catch (error: any) {
      toast.error('Ошибка сохранения');
    } finally {
      setSaving(false);
    }
  }, [id, title, content]);

  useEffect(() => {
    if (!spec) return;
    const timer = setTimeout(() => {
      saveChanges();
    }, 2000);
    return () => clearTimeout(timer);
  }, [content, title]);

  const handleShare = async () => {
    if (!id) return;
    try {
      const link = await specApi.share(id);
      setShareLink(link.url);
      toast.success('Ссылка скопирована');
      navigator.clipboard.writeText(window.location.origin + link.url);
    } catch (error: any) {
      toast.error('Ошибка создания ссылки');
    }
  };

  const downloadDocx = async () => {
    if (!id) return;
    try {
      const blob = await exportApi.downloadDocx(id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${title}.docx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error: any) {
      toast.error('Ошибка экспорта');
    }
  };

  const downloadPdf = async () => {
    if (!id) return;
    try {
      const blob = await exportApi.downloadPdf(id);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${title}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error: any) {
      toast.error('Ошибка экспорта');
    }
  };

  const downloadTrello = async () => {
    if (!id) return;
    try {
      const data = await exportApi.getTrello(id);
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${title}-trello.json`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (error: any) {
      toast.error('Ошибка экспорта');
    }
  };

  const updateContent = (field: keyof SpecificationContent, value: string | string[]) => {
    if (!content) return;
    setContent({ ...content, [field]: value });
  };

  if (loading) {
    return <div className="text-center py-8">Загрузка...</div>;
  }

  if (!spec || !content) {
    return <div className="text-center py-8">ТЗ не найдено</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="flex justify-between items-start mb-6">
        {editingTitle ? (
          <input
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onBlur={() => setEditingTitle(false)}
            onKeyDown={(e) => e.key === 'Enter' && setEditingTitle(false)}
            className="text-2xl font-bold border border-gray-300 rounded px-2 py-1"
            autoFocus
          />
        ) : (
          <h1
            className="text-2xl font-bold cursor-pointer hover:text-blue-600"
            onClick={() => setEditingTitle(true)}
          >
            {title}
          </h1>
        )}
        {saving && <span className="text-sm text-gray-500">Сохранение...</span>}
      </div>

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex gap-2 mb-4">
          <button onClick={downloadDocx} className="bg-gray-100 px-4 py-2 rounded hover:bg-gray-200">
            DOCX
          </button>
          <button onClick={downloadPdf} className="bg-gray-100 px-4 py-2 rounded hover:bg-gray-200">
            PDF
          </button>
          <button onClick={downloadTrello} className="bg-gray-100 px-4 py-2 rounded hover:bg-gray-200">
            Trello JSON
          </button>
          <button onClick={handleShare} className="bg-gray-100 px-4 py-2 rounded hover:bg-gray-200">
            Поделиться
          </button>
        </div>
        {shareLink && (
          <div className="text-sm text-green-600 mb-4">
            Ссылка скопирована: {window.location.origin}{shareLink}
          </div>
        )}
      </div>

      <div className="space-y-6">
        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-medium mb-2">Цель</h2>
          <textarea
            value={content.goal}
            onChange={(e) => updateContent('goal', e.target.value)}
            className="w-full border border-gray-300 rounded p-2"
            rows={2}
          />
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-medium mb-2">Описание</h2>
          <textarea
            value={content.description}
            onChange={(e) => updateContent('description', e.target.value)}
            className="w-full border border-gray-300 rounded p-2"
            rows={3}
          />
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-medium mb-2">Функциональные требования</h2>
          <textarea
            value={content.functional_requirements.join('\n')}
            onChange={(e) => updateContent('functional_requirements', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={5}
          />
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-medium mb-2">Требования к БД</h2>
          <textarea
            value={content.db_requirements.join('\n')}
            onChange={(e) => updateContent('db_requirements', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={4}
          />
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-medium mb-2">Стек технологий</h2>
          <textarea
            value={content.tech_stack.join('\n')}
            onChange={(e) => updateContent('tech_stack', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={3}
          />
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-lg font-medium mb-2">Список фич</h2>
          <textarea
            value={content.features.join('\n')}
            onChange={(e) => updateContent('features', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={4}
          />
        </div>
      </div>
    </div>
  );
}

export default SpecificationView;