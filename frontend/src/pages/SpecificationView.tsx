import { useState, useEffect, useCallback } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import { Specification, SpecificationContent } from '../types';
import { specApi, exportApi, authApi } from '../services/api';

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
  const [isReadOnly, setIsReadOnly] = useState(true);

  const token = authApi.getToken();

  useEffect(() => {
    setIsReadOnly(!token);
  }, [token]);

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
      navigate('/');
    } finally {
      setLoading(false);
    }
  };

  const saveChanges = useCallback(async () => {
    if (!id || !content || isReadOnly) return;
    setSaving(true);
    try {
      await specApi.update(id, title, content);
      toast.success('Сохранено');
    } catch (error: any) {
      toast.error('Ошибка сохранения');
    } finally {
      setSaving(false);
    }
  }, [id, title, content, isReadOnly]);

  useEffect(() => {
    if (!spec || isReadOnly) return;
    const timer = setTimeout(() => {
      saveChanges();
    }, 2000);
    return () => clearTimeout(timer);
  }, [content, title, spec, isReadOnly]);

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
    } catch {
      toast.error('Ошибка экспорта DOCX');
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
    } catch {
      toast.error('Ошибка экспорта PDF');
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
    } catch {
      toast.error('Ошибка экспорта Trello');
    }
  };

  const updateContent = (field: keyof SpecificationContent, value: string | string[]) => {
    if (!content || isReadOnly) return;
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
        {editingTitle && !isReadOnly ? (
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
            className={`text-2xl font-bold ${isReadOnly ? '' : 'cursor-pointer hover:text-blue-600'}`}
            onClick={() => !isReadOnly && setEditingTitle(true)}
          >
            {title}
          </h1>
        )}
        {saving && !isReadOnly && <span className="text-sm text-gray-500">Сохранение...</span>}
        {isReadOnly && (
          <span className="text-sm text-gray-400 bg-gray-100 px-2 py-1 rounded">
            Только чтение
          </span>
        )}
      </div>

      {isReadOnly && (
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6 text-sm text-yellow-800">
          Вы просматриваете ТЗ в режиме чтения.{' '}
          <a href="/login" className="underline">Войдите</a>, чтобы редактировать и сохранять изменения.
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <div className="flex gap-2 flex-wrap">
          <button onClick={downloadDocx} className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700">
            DOCX
          </button>
          <button onClick={downloadPdf} className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700">
            PDF
          </button>
          <button onClick={downloadTrello} className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700">
            Trello JSON
          </button>
          {!isReadOnly && (
            <button onClick={handleShare} className="bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700">
              Поделиться
            </button>
          )}
        </div>
        {shareLink && (
          <div className="text-sm text-green-600 mt-4 bg-green-50 border border-green-200 rounded p-2">
            Ссылка скопирована: {window.location.origin}{shareLink}
          </div>
        )}
      </div>

      <div className="space-y-6">
        <Section title="Цель" readonly={isReadOnly}>
          <textarea
            value={content.goal}
            onChange={(e) => updateContent('goal', e.target.value)}
            className="w-full border border-gray-300 rounded p-2"
            rows={2}
            readOnly={isReadOnly}
          />
        </Section>

        <Section title="Описание" readonly={isReadOnly}>
          <textarea
            value={content.description}
            onChange={(e) => updateContent('description', e.target.value)}
            className="w-full border border-gray-300 rounded p-2"
            rows={3}
            readOnly={isReadOnly}
          />
        </Section>

        <Section title="Функциональные требования" readonly={isReadOnly}>
          <textarea
            value={content.functional_requirements.join('\n')}
            onChange={(e) => updateContent('functional_requirements', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={5}
            readOnly={isReadOnly}
          />
        </Section>

        <Section title="Требования к БД" readonly={isReadOnly}>
          <textarea
            value={content.db_requirements.join('\n')}
            onChange={(e) => updateContent('db_requirements', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={4}
            readOnly={isReadOnly}
          />
        </Section>

        <Section title="Стек технологий" readonly={isReadOnly}>
          <textarea
            value={content.tech_stack.join('\n')}
            onChange={(e) => updateContent('tech_stack', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={3}
            readOnly={isReadOnly}
          />
        </Section>

        <Section title="Список фич" readonly={isReadOnly}>
          <textarea
            value={content.features.join('\n')}
            onChange={(e) => updateContent('features', e.target.value.split('\n'))}
            className="w-full border border-gray-300 rounded p-2"
            rows={4}
            readOnly={isReadOnly}
          />
        </Section>
      </div>
    </div>
  );
}

function Section({ title, children, readonly }: { title: string; children: React.ReactNode; readonly: boolean }) {
  return (
    <div className={`bg-white rounded-lg shadow-md p-6 ${readonly ? 'opacity-90' : ''}`}>
      <h2 className="text-lg font-medium mb-2">{title}</h2>
      {children}
    </div>
  );
}

export default SpecificationView;