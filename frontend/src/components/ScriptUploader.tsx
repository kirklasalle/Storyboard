import React, { useState } from 'react';
import { Upload, FileText, CheckCircle, AlertCircle } from 'lucide-react';

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
            const response = await fetch(`http://127.0.0.1:8000/projects/${projectId}/scripts`, {
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
                    <p className="text-slate-400">PDF or Text files are supported</p>
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
