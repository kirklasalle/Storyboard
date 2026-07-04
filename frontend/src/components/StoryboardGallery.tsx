import React, { useEffect, useState } from 'react';
import { Layout, Image as ImageIcon, Wand2, Download, RefreshCw, Loader2, AlertCircle, Activity, CheckCircle2, XCircle, ArrowRight, Sparkles, Info, Zap, Shield } from 'lucide-react';
import { API_BASE } from '../utils/api';

interface Attempt {
    model: string;
    status: 'success' | 'failed';
    reason?: string;
    note?: string;
}

interface ImageGenNotification {
    frameId: string;
    modelUsed: string;
    provider: string;
    attempts: Attempt[];
    visible: boolean;
}

interface ImageModelInfo {
    name: string;
    status: string;
    tier: string;
}

interface ImageStatus {
    ready: boolean;
    provider: string;
    text_model?: string;
    tier: string;
    message: string;
    models_available: ImageModelInfo[];
}

interface StoryboardGalleryProps {
    projectId: string;
    config?: any;
}

export const StoryboardGallery: React.FC<StoryboardGalleryProps> = ({ projectId, config }) => {
    const [frames, setFrames] = useState<any[]>([]);
    const [status, setStatus] = useState<'idle' | 'generating' | 'success' | 'error'>('idle');
    const [error, setError] = useState<string | null>(null);
    const [notification, setNotification] = useState<ImageGenNotification | null>(null);
    const [imageStatus, setImageStatus] = useState<ImageStatus | null>(null);
    const [showModelPanel, setShowModelPanel] = useState(false);

    // Fetch image status on mount
    useEffect(() => {
        fetchImageStatus();
    }, []);

    useEffect(() => {
        if (projectId) {
            handleGenerate();
        }
    }, [projectId]);

    // Auto-dismiss notification after 12 seconds
    useEffect(() => {
        if (notification?.visible) {
            const timer = setTimeout(() => {
                setNotification(prev => prev ? { ...prev, visible: false } : null);
            }, 12000);
            return () => clearTimeout(timer);
        }
    }, [notification?.visible]);

    const fetchImageStatus = async () => {
        try {
            const resp = await fetch(`${API_BASE}/providers/image-status`);
            if (resp.ok) {
                const data = await resp.json();
                setImageStatus(data);
            }
        } catch (e) {
            // Backend not reachable, but Pollinations.ai is always available
            setImageStatus({
                ready: true,
                provider: 'Pollinations.ai',
                tier: 'free',
                message: 'Backend unreachable. Free Pollinations.ai fallback available.',
                models_available: [{ name: 'Pollinations.ai', status: 'ready', tier: 'free' }]
            });
        }
    };

    const handleGenerate = async () => {
        setStatus('generating');
        setError(null);
        try {
            const resp = await fetch(`${API_BASE}/projects/${projectId}/generate`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(config || { type: 'openai', api_key: '' })
            });
            const data = await resp.json();
            if (resp.ok) {
                if (Array.isArray(data) && data.length === 0) {
                    setStatus('error');
                    setError('The AI could not identify any scenes or moments in this document. Try uploading a different script or story.');
                } else {
                    setFrames(data);
                    setStatus('success');
                    // Refresh image status after generation
                    fetchImageStatus();
                }
            } else {
                setStatus('error');
                setError(data.detail || data.error || 'Generation failed. Check your AI provider configuration.');
            }
        } catch (e: any) {
            console.error(e);
            setStatus('error');
            setError(e.message === 'Failed to fetch'
                ? 'Backend server is unreachable. Please ensure the Storyboard backend is running on port 8000.'
                : e.message
            );
        }
    };

    const handleGenerateImage = async (frameId: string) => {
        setFrames(prev => prev.map(f => f.id === frameId ? { ...f, generating: true, imageError: null } : f));
        setNotification(null);
        try {
            const resp = await fetch(`${API_BASE}/frames/${frameId}/generate-image`, {
                method: 'POST'
            });
            const data = await resp.json();
            if (resp.ok) {
                setFrames(prev => prev.map(f => f.id === frameId ? { ...f, image_path: data.image_url, generating: false } : f));

                setNotification({
                    frameId,
                    modelUsed: data.model_used || 'unknown',
                    provider: data.provider || 'unknown',
                    attempts: data.attempts || [],
                    visible: true
                });
            } else {
                setFrames(prev => prev.map(f => f.id === frameId ? { ...f, generating: false, imageError: data.detail || 'Failed' } : f));
            }
        } catch (e) {
            console.error(e);
            setFrames(prev => prev.map(f => f.id === frameId ? { ...f, generating: false, imageError: 'Backend unreachable' } : f));
        }
    };

    // ─── Telemetry Bar ──────────────────────────────────────────────
    const renderImageTelemetry = () => {
        if (!imageStatus) return null;

        const guaranteedModel = imageStatus.models_available.find(m => m.status === 'ready');
        const paidModels = imageStatus.models_available.filter(m => m.tier !== 'free');

        return (
            <div className="mb-8 rounded-2xl border border-white/5 bg-slate-900/60 backdrop-blur-lg overflow-hidden">
                {/* Top bar */}
                <div className="flex items-center justify-between px-5 py-3 border-b border-white/5">
                    <div className="flex items-center gap-3">
                        <div className={`w-2.5 h-2.5 rounded-full ${imageStatus.ready ? 'bg-emerald-400 shadow-lg shadow-emerald-500/40 animate-pulse' : 'bg-rose-400'}`} />
                        <span className="text-sm font-bold text-white">
                            Image Generation {imageStatus.ready ? 'Ready' : 'Unavailable'}
                        </span>
                        <span className="text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded-md bg-white/5 text-slate-400">
                            {imageStatus.provider}
                        </span>
                    </div>
                    <button
                        onClick={() => setShowModelPanel(!showModelPanel)}
                        className="text-xs font-bold text-slate-500 hover:text-white transition-colors flex items-center gap-1.5 px-3 py-1.5 rounded-lg hover:bg-white/5"
                    >
                        <Activity className="w-3 h-3" />
                        {showModelPanel ? 'Hide' : 'Show'} Model Chain
                    </button>
                </div>

                {/* Expandable model chain */}
                {showModelPanel && (
                    <div className="px-5 py-4 space-y-3 border-b border-white/5 animate-in slide-in-from-top-2 duration-300">
                        <p className="text-[10px] font-bold uppercase tracking-widest text-slate-600 mb-2">
                            Image Model Priority Chain
                        </p>
                        <div className="flex flex-wrap items-center gap-2">
                            {imageStatus.models_available.map((model, idx) => (
                                <React.Fragment key={idx}>
                                    <div className={`
                                        flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-bold
                                        ${model.status === 'ready'
                                            ? 'bg-emerald-500/10 border border-emerald-500/20 text-emerald-300'
                                            : 'bg-white/5 border border-white/5 text-slate-400'
                                        }
                                    `}>
                                        {model.status === 'ready' ? (
                                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                                        ) : (
                                            <Zap className="w-3.5 h-3.5 text-slate-500" />
                                        )}
                                        <span>{model.name}</span>
                                        <span className={`
                                            text-[9px] uppercase tracking-wider px-1.5 py-0.5 rounded-md
                                            ${model.tier === 'free' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-indigo-500/20 text-indigo-400'}
                                        `}>
                                            {model.tier}
                                        </span>
                                    </div>
                                    {idx < imageStatus.models_available.length - 1 && (
                                        <ArrowRight className="w-3 h-3 text-slate-700 flex-shrink-0" />
                                    )}
                                </React.Fragment>
                            ))}
                        </div>
                    </div>
                )}

                {/* Status summary */}
                <div className="flex items-center justify-between px-5 py-2.5">
                    <div className="flex items-center gap-3 text-xs text-slate-500">
                        <Shield className="w-3.5 h-3.5 text-emerald-500" />
                        <span>
                            {guaranteedModel
                                ? <><span className="text-emerald-400 font-bold">{guaranteedModel.name}</span> guaranteed fallback</>
                                : 'No guaranteed model'
                            }
                            {paidModels.length > 0 && (
                                <> · {paidModels.length} premium model{paidModels.length > 1 ? 's' : ''} in chain</>
                            )}
                        </span>
                    </div>
                    <span className="text-[10px] font-bold text-emerald-500 flex items-center gap-1">
                        <CheckCircle2 className="w-3 h-3" />
                        IMAGES WILL GENERATE
                    </span>
                </div>
            </div>
        );
    };

    // ─── Notification Toast ─────────────────────────────────────────
    const renderNotification = () => {
        if (!notification || !notification.visible) return null;

        const hasFailures = notification.attempts.some(a => a.status === 'failed');
        const isFallback = notification.modelUsed === 'Pollinations.ai';

        return (
            <div className="fixed bottom-6 right-6 z-50 max-w-md animate-in slide-in-from-bottom-4 fade-in duration-500">
                <div className={`
                    rounded-2xl border backdrop-blur-xl shadow-2xl overflow-hidden
                    ${isFallback
                        ? 'bg-amber-950/90 border-amber-500/30 shadow-amber-500/10'
                        : 'bg-emerald-950/90 border-emerald-500/30 shadow-emerald-500/10'
                    }
                `}>
                    <div className={`px-5 py-3 flex items-center justify-between border-b ${isFallback ? 'border-amber-500/20' : 'border-emerald-500/20'
                        }`}>
                        <div className="flex items-center gap-2.5">
                            {isFallback ? (
                                <div className="w-7 h-7 rounded-full bg-amber-500/20 flex items-center justify-center">
                                    <Info className="w-4 h-4 text-amber-400" />
                                </div>
                            ) : (
                                <div className="w-7 h-7 rounded-full bg-emerald-500/20 flex items-center justify-center">
                                    <Sparkles className="w-4 h-4 text-emerald-400" />
                                </div>
                            )}
                            <span className={`text-sm font-bold ${isFallback ? 'text-amber-200' : 'text-emerald-200'}`}>
                                {isFallback ? 'Model Fallback Active' : 'Image Generated'}
                            </span>
                        </div>
                        <button
                            onClick={() => setNotification(prev => prev ? { ...prev, visible: false } : null)}
                            className="text-slate-500 hover:text-white transition-colors text-xs font-bold px-2 py-1 rounded-lg hover:bg-white/5"
                        >
                            ✕
                        </button>
                    </div>

                    <div className="px-5 py-4 space-y-2.5">
                        <p className="text-[11px] font-bold uppercase tracking-widest text-slate-500 mb-3">
                            Model Resolution Chain
                        </p>
                        {notification.attempts.map((attempt, idx) => (
                            <div key={idx} className="flex items-center gap-3">
                                {attempt.status === 'success' ? (
                                    <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                                ) : (
                                    <XCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
                                )}
                                <div className="flex-1 min-w-0">
                                    <span className={`text-sm font-semibold ${attempt.status === 'success' ? 'text-white' : 'text-slate-400 line-through'
                                        }`}>
                                        {attempt.model}
                                    </span>
                                    {attempt.reason && (
                                        <p className="text-[11px] text-rose-400/80 truncate mt-0.5">{attempt.reason}</p>
                                    )}
                                    {attempt.note && (
                                        <p className="text-[11px] text-emerald-400/80 mt-0.5">{attempt.note}</p>
                                    )}
                                </div>
                                {idx < notification.attempts.length - 1 && attempt.status === 'failed' && (
                                    <ArrowRight className="w-3 h-3 text-slate-600 flex-shrink-0" />
                                )}
                            </div>
                        ))}
                    </div>

                    <div className={`px-5 py-3 border-t ${isFallback ? 'border-amber-500/20 bg-amber-950/50' : 'border-emerald-500/20 bg-emerald-950/50'
                        }`}>
                        <p className="text-[11px] text-slate-400">
                            {isFallback ? (
                                <>Rendered via <span className="font-bold text-amber-300">Pollinations.ai</span> — free community generation. Enable a paid image model for higher quality.</>
                            ) : (
                                <>Rendered via <span className="font-bold text-emerald-300">{notification.provider}</span> using <span className="font-bold text-emerald-300">{notification.modelUsed}</span></>
                            )}
                        </p>
                    </div>
                </div>
            </div>
        );
    };

    // ─── Main Render ────────────────────────────────────────────────
    return (
        <div className="space-y-8 animate-in fade-in duration-700">
            {/* Header */}
            <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                <div>
                    <h2 className="text-4xl font-black tracking-tight">Storyboard Discovery</h2>
                    <p className="text-slate-400">Visual narrative moments identified from your script</p>
                </div>
                <div className="flex items-center gap-4">
                    <button
                        onClick={handleGenerate}
                        disabled={status === 'generating'}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-2xl font-bold transition-all flex items-center gap-2 disabled:opacity-50"
                    >
                        {status === 'generating' ? (
                            <Loader2 className="w-5 h-5 animate-spin" />
                        ) : (
                            <RefreshCw className="w-5 h-5" />
                        )}
                        <span>{status === 'generating' ? 'Analyzing Script...' : 'Regenerate'}</span>
                    </button>
                    <button className="bg-slate-900 border border-white/5 hover:border-white/10 text-white px-6 py-3 rounded-2xl font-bold transition-all flex items-center gap-2">
                        <Download className="w-5 h-5" />
                        <span>Export PDF</span>
                    </button>
                </div>
            </div>

            {/* Image Generation Telemetry Bar */}
            {status === 'success' && renderImageTelemetry()}

            {/* Loading State */}
            {status === 'generating' && (
                <div className="py-20 text-center space-y-6">
                    <div className="relative inline-block">
                        <div className="w-24 h-24 rounded-full border-4 border-indigo-500/20 border-t-indigo-500 animate-spin"></div>
                        <Wand2 className="w-8 h-8 text-indigo-500 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2" />
                    </div>
                    <div className="space-y-2">
                        <h3 className="text-xl font-bold">Orchestrating AI Discovery</h3>
                        <p className="text-slate-500 max-w-sm mx-auto">
                            Performing triple-pass analysis to find intensity peaks and narrative flow...
                        </p>
                    </div>
                </div>
            )}

            {/* Error State */}
            {status === 'error' && (
                <div className="py-20 text-center space-y-6 max-w-2xl mx-auto">
                    <div className={`w-20 h-20 rounded-full ${error?.includes('Credits') ? 'bg-amber-500/20' : 'bg-rose-500/20'} flex items-center justify-center mx-auto animate-bounce`}>
                        <AlertCircle className={`w-10 h-10 ${error?.includes('Credits') ? 'text-amber-500' : 'text-rose-500'}`} />
                    </div>
                    <div className="space-y-3">
                        <h3 className="text-2xl font-black tracking-tight">
                            {error?.includes('Credits') ? 'Account Refill Required' : 'Analysis Interrupted'}
                        </h3>
                        <div className="glass-morphism p-6 rounded-2xl border border-white/5 bg-slate-900/50">
                            <p className="text-slate-300 leading-relaxed font-medium">{error}</p>
                        </div>
                    </div>
                    <button
                        onClick={handleGenerate}
                        className="bg-indigo-600 hover:bg-indigo-700 text-white px-8 py-3 rounded-2xl font-bold transition-all shadow-xl shadow-indigo-500/20"
                    >
                        Retry Analysis
                    </button>
                </div>
            )}

            {/* Frame Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {frames.map((frame, idx) => (
                    <div
                        key={idx}
                        className="glass-morphism rounded-3xl overflow-hidden border border-white/5 group hover:border-indigo-500/30 transition-all hover:translate-y-[-4px] flex flex-col"
                    >
                        {/* ── Image Area (top) ── */}
                        <div className="aspect-video bg-slate-900 relative flex items-center justify-center overflow-hidden group/img">
                            {frame.image_path ? (
                                <img
                                    src={frame.image_path}
                                    alt={frame.description}
                                    className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
                                    loading="lazy"
                                />
                            ) : (
                                <>
                                    <div className="absolute inset-0 bg-gradient-to-b from-transparent to-slate-950/80"></div>
                                    <ImageIcon className="w-12 h-12 text-slate-800 group-hover:scale-110 transition-transform" />
                                </>
                            )}

                            {frame.generating && (
                                <div className="absolute inset-0 bg-slate-950/60 backdrop-blur-sm flex items-center justify-center z-10">
                                    <div className="flex flex-col items-center gap-3">
                                        <Loader2 className="w-8 h-8 text-indigo-500 animate-spin" />
                                        <span className="text-[10px] font-bold uppercase tracking-widest text-indigo-400">Generating visual...</span>
                                    </div>
                                </div>
                            )}

                            {/* Scene badge */}
                            <div className="absolute top-4 left-4 z-20">
                                <span className="bg-indigo-500 text-white text-[10px] font-black uppercase tracking-widest px-2 py-1 rounded-md">
                                    Scene {frame.scene_number}
                                </span>
                            </div>

                            {/* Intensity badge */}
                            <div className="absolute top-4 right-4 z-20">
                                <div className="bg-slate-950/70 backdrop-blur-sm border border-white/10 text-white text-[10px] font-bold px-2 py-1 rounded-md flex items-center gap-1.5">
                                    <Activity className="w-3 h-3 text-indigo-400" />
                                    {Math.round(frame.intensity_score * 100)}%
                                </div>
                            </div>

                            {/* ── Cinematography Hover Panel (renders INSIDE the frame) ── */}
                            <div className="absolute inset-x-0 bottom-0 z-30 translate-y-full group-hover:translate-y-0 transition-transform duration-300 ease-out">
                                <div className="bg-slate-950/95 backdrop-blur-xl border-t border-indigo-500/20 p-4 space-y-3">
                                    {/* Panel header */}
                                    <div className="flex items-center justify-between">
                                        <span className="text-[9px] font-black uppercase tracking-widest text-indigo-400">
                                            Cinematography Spec
                                        </span>
                                        <span className={`text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full ${frame.intensity_type === 'Action Peak' ? 'bg-orange-500/20 text-orange-400' :
                                                frame.intensity_type === 'Emotional Peak' ? 'bg-rose-500/20 text-rose-400' :
                                                    'bg-slate-700/50 text-slate-400'
                                            }`}>
                                            {frame.intensity_type || 'Scene'}
                                        </span>
                                    </div>
                                    {/* Spec grid */}
                                    <div className="grid grid-cols-2 gap-x-4 gap-y-2">
                                        {frame.shot_type && (
                                            <div>
                                                <p className="text-[9px] font-bold text-slate-600 uppercase tracking-widest">Shot</p>
                                                <p className="text-[11px] font-semibold text-slate-200">{frame.shot_type}</p>
                                            </div>
                                        )}
                                        {frame.camera_movement && (
                                            <div>
                                                <p className="text-[9px] font-bold text-slate-600 uppercase tracking-widest">Camera</p>
                                                <p className="text-[11px] font-semibold text-slate-200">{frame.camera_movement}</p>
                                            </div>
                                        )}
                                        {frame.lens && (
                                            <div>
                                                <p className="text-[9px] font-bold text-slate-600 uppercase tracking-widest">Lens</p>
                                                <p className="text-[11px] font-semibold text-slate-200">{frame.lens}</p>
                                            </div>
                                        )}
                                        {frame.lighting && (
                                            <div>
                                                <p className="text-[9px] font-bold text-slate-600 uppercase tracking-widest">Lighting</p>
                                                <p className="text-[11px] font-semibold text-slate-200">{frame.lighting}</p>
                                            </div>
                                        )}
                                    </div>
                                    {/* Moment summary */}
                                    {frame.moment_summary && (
                                        <div className="pt-1 border-t border-white/5">
                                            <p className="text-[9px] font-bold text-slate-600 uppercase tracking-widest mb-1">Director's Note</p>
                                            <p className="text-[10px] text-slate-400 leading-relaxed italic">
                                                "{frame.moment_summary}"
                                            </p>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>

                        {/* ── Content Area (below image) ── */}
                        <div className="p-5 flex flex-col flex-1 gap-4">
                            {/* Description */}
                            <div className="flex-1 space-y-2">
                                <div className="flex items-center gap-2">
                                    <span className="text-[10px] font-bold uppercase tracking-widest text-slate-600">
                                        {frame.intensity_type} Moment
                                    </span>
                                </div>
                                <p className="text-sm text-slate-300 leading-relaxed">
                                    {frame.description}
                                </p>
                            </div>

                            {/* Error display */}
                            {frame.imageError && (
                                <div className="text-xs text-rose-400 bg-rose-500/10 border border-rose-500/20 rounded-xl px-3 py-2 flex items-center gap-2">
                                    <AlertCircle className="w-3.5 h-3.5 flex-shrink-0" />
                                    {frame.imageError}
                                </div>
                            )}

                            {/* Generate button with telemetry */}
                            <button
                                onClick={() => handleGenerateImage(frame.id)}
                                disabled={frame.generating}
                                className={`
                                    w-full py-3 rounded-xl text-xs font-bold transition-all flex items-center justify-center gap-2 disabled:opacity-50
                                    ${frame.image_path
                                        ? 'bg-white/5 hover:bg-white/10 text-slate-300'
                                        : 'bg-indigo-600/20 hover:bg-indigo-600/30 text-indigo-300 border border-indigo-500/20'
                                    }
                                `}
                            >
                                {frame.generating ? (
                                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                                ) : (
                                    <ImageIcon className="w-3.5 h-3.5" />
                                )}
                                <span>{frame.image_path ? 'Regenerate Visual' : 'Generate Visual'}</span>
                                {imageStatus && !frame.generating && (
                                    <span className="ml-1 text-[9px] font-bold uppercase tracking-widest text-emerald-500 flex items-center gap-1">
                                        <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block"></span>
                                        {imageStatus.provider}
                                    </span>
                                )}
                            </button>
                        </div>
                    </div>
                ))}
            </div>

            {/* Notification Toast */}
            {renderNotification()}
        </div>
    );
};
