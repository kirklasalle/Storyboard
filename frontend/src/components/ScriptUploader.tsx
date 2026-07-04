import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle, Shield, BookOpen } from 'lucide-react';
import { API_BASE } from '../utils/api';

interface ScriptUploaderProps {
    onUploadSuccess: (id: string) => void;
    projectId: string;
}

export const ScriptUploader: React.FC<ScriptUploaderProps> = ({ onUploadSuccess, projectId }) => {
    const [file, setFile] = useState<File | null>(null);
    const [status, setStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setStatus('uploading');
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`${API_BASE}/projects/${projectId}/scripts`, {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const data = await response.json();
                setStatus('success');
                onUploadSuccess(data.id);
            } else {
                setStatus('error');
            }
        } catch (error) {
            console.error('Upload failed:', error);
            setStatus('error');
        }
    };

    return (
        <div className="glass-morphism rounded-2xl p-8 border border-white/10 max-w-xl mx-auto">
            <div className="flex flex-col items-center gap-6 text-center">
                <div className="w-16 h-16 rounded-full bg-indigo-500/20 flex items-center justify-center">
                    <FileText className="w-8 h-8 text-indigo-500" />
                </div>
                <div>
                    <h3 className="text-xl font-bold">Upload Your Script</h3>
                    <p className="text-slate-400">PDF, Final Draft (.fdx), Fountain, Word (.docx), or plain text</p>
                </div>

                <label className="w-full h-32 border-2 border-dashed border-slate-700 rounded-xl flex items-center justify-center cursor-pointer hover:border-indigo-500/50 transition-colors group">
                    <input type="file" className="hidden" onChange={handleFileChange} />
                    {file ? (
                        <span className="text-slate-200 font-medium">{file.name}</span>
                    ) : (
                        <div className="flex flex-col items-center gap-2">
                            <Upload className="w-5 h-5 text-slate-500 group-hover:text-indigo-500 transition-colors" />
                            <span className="text-sm text-slate-500">Click to browse</span>
                        </div>
                    )}
                </label>

                {file && status !== 'success' && (
                    <button
                        onClick={handleUpload}
                        disabled={status === 'uploading'}
                        className="w-full py-3 bg-indigo-600 rounded-xl font-bold hover:bg-indigo-700 transition-all flex items-center justify-center gap-2"
                    >
                        {status === 'uploading' ? 'Analyzing...' : 'Analyze Script'}
                    </button>
                )}

                {/* ── Content Agreement Notice ────────────────────────── */}
                <div className="w-full rounded-xl border border-indigo-500/15 bg-indigo-500/5 p-4 text-left space-y-3">
                    <div className="flex items-center gap-2">
                        <Shield className="w-3.5 h-3.5 text-indigo-400 shrink-0" />
                        <span className="text-[10px] font-black uppercase tracking-widest text-indigo-400">
                            Content Agreement — Active &amp; Binding
                        </span>
                    </div>
                    <p className="text-[10px] text-slate-400 leading-relaxed">
                        By uploading, you grant Storyboard AI an irrevocable license to analyze your work
                        and learn from it — like a skilled reader who learns <em>craft and pattern</em>,
                        not verbatim content. <strong className="text-slate-300">You retain full copyright.</strong> Raw content
                        is analyzed then discarded. Only distilled cinematic insights are added to our
                        Knowledge Base. No personal data is stored.
                    </p>
                    <div className="grid grid-cols-2 gap-1.5">
                        {[
                            'You keep full copyright',
                            'Raw content is never stored',
                            'Only craft insights retained',
                            'No personal data stored',
                        ].map((point) => (
                            <div key={point} className="flex items-center gap-1.5 text-[9px] text-slate-500">
                                <div className="w-1 h-1 rounded-full bg-indigo-500 shrink-0" />
                                {point}
                            </div>
                        ))}
                    </div>
                    <div className="flex items-center gap-1.5 pt-1 border-t border-white/5">
                        <BookOpen className="w-3 h-3 text-slate-600 shrink-0" />
                        <span className="text-[9px] text-slate-600">
                            Governed by Kirk LaSalle's 10 Laws (Laws 6, 7 &amp; 8 — Privacy, Transparency &amp; Equity)
                        </span>
                    </div>
                </div>

                {status === 'success' && (
                    <div className="flex items-center gap-2 text-emerald-500 font-medium">
                        <CheckCircle className="w-5 h-5" />
                        <span>Analysis Complete!</span>
                    </div>
                )}

                {status === 'error' && (
                    <div className="flex items-center gap-2 text-rose-500 font-medium">
                        <AlertCircle className="w-5 h-5" />
                        <span>Upload failed. Please try again.</span>
                    </div>
                )}
            </div>
        </div>
    );
};
